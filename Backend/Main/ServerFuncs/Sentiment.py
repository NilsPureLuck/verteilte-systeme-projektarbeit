import requests
from dotenv import load_dotenv
from .Message import MessageFromClient, MessageToClient
import os
import traceback
import datetime

def sentiment_analysis(message: MessageFromClient, retry=False) -> MessageToClient:
    """
    This method analyses the sentiment of a given message.
    :param message: incoming message without a sentiment
    :param retry: indicates if the function is being retried
    :return: analysed message with a sentiment
    """
    try:
        load_dotenv()
        url = os.environ.get("URL") #change name to SENTIMENT_ANALYSIS_URL
        headers = {
            "X-RapidAPI-Key": os.environ.get("XKEY"), # change name to RAPIDAPI_KEY
            "X-RapidAPI-Host": os.environ.get("XHOST") #  change name to  RAPIDAPI_HOST
        }
        querystring = {"text": message.message}
        response = requests.get(url, headers=headers, params=querystring)
        message_dict = message.__dict__
        message_dict["sentiment"] = response.json()["score"]
        return MessageToClient.model_validate(message_dict)

    except Exception as e:
        print("An error occurred while performing sentiment analysis:", e)
        print(traceback.format_exc())
        if not retry:
            print("Retrying...")
            return sentiment_analysis(message, retry=True)
        else:
            # Return a default message if retry fails
            return MessageToClient(username="Botify",
                                   message="I'm sorry, I couldn't analyse the sentiment of your message.",
                                   language="EN", timestamp=datetime.now().strftime("%H:%M:%S"), sentiment=0.0)