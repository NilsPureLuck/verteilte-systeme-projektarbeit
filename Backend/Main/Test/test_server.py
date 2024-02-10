import unittest
from Server import ChatServerProtocol, ChatServerFactory


class MyTestCase(unittest.TestCase):
    def test_onConnect(self):
        self.assertEqual(True, False)  # add assertion here

    def test_onOpen(self):
        self.assertEqual(True, False)  # add assertion here

    def test_onMessage(self):
        self.assertEqual(True, False)  # add assertion here

    def test_onClose(self):
        self.assertEqual(True, False)  # add assertion here

    def test_getUsernameAndLang(self):
        self.assertEqual(True, False)  # add assertion here

    def test_sendCurrentUsers(self):
        self.assertEqual(True, False)  # add assertion here

    def test_register(self):
        self.assertEqual(True, False)  # add assertion here

    def test_unregister(self):
        self.assertEqual(True, False)  # add assertion here

    def test_broadcast(self):
        self.assertEqual(True, False)  # add assertion her


if __name__ == '__main__':
    unittest.main()
