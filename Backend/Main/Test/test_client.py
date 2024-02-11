from twisted.internet import reactor
from autobahn.twisted.websocket import WebSocketClientProtocol, WebSocketClientFactory
import json

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

async def startClient():
    factory = WebSocketClientFactory("ws://localhost")
    factory.protocol = MyClientProtocol

    reactor.connectTCP("localhost" , 9000, factory)
    reactor.run()
            
if __name__ == '__main__':
    factory = WebSocketClientFactory("ws://localhost")
    factory.protocol = MyClientProtocol

    reactor.connectTCP("localhost" , 9000, factory)
    reactor.run()
