import unittest
from Server import ChatServerProtocol, ChatServerFactory, startServer
from autobahn.twisted.websocket import WebSocketServerFactory, WebSocketServerProtocol
from .test_client import startClient, WebSocketClientFactory



class TestChatServerProtocol(unittest.TestCase):
    """
    Tests for ChatServerProtocol of the Server module \n
    """
    
    
    '''
    def test_server(self):
        
        #client = startClient()
        #server = startServer()    
        
        #self.assertIsInstance(client, WebSocketClientFactory)
        #self.assertIsInstance(startServer(), ChatServerFactory)
        
    
   
    class ChatServerProtocol(WebSocketServerProtocol):
    
        
       
        def test_onConnect(self):
            """
            This method tests the onConnect-method\n
            """
           
            self.language = None
            self.username = None
            print(f"Client verbunden: {request.peer}")
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
        '''


class TestChatServerFactory(unittest.TestCase):
    """
    Tests for ChatServerFactory of the Server module\n
    """
    server = startServer()

    class MyClientProtocol(WebSocketClientProtocol):

        def onConnect(self, response):
            print("Connected to Server: {0}".format(response.peer))
            

        def onOpen(self):
            print("WebSocket connection open.")
            #self.sendUserInput()
            self.sendPredefinedInput({"username":"test", "message":"test message an den Server", "language":"de", "timestamp":"15:13:23"})
                    
        def sendUserInput(self):
            while True:
                ask = "Enter your message: "
                data = input(ask)
                message = json.dumps(str("{\"username\":\"test\", \"message\":\"" + data + "\", \"language\":\"de\", \"timestamp\":\"15:13:23\"}"))
                self.sendMessage(json.dumps(message).encode("utf-8"))

        def sendPredefinedInput(self, message):
            message = json.dumps(message)
            print(message)
            self.sendMessage(message.encode("utf-8"))

        def onClose(self, wasClean, code, reason):
            print("WebSocket connection closed: {0}".format(reason))
            
        def onMessage(self, payload, isBinary):
            try:
                if not isBinary:
                    message = payload.decode("utf8")
                    print(f"Message from Server {message}")
                
                else:
                    print("Message is Binary")    
                
            except:
                print("Error")
    
    def test_register():
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
