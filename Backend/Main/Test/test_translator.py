import os
import unittest
from google.cloud import translate_v2 as translate
from ServerFuncs.Translator import translate_text, initialize_translate_client
from ServerFuncs.Message import MessageFromClient, MessageToClient


class TestTranslator(unittest.TestCase):
    """
    Tests for the Translator module
    """

    def test_initialize_translate_client(self):
        """
        This method tests the initialize_translate_client-method\n
        """
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "../../credentials.json"
        expected_translate_client = translate.Client()

        self.assertEqual(initialize_translate_client().__dict__["target_language"],
                         expected_translate_client.__dict__["target_language"])

    def test_translate(self):
        """
        This method tests the translate-method\n
        """
        # MessagFromClient as Input
        message_given = MessageFromClient(username="Matthias", message="Hallo ich bin ein Bär",
                                          language="EN", timestamp="15:43:33")
        message_expected = MessageFromClient(username="Matthias", message="Hello, I am a bear",
                                             language="EN", timestamp="15:43:33", sentiment=0.85434434)
        self.assertEqual(translate_text(message_given), (message_expected, 'de'))
        message_given.language = "ES"
        message_expected.language = "ES"
        message_expected.message = "hola soy un oso"
        self.assertEqual(translate_text(message_given), (message_expected, 'en'))

        # MessageToClient as Input
        message_given = MessageToClient(username="Matthias", message="Hallo ich bin ein Bär",
                                        language="EN", timestamp="15:43:33", sentiment=0.85434434)
        message_expected = MessageToClient(username="Matthias", message="Hello, I am a bear",
                                           language="EN", timestamp="15:43:33", sentiment=0.85434434)
        self.assertEqual(translate_text(message_given), (message_expected, 'de'))

        # Check Exception mechanism by entering an empty language
        message_given = MessageToClient(username="Matthias", message="Hallo ich bin ein Bär",
                                        language="", timestamp="15:43:33", sentiment=0.85434434)
        message_expected = MessageToClient(username="Matthias", message="Hallo ich bin ein Bär",
                                        language="", timestamp="15:43:33", sentiment=0.85434434)
        self.assertEqual(translate_text(message_given), (message_expected, 'unknown'))


if __name__ == '__main__':
    unittest.main()
