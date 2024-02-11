import json
import traceback
import logging
import os
from datetime import datetime
from twisted.internet import reactor
from autobahn.twisted.websocket import WebSocketServerFactory, WebSocketServerProtocol
from ServerFuncs.Message import MessageFromClient
from ServerFuncs.Translator import translate_text
from ServerFuncs.ChatHelper import listenToMessages
from ServerFuncs.Sentiment import sentiment_analysis


class ChatServerProtocol(WebSocketServerProtocol):
    """
    WebSocket Server\n
    """
    chatHistory = []

    def onConnect(self, request):
        """
        This method connects a client to the server\n
        :param request: incoming request from the client\n
        """
        self.language = None
        self.username = None

    def onOpen(self):
        """
        This method registers a new client when the connection is openned\n
        """
        self.factory.register(self)
        logging.info(f"Client connected: {self.peer}")

    def onMessage(self, payload, isBinary):
        """
        This method receives a message from a client, calls translation, sentiment analysis,
        chatbot and distributes it among the chat participants\n
        :param payload: incoming message from the client\n
        :param isBinary: Boolean indicating whether a message is binary or not\n
        :raise HTTPStatus: 400 Bad Request if the incoming message is malformed\n
        """
        try:
            if not isBinary:
                try:
                    message = payload.decode("utf8")
                    message = json.loads(message)
                    print(f"message received: {message}")
                    logging.info(f"message received: {message}")
                    message = MessageFromClient.model_validate(message)

                    # check if user.language or user.username is assigned for client, if not assign them and send current users
                    if self.language is None or self.username is None:
                        self.language = message.language.lower()
                        self.username = message.username
                        self.factory.sendCurrentUsers()

                    if message.language != "en":
                        message.language = "en"

                    message_copy = message.message

                    # translate message to english and calculate the sentiment
                    message, detectedlang = translate_text(message)

                    message = sentiment_analysis(message)

                    self.chatHistory.append(message)

                    while len(self.chatHistory) > 5:
                        message_old = self.chatHistory.pop(0)
                        print(
                            f"old message '{message_old.message} removed from chat history"
                        )

                    message.orgmessage = message_copy
                    message.detectedlang = detectedlang

                    self.factory.broadcast(message, self)

                    chat_response = listenToMessages(self.chatHistory)

                    if chat_response is not None:
                        self.chatHistory.append(chat_response)

                        self.factory.broadcast(chat_response, self)
                        print(f"Message '{chat_response.message}' broadcasted")

                        while len(self.chatHistory) > 5:
                            message_old = self.chatHistory.pop(0)

                except Exception:
                    print(traceback.format_exc())
                    self.sendMessage(
                        "wrong request parameter send Request as Json with fields "
                        + json.dumps(
                            {"username", "message", "language", "timestamp"}
                        ).encode("utf-8")
                    )
                    raise Exception(
                        status=400,
                        reason="wrong request parameter send Request as Json with fields "
                        + json.dumps({"username", "message", "language", "timestamp"}),
                    )

        except Exception:
            print(traceback.format_exc())
            logging.error(traceback.format_exc())

    def onClose(self, wasClean, code, reason):
        """
        This method is called when the websocket connection closes\n
        :param wasClean: boolean whether the connection was closed cleanly\n
        :param code: status code of the connection close\n
        :param reason: cause for connection close\n
        """
        message = f"Client disconnected: {self.peer}    Closing details: {reason}, was clean: {wasClean}, code: {code}"
        print(message)
        logging.info(message)
        self.factory.unregister(self)


class ChatServerFactory(WebSocketServerFactory):
    """
    Factory for WebSocket Servers
    """

    def __init__(self, url):
        super().__init__(url)
        self.clients = []
        self.maxConnections = 50

    def getUsernameAndLang(self):
        """
        This methods compiles a list of all usernames and languages participating in the chat\n
        :return list: List of clients and their set language\n
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
        This method sends a list of all clients currently registered to the server\n
        """
        number_of_clients = len(self.clients)
        client_list = self.getUsernameAndLang()
        message = json.dumps({"clientsOnline": client_list,"numOfClients": number_of_clients})
        logging.info(f"Active users message send: {message}")
        
        for client in self.clients:
            try:
                if not (client.username is None or client.language is None):
                    client.sendMessage(message.encode("utf-8"))
            except:
                logging.error(traceback.format_exc())
                print(traceback.format_exc())

    def register(self, client):
        """
        This method adds a client to the list of chat participants\n
        :param client: client to be registered\n
        """
        if client not in self.clients:
            print(f"Client registered: {client.peer}")
            self.clients.append(client)
            logging.info(f"Client registered: {client.peer}")

    def unregister(self, client):
        """
        This method removes the client from the list of chat participants\n
        :param client: client to be removed\n
        """
        if client in self.clients:
            print(f"Client unregister: {client.peer}")
            self.clients.remove(client)
            logging.info(f"Client unregisterd: {client.peer}")
        if len(self.clients) > 0:
            self.sendCurrentUsers()

    def broadcast(self, message, sender):
        """
        This method broadcasts the message to all clients in the chat\n
        :param message: The message to broadcast\n
        :param sender: Sender client of the message\n
        """
        print(f"message for broadcast {message}")
        for client in self.clients:
            try:
                if not (client.username is None or client.language is None):
                    if client.language == message.detectedlang:
                        message.message = str(message.orgmessage)
                        jsonmassage = json.dumps(
                            message.model_dump(exclude={"detectedlang", "orgmessage"}),
                            ensure_ascii=True,
                        )
                        client.sendMessage(jsonmassage.encode("utf-8"))
                        print(f"Send Message {jsonmassage} to {client.peer}")
                        logging.info(f"Send Message {jsonmassage} to {client.peer}")
                    else:
                        print(f"USERLANG: {client.language} {type(client.language)}")
                        message.language = str(client.language)
                        print(f"user alnguage : {message.language}")
                        message, _ = translate_text(message)
                        jsonmassage = json.dumps(
                            message.model_dump(exclude={"detectedlang", "orgmessage"}),
                            ensure_ascii=True,
                        )
                        client.sendMessage(jsonmassage.encode("utf-8"))
                        print(f"Send Message {jsonmassage} to {client.peer}")
                        logging.info(f"Send Message {jsonmassage} to {client.peer}")

            except Exception:
                logging.error(traceback.format_exc())


if __name__ == "__main__":
    log_dir = "./LogFiles"
    log_filename = str(
        "logfile" + datetime.today().strftime("-%Y-%m-%d-%H-%M") + ".log"
    )
    log_path = os.path.join(log_dir, log_filename)
    # create log file if not exsist
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # Konfiguration des Loggings
    logging.basicConfig(
        filename=log_path,
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )

    factory = ChatServerFactory("ws://localhost:9000")
    factory.protocol = ChatServerProtocol
    reactor.listenTCP(9000, factory)
    print("WebSocket-Server gestartet auf Port 9000.")
    reactor.run()
