import unittest
from ServerFuncs.Translator import translate_text
from ServerFuncs.Message import MessageFromClient, MessageToClient


class TestTranslator(unittest.TestCase):
    """
    Tests for the Translator module
    """
    def test_translate(self):
        """
        This method tests the translate-method\n
        """
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


if __name__ == '__main__':
    unittest.main()
