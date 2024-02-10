"""
Server Module
-------------
"""

import json
import traceback
from twisted.internet import reactor
from autobahn.twisted.websocket import WebSocketServerFactory, WebSocketServerProtocol
from http import HTTPStatus
from ServerFuncs.Message import MessageFromClient
from ServerFuncs.Translator import translate_text
from ServerFuncs.ChatHelper import listenToMessages
from ServerFuncs.Sentiment import sentiment_analysis


class ChatServerProtocol(WebSocketServerProtocol):
    """
    WebSocket Server
    """

    chatHistory = []

    def onConnect(self, request):
        """
        This method connects a client to the server
        :param request: incoming request from the client
        """
        self.language = None
        self.username = None
        print(f"Client verbunden: {request.peer}")

    def onOpen(self):
        """
        This method registers a new client when the connection is openned
        """
        self.factory.register(self)

    def onMessage(self, payload, isBinary):
        """
        This method receives a message from a client, calls translation, sentiment analysis, chatbot and distributes it
        among the chat participants
        :param payload: incoming message from the client
        :param isBinary: Boolean indicating whether a message is binary or not
        :raise HTTPStatus: 400 Bad Request if the incoming message is malformed
        """
        try:
            if not isBinary:
                try:
                    message = payload.decode("utf8")
                    message = json.loads(message)
                    print(f"message received: {message}")
                    message = MessageFromClient.model_validate(message)

                    if self.language is None or self.username is None:
                        self.language = message.language.lower()
                        self.username = message.username
                        print("set user language to", self.language)
                        print("linked user with username", self.username)
                        self.factory.sendCurrentUsers()

                    if message.language != "en":
                        message.language = "en"
                        
                    message_copy = message.message

                    message, detectedlang = translate_text(message)
                    print(f"translated message for sentiment to: {message.message}")
                    message = sentiment_analysis(message)
                    print(f"sentiment generated: {message.sentiment}")

                    
                    self.chatHistory.append(message)
                    print(f"Message '{message.message}' added to chat history")

                    while len(self.chatHistory) > 5:
                        message_old = self.chatHistory.pop(0)
                        print(
                            f"old message '{message_old.message} removed from chat history"
                        )

                    message.orgmessage = message_copy
                    message.detectedlang = detectedlang
                    
                    print(f"Message with old message and detected Lang : {message}")
                    self.factory.broadcast(message, self)
                    print(f"Message '{message.message}' broadcasted")

                    chat_response = listenToMessages(self.chatHistory)
                    print(chat_response)
                    if chat_response is not None:
                        self.chatHistory.append(chat_response)
                        print(
                            f"Message '{chat_response.message}' added to chat history"
                        )
                        self.factory.broadcast(chat_response, self)
                        print(f"Message '{chat_response.message}' broadcasted")

                        while len(self.chatHistory) > 5:
                            message_old = self.chatHistory.pop(0)
                            print(
                                f"old message '{message_old.message} removed from chat history"
                            )
                except:
                    print(traceback.format_exc())

        except Exception:
            print(traceback.format_exc())
            raise HTTPStatus(status=400, reason="wrong parameter in request")

    def onClose(self, wasClean, code, reason):
        print(
            f"WebSocket-Verbindung geschlossen: {reason}, was clean: {wasClean}, code: {code}"
        )
        self.factory.unregister(self)


class ChatServerFactory(WebSocketServerFactory):
    """
    Factory for WebSocket Servers
    """

    def __init__(self, url):
        super().__init__(url)
        self.clients = []

    def getUsernameAndLang(self):
        """
        This methods compiles a list of all usernames and languages participating in the chat
        :return: List of clients and their set language
        """
        client_list = []
        for client in self.clients:
            if not (client.username is None or client.language is None):
                client_list.append(
                    {"username": client.username, "language": client.language}
                )
        return client_list

    def sendCurrentUsers(self):
        """
        This method sends a list of all clients currently registered to the server
        """
        number_of_clients = len(self.clients)
        client_list = self.getUsernameAndLang()
        print(client_list)
        for client in self.clients:
            try:
                if not (client.username is None or client.language is None):
                    message = json.dumps(
                        {
                            "clientsOnline": client_list,
                            "numOfClients": number_of_clients,
                        }
                    )
                    client.sendMessage(message.encode("utf-8"))
            except:
                print(traceback.format_exc())

    def register(self, client):
        """
        This method adds a client to the list of chat participants
        :param client: client to be registered
        """
        if client not in self.clients:
            print(f"Client {client.peer} registriert.")
            self.clients.append(client)

    def unregister(self, client):
        """
        This method removes the client from the list of chat participants
        :param client: client to be removed
        """
        if client in self.clients:
            print(f"Client {client.peer} registriert.")
            self.clients.remove(client)
        if len(self.clients):
            self.sendCurrentUsers()

    def broadcast(self, message, sender):
        print(f"message for broadcast {message}")
        """
        This method broadcasts the message to all clients in the chat
        :param message: The message to broadcast
        :param sender: Sender client of the message
        """
        
        for client in self.clients:
            if client.language == message.detectedlang:
                message.message = message.orgmessage
                jsonmassage = json.dumps(message.model_dump(exclude={"detectedlang", "orgmessage"}), ensure_ascii=True)
                client.sendMessage(jsonmassage.encode("utf-8"))    
            else:
                message.language = str(client.language)
                message, _ = translate_text(message)
                print(f"Message translated for {client.username} to {message}")
                jsonmassage = json.dumps(message.model_dump(exclude={"detectedlang", "orgmessage"}), ensure_ascii=True)
                client.sendMessage(jsonmassage.encode("utf-8"))    


if __name__ == "__main__":
    factory = ChatServerFactory("ws://localhost:9000")
    factory.protocol = ChatServerProtocol
    reactor.listenTCP(9000, factory)
    print("WebSocket-Server gestartet auf Port 9000.")
    reactor.run()
