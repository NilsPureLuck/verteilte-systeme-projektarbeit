import unittest
from ServerFuncs.Message import MessageToClient
from ServerFuncs.ChatHelper import *


class TestChatHelper(unittest.TestCase):
    """
    Tests for the Chat Helper module
    """

    def test_listenToMessages(self):
        """
        This method tests the listenToMessages-method\n
        """

        chatHistory_given =[]
        expected_return = None

        self.assertEqual(listenToMessages(chatHistory_given), expected_return)

        message1 = MessageToClient(username="Testuser", message="Testmessage",
                                   language="en", timestamp="00:00:00", sentiment="-1")
        message2 = MessageToClient(username="Testuser", message="Testmessage",
                                   language="en", timestamp="00:00:00", sentiment="-0.5")
        message3 = MessageToClient(username="Testuser", message="Testmessage",
                                   language="en", timestamp="00:00:00", sentiment="-0.0")
        message_list = [message1, message2, message3]

        self.assertEqual(listenToMessages(message_list), None)

        message3.message = "botify, wieviel ist 2+2"

        self.assertEqual(listenToMessages(message_list).username, "Botify")



    def test_is_message_addressing_bot(self):
        """
        This method tests the is_message_addressing_bot-method\n
        """
        message_given = "Testmessage"
        self.assertEqual(is_message_addressing_bot(message_given), False)

        message_given = "botify, wieviel ist 2+2"
        self.assertEqual(is_message_addressing_bot(message_given), True)

        message_given = "Bitify, wieviel ist 2+2"
        self.assertEqual(is_message_addressing_bot(message_given), True)

    def test_createChatBot(self):
        """
        This method tests the createChatBot-method\n
        """
        message1 = MessageToClient(username="Testuser", message="Testmessage",
                                   language="en", timestamp="00:00:00", sentiment="-1")
        message2 = MessageToClient(username="Testuser", message="Testmessage",
                                   language="en", timestamp="00:00:00", sentiment="-0.5")
        message3 = MessageToClient(username="Testuser", message="botify, wieviel ist 2+2",
                                   language="en", timestamp="00:00:00", sentiment="-0.0")
        message_list = [message1, message2, message3]

        self.assertEqual(create_chatbot(message_list).username, "Botify")

        load_dotenv()

        self.assertEqual(create_chatbot(message_list).username, "Botify")

    def test_prepare_messages(self):
        message1 = MessageToClient(username="Testuser", message="Testmessage",
                                   language="en", timestamp="00:00:00", sentiment="-1")
        message2 = MessageToClient(username="Testuser", message="Testmessage",
                                   language="en", timestamp="00:00:00", sentiment="-0.5")
        message3 = MessageToClient(username="Testuser", message="Testmessage",
                                   language="en", timestamp="00:00:00", sentiment="-0.0")
        sentiment_given = -0.5

        chatHistory_given = [message1, message2, message3]
        messages_expected = [{'role': 'user', 'content': 'Testmessage'},
                             {'role': 'user', 'content': 'Testmessage'},
                             {'role': 'user', 'content': 'Testmessage'},
                             {'role': 'system', 'content': 'Deine aktuelle Stimmung liegt bei: -0.5'}]
        self.assertEqual(prepare_messages(chatHistory_given, sentiment_given), messages_expected)

    def test_calculate_temperature(self):
        sentiment_given = 0.5
        temperature_expected = 0.6500000000000001
        self.assertEqual(calculate_temperature(sentiment_given), temperature_expected)

    def test_build_message_object(self):
        response_given = "Test"
        sentiment_given = 0.0
        message_expected = MessageToClient(username="botify", message="Test", language="EN",
                                           timestamp=datetime.now().strftime("%H:%M:%S"), sentiment=0.0)
        self.assertEqual(build_message_object(response_given, sentiment_given), message_expected)

    def test_handle_error_on_retry_failure(self):
        message_expected = MessageToClient(username="Botify", message="I'm sorry, I'm not able to answer right now.",
                                           language="EN", timestamp=datetime.now().strftime("%H:%M:%S"), sentiment=0.0)
        self.assertEqual(handle_error_on_retry_failure(), message_expected)

    def test_check_sentiment(self):
        """
        This method tests the checkSentiment-method\n
        """

        chatHistory_given =[]
        sentiment_expected = 0.0
        self.assertEqual(check_sentiment(chatHistory_given), sentiment_expected)

        message1 = MessageToClient(username="Testuser", message="Testmessage",
                                   language="en", timestamp="00:00:00", sentiment="-1")
        message2 = MessageToClient(username="Testuser", message="Testmessage",
                                   language="en", timestamp="00:00:00", sentiment="-0.5")
        message3 = MessageToClient(username="Testuser", message="Testmessage",
                                   language="en", timestamp="00:00:00", sentiment="-0.0")
        message_list = [message1, message2, message3]

        sentiment_expected = -0.5

        self.assertEqual(check_sentiment(message_list), sentiment_expected)



if __name__ == '__main__':
    unittest.main()
