import requests
from dotenv import load_dotenv
from .Message import MessageFromClient, MessageToClient
import os
import traceback
import datetime

def sentiment_analysis(message: MessageFromClient) -> MessageToClient:
	"""
	This method analyses the sentiment of a given message\n
	:param message: incoming message without a sentiment\n
	:return message: analysed message with a sentiment\n
	"""

	try:
		load_dotenv()
	except Exception as e:
		print(traceback.format_exc())

	try:
		url = os.environ.get("URL")
		headers = {
			"X-RapidAPI-Key": os.environ.get("XKEY"),
			"X-RapidAPI-Host": os.environ.get("XHOST")
		}
		querystring = {"text": message.message}
		response = requests.get(url, headers=headers, params=querystring)
		message = message.__dict__
		message["sentiment"] = response.json()["score"]
		return MessageToClient.model_validate(message)
	except Exception as e:
		print("An error occurred while performing sentiment analysis:", e)
		print(traceback.format_exc())
		return MessageToClient(username="Bot", message="I'm sorry, I couldn't analyse the sentiment of your message.",
							   language="EN", timestamp=datetime.now().strftime("%H:%M:%S"), sentiment=0.0)