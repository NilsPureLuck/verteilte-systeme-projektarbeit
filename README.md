# Virtual Meet: Ein polyglotter Chat mit Sentiment-Analyse
### Willkommen bei Virtual Meet, einem innovativen Projekt aus dem Modul "Verteilte Systeme". Unser Ziel war es, ein Mashup zu kreieren, das nicht nur eine plattformübergreifende Kommunikation ermöglicht, sondern auch durch die Integration eines intelligenten Chatbots und Sentiment-Analysen ein einzigartiges Chaterlebnis schafft.

## Funktionen
 Polyglotter Chat: Ermöglicht Benutzern, in ihrer bevorzugten Sprache zu kommunizieren, während Nachrichten automatisch für alle übersetzt werden.
 
 Intelligenter Chatbot: Basierend auf OpenAI's Large Language Model, kann unser Bot Fragen beantworten, an Gesprächen teilnehmen und Informationen bereitstellen.
 
 Sentiment-Analyse: Erfasst die allgemeine Stimmung innerhalb des Chats und stellt diese den Benutzern dar.

## Voraussetzungen:
Für die Durchführung auf einem lokalen Rechner benötigen Sie die Keys und Credentials für den Zugriff auf die APIs. Diese befinden sich in den Dateien .env und credentials.json

## Setup
### Konfiguration der Umgebungsvariablen:
Die .env und die credentials.json Dateien müssen im Rootverzeichnis abgelegt werden.

### Installation der Abhängigkeiten:
Führen Sie im Hauptordner folgenden Befehl aus:
```pip install -r requirements.txt```

### Starten des Servers:
Starten Sie die Anwendung mit:
```python Server.py```

## Schnellstartanleitung
### Erste Schritte mit Virtual Meet
1. Nutzernamen und Sprache wählen: Wählen Sie zu Beginn einen Nutzernamen und Ihre bevorzugte Sprache. Vergessen Sie nicht, auf „Speichern“ zu drücken.
2. Nachricht senden: Geben Sie Ihren Text in das Textfeld ein und klicken Sie auf „Senden“.
3. Chatbot einbeziehen: Um den Chatbot einzubeziehen, erwähnen Sie ihn einfach mit „botify“ gefolgt von Ihrer Frage oder Nachricht.
4. Aktive Nutzer: Auf der linken Seite können Sie sehen, wer aktuell online ist und welche Sprache eingestellt wurde.
5. Stimmungsanzeige: Jede Nachricht wird mit einem Indikator für die aktuelle Stimmung im Chat versehen, der automatisch berechnet wird.

## Tests
### Coverage
Die Ergebnisse der Testcoverage können unter https://virtualmeet.social/docs/coverage eingesehen werden. Für die Unittests wurden die Module test_chathelper, test_sentiment und test_translator erstellt. Für eine erneute Durchführung der Unittests mit Testcoverage sind folgende Schritte zu durchzuführen:
1. Installation der Module unittest und coverage mit den Befehlen
   ```pip install unittest``` und
   ```pip install coverage```
2. In das Verzeichnis /Backend/Main wechseln
3. Erst folgenden Befehl ausführen:
   ```python -m coverage run -m unittest```
4. Anschließend folgenden Befehl ausführen:
   ```python -m coverage html```
5. Im Verzeichnis /Backend/Main müsste nun ein neuer Ordner names htmlcov auftauchen
6. Im htmlcov Ordner die Datei index.html ausführen
   
### Einzelne Unittests
Alternativ zu Unittests mit Coverage können auch einzelne Unittests für die Funktionen durchgeführt werden. Hierfür können ebenfalls die Module test_chathelper, test_sentiment und test_translator verwendet werden. Zur Durchführung müssen folgende Schritte beachtet werden:

1. Alle imports aus dem package "ServerFuncs" müssen einen Punkt vorangestellt haben, ansonsten schlagen die Imports fehl (Bsp.: aus "from ServerFuncs.Translator import..." muss "from .ServerFuncs.Translator import..." werden)
2. Testmodul ausführen 

Da bei den Testfällen auch Fehlerfälle geprüft werden, tauchen während der Unittests unter anderem auch Fehlermeldungen der getesteten Module auf.

### Wir wünschen Ihnen viel Spaß bei der Nutzung von Virtual Meet und freuen uns auf Ihr Feedback! 😊 
