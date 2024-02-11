# Virtual Meet: Ein polyglotter Chat mit Sentiment-Analyse
### Willkommen bei Virtual Meet, einem innovativen Projekt aus dem Modul "Verteilte Systeme". Unser Ziel war es, ein Mashup zu kreieren, das nicht nur eine plattformübergreifende Kommunikation ermöglicht, sondern auch durch die Integration eines intelligenten Chatbots und Sentiment-Analysen ein einzigartiges Chaterlebnis schafft.

## Funktionen
 Polyglotter Chat: Ermöglicht Benutzern, in ihrer bevorzugten Sprache zu kommunizieren, während Nachrichten automatisch für alle übersetzt werden.
 Intelligenter Chatbot: Basierend auf OpenAI's Large Language Model, kann unser Bot Fragen beantworten, an Gesprächen teilnehmen und Informationen bereitstellen.
 Sentiment-Analyse: Erfasst die allgemeine Stimmung innerhalb des Chats und stellt diese den Benutzern dar.
## Voraussetzungen: Bevor Sie beginnen, stellen Sie sicher, dass Sie die folgenden API-Schlüssel bereit haben:

OpenAI-API-Key für den Chatbot. Erhältlich unter OpenAI API Keys.
Google Cloud Translate API-Key für die Übersetzung. Erhältlich unter Google Cloud Translate.
Twinword API-Key für die Sentiment-Analyse. Erhältlich unter Twinword Sentiment Analysis API.
## Setup
Konfiguration der Umgebungsvariablen:

Packen Sie Ihre OpenAI-API und Twinword-API Keys in eine .env Datei im Hauptordner.
Legen Sie die credentials.json Datei für Google Cloud Translation ebenfalls in den Hauptordner.

### Installation der Abhängigkeiten:
Führen Sie im Hauptordner folgenden Befehl aus:
pip install -r requirements.txt
Starten des Servers:
python Server.py

## Schnellstartanleitung
Erste Schritte mit Virtual Meet
Nutzernamen und Sprache wählen: Wählen Sie zu Beginn einen Nutzernamen und Ihre bevorzugte Sprache. Vergessen Sie nicht, auf „Speichern“ zu drücken.
Nachricht senden: Geben Sie Ihren Text in das Textfeld ein und klicken Sie auf „Senden“.
Chatbot einbeziehen: Um den Chatbot einzubeziehen, erwähnen Sie ihn einfach mit „botify“ gefolgt von Ihrer Frage oder Nachricht.
Aktive Nutzer: Auf der linken Seite können Sie sehen, wer aktuell online ist und welche Sprache eingestellt wurde.
Stimmungsanzeige: Jede Nachricht wird mit einem Indikator für die aktuelle Stimmung im Chat versehen, der automatisch berechnet wird.
Wir wünschen Ihnen viel Spaß bei der Nutzung von Virtual Meet und freuen uns auf Ihr Feedback!
