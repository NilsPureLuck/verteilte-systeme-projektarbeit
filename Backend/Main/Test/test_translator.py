import unittest
from ServerFuncs.Message import MessageFromClient, MessageToClient
from ServerFuncs.Translator import translate_text


class TestTranslator(unittest.TestCase):
    """
    Tests for the Translator module
    """
    # Methode to test the translation process. Checks on the correct translation of the given message
    def test_translate(self):
        """
        This method tests the translate-method\n
        """
        # MessageFromClient as Input
        message_given = MessageFromClient(username="Matthias", message="Hallo ich bin ein Bär",
                                          language="EN", timestamp="15:43:33")
        message_expected = MessageFromClient(username="Matthias", message="Hello, I am a bear",
                                             language="EN", timestamp="15:43:33", sentiment=0.85434434)
        self.assertEqual(translate_text(message_given), message_expected)
        message_given.language = "ES"
        message_expected.language = "ES"
        message_expected.message = "hola soy un oso"
        self.assertEqual(translate_text(message_given), message_expected)
        # MessageToClient as Input
        message_given = MessageToClient(username="Matthias", message="Hallo ich bin ein Bär",
                                        language="EN", timestamp="15:43:33", sentiment=0.85434434)
        message_expected = MessageToClient(username="Matthias", message="Hello, I am a bear",
                                           language="EN", timestamp="15:43:33", sentiment=0.85434434)
        self.assertEqual(translate_text(message_given), message_expected)
