import os
import unittest
from dotenv import load_dotenv
from ServerFuncs.Sentiment import sentiment_analysis, load_api_config, get_sentiment_score
from ServerFuncs.Message import MessageFromClient, MessageToClient


class TestSentiment(unittest.TestCase):
    """
    Tests for the Sentiment module
    """

    def test_load_api_config(self):
        load_dotenv()
        config_expected = {
            "url": os.environ.get("SENTIMENT_ANALYSIS_URL"),
            "headers": {
                "X-RapidAPI-Key": os.environ.get("TWINWORD_KEY"),
                "X-RapidAPI-Host": os.environ.get("TWINWORD_HOST")
            }
        }
        self.assertEqual(load_api_config(), config_expected)

    def test_get_sentiment_score(self):
        load_dotenv()
        config = {
            "url": os.environ.get("SENTIMENT_ANALYSIS_URL"),
            "headers": {
                "X-RapidAPI-Key": os.environ.get("TWINWORD_KEY"),
                "X-RapidAPI-Host": os.environ.get("TWINWORD_HOST")
            }
        }
        message_text_given = "I like that"

        score_expected = 0.85434434
        self.assertEqual(get_sentiment_score(message_text_given, config), score_expected)

    def test_sentiment_analysis(self):
        """
        This method tests the sentiment_analysis-method\n
        """
        # Check positive Sentiment
        message_given = MessageFromClient(username="Matthias", message="I like that",
                                          language="EN", timestamp="15:43:33")
        message_expected = MessageToClient(username="Matthias", message="I like that",
                                           language="EN", timestamp="15:43:33", sentiment=0.85434434)
        self.assertEqual(sentiment_analysis(message_given), message_expected)

        # Check negative Sentiment
        message_given.message = "I do not like that"
        message_expected.message = "I do not like that"
        message_expected.sentiment = -0.73967217
        self.assertEqual(sentiment_analysis(message_given), message_expected)

        # Check neutral Sentiment
        message_given.message = "Ok"
        message_expected.message = "Ok"
        message_expected.sentiment = 0
        self.assertEqual(sentiment_analysis(message_given), message_expected)
