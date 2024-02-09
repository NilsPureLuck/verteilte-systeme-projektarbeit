import unittest
from Backend.Main import MessageToClient
from Backend.Main.ChatGPT import listenToMessages, create_chatbot, checkSentiment


class MyTestCase(unittest.TestCase):
    def test_checkSentiment(self):
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
        message1 = MessageToClient(username="Testuser", message="Testmessage",
                                   language="en", timestamp="00:00:00", sentiment="-1")
        message2 = MessageToClient(username="Testuser", message="Testmessage",
                                   language="en", timestamp="00:00:00", sentiment="-0.5")
        message3 = MessageToClient(username="Testuser", message="Testmessage",
                                   language="en", timestamp="00:00:00", sentiment="-0.0")
        message_list = [message1, message2, message3]

        self.assertEqual(listenToMessages(message_list), None)

        message3.message = "alexa, wieviel ist 2+2"

        self.assertEqual(listenToMessages(message_list).username, "Alexa")

    def test_createChatBot(self):
        message1 = MessageToClient(username="Testuser", message="Testmessage",
                                   language="en", timestamp="00:00:00", sentiment="-1")
        message2 = MessageToClient(username="Testuser", message="Testmessage",
                                   language="en", timestamp="00:00:00", sentiment="-0.5")
        message3 = MessageToClient(username="Testuser", message="alexa, wieviel ist 2+2",
                                   language="en", timestamp="00:00:00", sentiment="-0.0")
        message_list = [message1, message2, message3]

        self.assertEqual(listenToMessages(message_list).username, "Alexa")


if __name__ == '__main__':
    unittest.main()
