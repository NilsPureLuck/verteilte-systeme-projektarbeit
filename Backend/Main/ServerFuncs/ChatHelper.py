from datetime import datetime
import openai
import os
from dotenv import load_dotenv
from fuzzywuzzy import fuzz
from .Message import MessageToClient
import traceback


def load_api_config():
    """
    This method loads the api key for the REST call to the chatbot.\n
    """
    try:
        load_dotenv()
        openai.api_key = os.getenv('OPENAI_API_KEY')
    except Exception as e:
        print(traceback.format_exc())


def listenToMessages(chatHistory: list) -> MessageToClient:
    """
    This method listens to incoming messages and determines whether the chatbot should be called.\n
    :param chatHistory: List of last 5 messages in the chat\n
    :return MessageToClient or None: either returns a message from the chatbot or None if the chatbot is not addressed
    or an Exception was thrown\n
    """
    try:
        message = chatHistory[len(chatHistory) - 1]
        message_str = message.message
        if is_message_addressing_bot(message_str):
            print("Bot should answer")
            return create_chatbot(chatHistory)
        else:
            print("Bot should not answer")
            return None
    except Exception as e:
        print(traceback.format_exc())
        return None


# Checks the similarity between the last message and the word "botify" using fuzzy matching (Levenshtein distance).
def is_message_addressing_bot(message_str: str) -> bool:
    """
    This method analyses if a message is addressing the chatbot. For this, it compares the similarity of the incoming
    string with the keyword "botify".\n
    :param message_str: Incoming message as a string\n
    :return Bool: True if the incoming message is addressing the chatbot, False otherwise\n
    """
    keyword = "botify"
    threshold = 70
    similarity = fuzz.partial_ratio(message_str.lower(), keyword.lower())
    # If similarity is above 70, it's likely the user is addressing the bot.
    return similarity > threshold


def create_chatbot(chatHistory: list, retry=False) -> MessageToClient:
    """
    Creates a chatbot response based on the sentiment of the chat history.\n
    :param chatHistory: List of last 5 messages in the chat\n
    :param retry: Indicates if this is a retry attempt\n
    :return MessageToClient: The response message object
    """
    try:
        sentiment = check_sentiment(chatHistory)
        messages = prepare_messages(chatHistory, sentiment)
        response_message = generate_response(messages, sentiment)
        return build_message_object(response_message, sentiment)
    except Exception as e:
        print("An error occurred while creating the chatbot:", e)
        if not retry:
            print("Retrying...")
            return create_chatbot(chatHistory, retry=True)
        else:
            return handle_error_on_retry_failure()


def prepare_messages(chatHistory: list, sentiment: float) -> list:
    """
    Prepares messages for OpenAI completion call.\n
    :param chatHistory: List of last 5 messages in the chat\n
    :param sentiment: Sentiment value of the chat history\n
    :return list: List of formatted messages
    """
    messages = [{"role": "user", "content": message.message} for message in chatHistory]
    messages.append({"role": "system", "content": "Deine aktuelle Stimmung liegt bei: " + str(sentiment)})
    return messages


def generate_response(messages: list, sentiment: float) -> str:
    """
    Generates a response using the OpenAI API.\n
    :param messages: List of messages\n
    :param sentiment: Sentiment value\n
    :return str: Generated response
    """
    temperature = calculate_temperature(sentiment)
    response = openai.chat.completions.create(
        model="gpt-4-0125-preview",  # Adjust the model as necessary
        messages=messages,
        temperature=temperature,
        max_tokens=100,
        frequency_penalty=0,
        presence_penalty=0
    )
    return response.choices[0].message.content


def calculate_temperature(sentiment: float) -> float:
    """
    Calculates response temperature based on sentiment.\n
    :param sentiment: Sentiment value\n
    :return float: Calculated temperature
    """
    min_temp, max_temp = 0.2, 0.8
    return 0.5 * (sentiment + 1) * (max_temp - min_temp) + min_temp


def build_message_object(response: str, sentiment: float) -> MessageToClient:
    """
    Build MessageToClient object\n
    :param response: Generated response\n
    :param sentiment: Sentiment value\n
    :return MessageToClient: Message object
    """
    return MessageToClient(username="Botify", message=response, language="EN",
                           timestamp=datetime.now().strftime("%H:%M:%S"), sentiment=sentiment)


def handle_error_on_retry_failure() -> MessageToClient:
    """
    Handles errors after a retry failure while creating the chatbot.\n
    :return MessageToClient: Error message object
    """
    print("Failed to create chatbot response even after retry.")
    return MessageToClient(username="Botify", message="I'm sorry, I'm not able to answer right now.",
                           language="EN", timestamp=datetime.now().strftime("%H:%M:%S"), sentiment=0.0)


def check_sentiment(chatHistory: list) -> float:
    """
    Calculates the average sentiment of the last 5 messages in the chat history.\n
    :param chatHistory: List of last 5 messages in the chat\n
    :return float: Average sentiment of the last 5 messages
    """
    try:
        sentiment_value = sum(message.sentiment for message in chatHistory) / len(chatHistory)
        return sentiment_value
    except Exception as e:
        print(traceback.format_exc())
        return 0.0
