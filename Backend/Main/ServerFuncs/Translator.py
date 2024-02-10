import os
import html
from google.cloud import translate_v2 as translate
from .Message import MessageFromClient, MessageToClient
import traceback


def translate_text(message: MessageFromClient | MessageToClient, retry=False) -> (MessageFromClient | MessageToClient, str):
    """
    Translates an incoming message into the language specified in the message.language field.
    If an exception occurs, it retries once more.

    :param message: Incoming message in original language
    :param retry: Indicates if this is a retry attempt
    :return: Tuple of (translated message, detected source language or "unknown" on error)
    """
    try:
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "../../credentials.json"
        translate_client = translate.Client()
        message_str = message.message
        target = message.language

        #message.language funktioniert irgendwie nicht ganz

        print("message language:  "+message.language)
        if isinstance(message_str, bytes):
            message_str = message_str.decode("utf-8")

        print("message: -> "+ message_str)
        print("target language: -> "+ target) # target bekommt er nciht?
        result = translate_client.translate(message_str, target_language='en')
        result["translatedText"] = html.unescape(result["translatedText"])
        message.message = result["translatedText"]
        return message, result["detectedSourceLanguage"]
    except Exception as e:
        print("An error occurred while translating the text:", e)
        print(traceback.format_exc())
        if not retry:
            print("Retrying...")
            return translate_text(message, retry=True)
        else:
            # Return the original message and "unknown" if the retry also fails
            return message, "unknown"