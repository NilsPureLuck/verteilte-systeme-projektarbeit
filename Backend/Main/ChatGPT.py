from datetime import datetime
import openai
import os
from dotenv import load_dotenv
from fuzzywuzzy import fuzz
from Message import MessageToClient

# Set the OpenAI API key from the .env file for authentication.
load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')


def listenToMessages(chatHistory):
    # Extracts the last message from the chat history to analyze its content.
    message = chatHistory[len(chatHistory) - 1]
    message_str = message.message
    print("Message: " + message_str)
    # Checks the similarity between the last message and the word "alexa" using fuzzy matching (Levenshtein distance).
    similarity = fuzz.partial_ratio(message_str, "alexa")
    if similarity > 70:
        # If similarity is above 70, it's likely the user is addressing the bot.
        print("Bot should answer")
        return create_chatbot(chatHistory)
    else:
        # If similarity is below 70, it's likely the message is not directed at the bot.
        print("Bot should not answer")
        return None


def create_chatbot(chatHistory):
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
    messages.append({"role": "system",
                     "content": "Du bist ein intelligenter Assistent in einem Chatraum."
                                " Deine Aufgabe ist es, mit relevanten und hilfreichen Antworten"
                                " zu reagieren. Zusätzlich hast du Zugriff auf die letzten bis zu 5 Nachrichten aus"
                                " dem Chatverlauf. Diese Nachrichten enthalten jeweils den Nickname des Teilnehmers"
                                " und die Nachricht selbst. Deine Antworten sollten sowohl den Kontext dieser "
                                "Nachrichten berücksichtigen. Deine Stimmung wird algorithmisch auf einer Skala von -1 "
                                "(sehr negativ) bis 1 (sehr positiv) erfasst und soll in deinen Antworten"
                                " widergespiegelt werden. Deine aktuelle Stimmung liegt bei: " + str(sentiment)
                     }

                    )
    # Generates a chat completion using the OpenAI API, with parameters adjusted for the current context.
    response = openai.chat.completions.create(
        model="gpt-4-0125-preview",
        messages=messages,
        temperature=temperature,
        max_tokens=1000,
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
    return MessageToClient(username="Alexa", message=response_message, language="EN", timestamp=str_date_time,
                           sentiment=sentiment)


def checkSentiment(chatHistory):
    # Calculates the average sentiment of the chat history to inform response generation.
    sentiment_value = 0
    for message in chatHistory:
        sentiment_value += message.sentiment
    sentiment_value = sentiment_value / len(chatHistory)
    return sentiment_value
