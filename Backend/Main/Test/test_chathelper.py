import unittest
from ServerFuncs.Message import MessageToClient
from ServerFuncs.ChatHelper import listenToMessages, create_chatbot, checkSentiment, is_message_addressing_bot


class TestChatHelper(unittest.TestCase):
    """
    Tests for the Chat Helper module
    """
    def test_checkSentiment(self):
        """
        This method tests the checkSentiment-method\n
        """
        message1 = MessageToClient(username="Testuser", message="Testmessage",
                                   language="en", timestamp="00:00:00", sentiment="-1")
        message2 = MessageToClient(username="Testuser", message="Testmessage",
                                   language="en", timestamp="00:00:00", sentiment="-0.5")
        message3 = MessageToClient(username="Testuser", message="Testmessage",
                                   language="en", timestamp="00:00:00", sentiment="-0.0")
        message_list = [message1, message2, message3]

        sentiment_expected = -0.5

        self.assertEqual(checkSentiment(message_list), sentiment_expected)

    def test_listenToMessages(self):
        """
        This method tests the listenToMessages-method\n
        """
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


if __name__ == '__main__':
    unittest.main()
