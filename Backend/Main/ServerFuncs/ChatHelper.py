from datetime import datetime
import openai
import os
from dotenv import load_dotenv
from fuzzywuzzy import fuzz
from .Message import MessageToClient

# Set the OpenAI API key from the .env file for authentication.
load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')


def listenToMessages(chatHistory: list) -> MessageToClient | None:
    """
    This method listens to incoming messages and determines whether the chatbot should be called\n
    :param chatHistory: List of last 5 messages in the chat\n
    :return message object or None: either return a message from the chatbot or None if the chatbot is not addressed\n
    """
    message = chatHistory[len(chatHistory) - 1]
    message_str = message.message
    if is_message_addressing_bot(message_str):
        print("Bot should answer")
        return create_chatbot(chatHistory)
    else:
        print("Bot should not answer")
        return None


# Checks the similarity between the last message and the word "botify" using fuzzy matching (Levenshtein distance).
def is_message_addressing_bot(message_str: str) -> bool:
    """
    This method analyses if a message is addressing the chatbot. For this, it compares the similarity of the incoming
    string with the keyword "botify"\n
    :param message_str: Incoming message as a string\n
    :return Bool: True if the incoming message is addressing the chatbot, False otherwise\n
    """
    keyword = "botify"
    threshold = 70
    similarity = fuzz.partial_ratio(message_str.lower(), keyword.lower())
    # If similarity is above 70, it's likely the user is addressing the bot.
    return similarity > threshold


def create_chatbot(chatHistory: list) -> MessageToClient:
    """
    This method creates a chatbot and forwards a list of the last 5 messages to it\n
    :param chatHistory: List of last 5 messages in the chat\n
    :return message: Answer from the chatbot\n
    """
    messages = []
    # Analyzes the overall sentiment of the chat history to adjust the bot's responses.
    sentiment = checkSentiment(chatHistory)

    # Calculates the response temperature based on sentiment, influencing the randomness/"creativity" of responses.
    min_temp = 0.2
    max_temp = 0.8
    temperature = 0.5 * (sentiment + 1) * (max_temp - min_temp) + min_temp

    # Prepares the message history for the OpenAI completion call, formatting them appropriately.
    for message in chatHistory:
        messages.append({"role": "user", "content": f"{message.message}"})

    # Adds a system message to guide the behavior of the OpenAI-API, providing context for its responses.
    # 100 Tokens ≈ 75 words according to openAPI documentation
    messages.append({"role": "system",
                     "content": "Du bist ein intelligenter Assistent in einem Chatraum und du heißt Botify."
                                " Deine Aufgabe ist es, mit relevanten und hilfreichen Antworten"
                                " zu reagieren. Zusätzlich hast du Zugriff auf die letzten bis zu 5 Nachrichten aus"
                                " dem Chatverlauf. Diese Nachrichten enthalten jeweils den Nickname des Teilnehmers"
                                " und die Nachricht selbst. Deine Antworten sollten den Kontext dieser "
                                "Nachrichten berücksichtigen. Deine Antworten sollten maximal aus 70 Wörten bestehen."
                                "Deine Stimmung wird algorithmisch auf einer Skala von -1 "
                                "(sehr negativ) bis 1 (sehr positiv) erfasst und soll in deinen Antworten"
                                " widergespiegelt werden. Deine aktuelle Stimmung liegt bei: " + str(sentiment)
                     }

                    )
    # Generates a chat completion using the OpenAI API, with parameters adjusted for the current context.
    response = openai.chat.completions.create(
        model="gpt-4-0125-preview",
        messages=messages,
        temperature=temperature,
        max_tokens=100,
        frequency_penalty=0,
        presence_penalty=0,
    )
    # Extracts and prints the generated response from the OpenAI API.
    response_message = response.choices[0].message.content
    messages.append({"role": "assistant", "content": response_message})
    print("\n" + response_message + "\n")

    # Captures the current time to timestamp the bot's response.
    date_time = datetime.now()
    str_date_time = date_time.strftime("%H:%M:%S")

    # Returns a new message object with the bot's response and additional metadata.
    return MessageToClient(username="Botify", message=response_message, language="EN", timestamp=str_date_time,
                           sentiment=sentiment)


def checkSentiment(chatHistory: list) -> float:
    """
    This method calculates the average sentiment of the last 5 messages in the chatHistory\n
    :param chatHistory: List of last 5 messages in the chat\n
    :return sentiment_value: average sentiment of the last 5 messages\n
    """
    # Calculates the average sentiment of the chat history to inform response generation.
    sentiment_value = 0
    for message in chatHistory:
        sentiment_value += message.sentiment
    sentiment_value = sentiment_value / len(chatHistory)
    return sentiment_value
