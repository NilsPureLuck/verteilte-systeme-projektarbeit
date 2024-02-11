import os
import html
from typing import Tuple
from google.cloud import translate_v2 as translate
from .Message import MessageFromClient, MessageToClient


def initialize_translate_client():
    """
    Initializes the Google Translate client with the necessary credentials.\n
    :return translate_client: Client to translate incoming messages
    """
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "../../credentials.json"
    return translate.Client()


def translate_text(message: MessageFromClient | MessageToClient, retry=False) -> Tuple[
    MessageFromClient | MessageToClient, str]:
    """
    Translates an incoming message into the language specified in the message.language field.
    If an exception occurs, it retries once more.

    :param message: Incoming message in original language
    :param retry: Indicates if this is a retry attempt
    :return Tuple of (translated message, detected source language or "unknown" on error)
    """
    try:
        translate_client = initialize_translate_client()
        message_str = message.message
        target = message.language

        result = translate_client.translate(message_str, target_language=target)
        result["translatedText"] = html.unescape(result["translatedText"])
        message.message = result["translatedText"]
        return message, result["detectedSourceLanguage"]
    except Exception as e:
        print("An error occurred while translating the text:", e)
        if not retry:
            print("Retrying...")
            return translate_text(message, retry=True)
        else:
            return message, str("unknown")
