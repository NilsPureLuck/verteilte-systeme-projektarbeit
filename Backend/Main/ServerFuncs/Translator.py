import os
import html
from google.cloud import translate_v2 as translate
from .Message import MessageFromClient, MessageToClient
import traceback


# Method to translate the messages
def translate_text(message: MessageFromClient | MessageToClient) -> MessageFromClient|MessageToClient:
    """
    This method translates an incoming message into the language specified in the message field message.language
    :param message: incoming message in original language
    :return: message: translated message
    """
    try:
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "../../credentials.json"
        translate_client = translate.Client()
        message_str = message.message
        target = message.language
        if isinstance(message_str, bytes):
            message_str = message_str.decode("utf-8")
        result = translate_client.translate(message_str, target_language=target)
        result["translatedText"] = html.unescape(result["translatedText"])
        message.message = result["translatedText"]
        return message, result["detectedSourceLanguage"]
    except Exception as e:
        print("An error occurred while translating the text:", e)
        print(traceback.format_exc())
        return message, "unknown"