import unittest
from Server import ChatServerProtocol, ChatServerFactory


class TestChatServerProtocol(unittest.TestCase):
    """
    Tests for ChatServerProtocol of the Server module \n
    """
    def test_onConnect(self):
        """
        This method tests the onConnect-method\n
        """
        self.assertEqual(True, False)  # add assertion here

    def test_onOpen(self):
        """
        This method tests the onOpen-method\n
        """
        self.assertEqual(True, False)  # add assertion here

    def test_onMessage(self):
        """
        This method tests the onMessage-method\n
        """
        self.assertEqual(True, False)  # add assertion here

    def test_onClose(self):
        """
        This method tests the onClose-method\n
        """
        self.assertEqual(True, False)  # add assertion here

    def test_getUsernameAndLang(self):
        """
        This method tests the getUsernameAndLang-method\n
        """
        self.assertEqual(True, False)  # add assertion here

    def test_sendCurrentUsers(self):
        """
        This method tests the sendCurrentUsers-method\n
        """
        self.assertEqual(True, False)  # add assertion here


class TestChatServerFactory(unittest.TestCase):
    """
    Tests for ChatServerFactory of the Server module\n
    """
    def test_register(self):
        """
        This method tests the register-method\n
        """
        self.assertEqual(True, False)  # add assertion here

    def test_unregister(self):
        """
        This method tests the unregister-method\n
        """
        self.assertEqual(True, False)  # add assertion here

    def test_broadcast(self):
        """
        This method tests the broadcast-method\n
        """
        self.assertEqual(True, False)  # add assertion her


if __name__ == '__main__':
    unittest.main()
