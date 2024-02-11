import requests
from dotenv import load_dotenv
from .Message import MessageFromClient, MessageToClient
import os
import traceback
from datetime import datetime


def load_api_config():
    load_dotenv()
    return {
        "url": os.environ.get("SENTIMENT_ANALYSIS_URL"),
        "headers": {
            "X-RapidAPI-Key": os.environ.get("RAPIDAPI_KEY"),
            "X-RapidAPI-Host": os.environ.get("RAPIDAPI_HOST")
        }
    }

def get_sentiment_score(message_text: str, config: dict) -> float:
    """
    Queries the sentiment analysis API and returns the sentiment score.
    :param message_text: The text of the message to analyze.
    :param config: Configuration dictionary containing the API details.
    :return: Sentiment score of the message.
    """
    response = requests.get(config["url"], headers=config["headers"], params={"text": message_text})
    return response.json()["score"]

def sentiment_analysis(message: MessageFromClient, retry=False) -> MessageToClient:
    """
    Analyzes the sentiment of a given message, with an optional retry mechanism.
    :param message: Incoming message without a sentiment.
    :param retry: Indicates if the function is being retried.
    :return: Analyzed message with a sentiment.
    """
    try:
        config = load_api_config()
        sentiment_score = get_sentiment_score(message.message, config)
        message_dict = message.__dict__
        message_dict["sentiment"] = sentiment_score
        return MessageToClient.model_validate(message_dict)
    except Exception as e:
        print("An error occurred while performing sentiment analysis:", e)
        print(traceback.format_exc())
        if not retry:
            print("Retrying...")
            return sentiment_analysis(message, retry=True)
        else:
            return MessageToClient(username="Botify",
                                   message="I'm sorry, I couldn't analyse the sentiment of your message.",
                                   language="EN", timestamp=datetime.now().strftime("%H:%M:%S"), sentiment=0.0)

