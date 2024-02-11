//global variables
let savedNickname;
let chosenlanguage = "en";
let socket;

/**
 * This method sends the text, which has been input, to the server along with the necessary
 * information in the JSON format
 */
function buttonSendAction() {

    const inputWindow = document.getElementById("chatTextInput");
    let inputText = inputWindow.value;

    if(inputText === '') {
        alert("Please enter a message!")
    }else {
        inputWindow.value = "";

        //creating timestamp
        const now = new Date();

        let hour = now.getHours().toString().padStart(2, '0');
        let minute = now.getMinutes().toString().padStart(2, '0');
        let second = now.getSeconds().toString().padStart(2, '0');

        let timestamp = `${hour}:${minute}:${second}`;

        // creating the JSON String
        const chatMessageToServer = {
            username: savedNickname,
            message: inputText,
            timestamp: timestamp,
            language: chosenlanguage
        };
        let data = JSON.stringify(chatMessageToServer);

        // sending the json String to the Server
        socket.send(data);
    }
}

/**
 * This method is being executed when loading the page
 * It established the connection between a client and the server
 */
function establishConnection() {
    socket = new WebSocket("ws://localhost:9000");

    socket.addEventListener("message", (event) => {

        //Parsing of the received json message
        const receivedMessage = JSON.parse(event.data);
        console.log(receivedMessage);

        //Checks the users that are connected to the chat and added to the current user list
        if(receivedMessage.numOfClients) {
            const currentUsersList = document.getElementById("unorderedUserList");
            currentUsersList.innerHTML = '';

            for (const user in receivedMessage.clientsOnline) {
                const listItem = document.createElement("li");
                listItem.textContent = `${receivedMessage.clientsOnline[user].username}: ${receivedMessage.clientsOnline[user].language}`;
                currentUsersList.appendChild(listItem)
            }
        }
        else {

            //receiving the message and adding it to the chat window
            const chatTextArea = document.getElementById("chatTextArea");
            const atmosphere = receivedMessage.sentiment;
            let smiley = "\u{1F610}";
            if (atmosphere < -0.3) {
                smiley = "\u{1F622}";
            }
            else if (atmosphere > 0.3) {
                smiley = "\u{1F60A}";
            }

            const formatMessage = `(${receivedMessage.timestamp}) ${smiley}  ${receivedMessage.username}: ${receivedMessage.message} `;

            // Hinzufügen der formatierten Nachricht zum Chatfenster, mit Zeilenumbruch für jede neue Nachricht
            chatTextArea.value += (chatTextArea.value ? "\n" : "") + formatMessage;
            scrollToBottom();
        }
    });
}

/**
 * Declares the action that are taken after pressing the "Save" Button
 * It includes:
 */
function saveUserSettings() {

    const nicknameEingabe = document.getElementById("nicknameArea");

    if(nicknameEingabe.value === ''){
        alert("Please fill in a username.");
    }else{
      savedNickname = nicknameEingabe.value;
        nicknameEingabe.readOnly = true;
        nicknameEingabe.style.backgroundColor = "lightgrey";

        //disables the dropdown menu
        let dropdowns = document.querySelectorAll('.dropdown');
        dropdowns.forEach(function (dropdown){
            dropdown.classList.add('no-hover-dropdown');
        })

        document.getElementById("chatTextInput").focus();
    }
}

/**
 * This method declares which language the user selected
 */
function selectLanguage() {
    switch (document.getElementById("dropdownValue").value){
        case "1": chosenlanguage ="de";
        break;
        case "2": chosenlanguage ="en";
        break;
        case "3": chosenlanguage ="fr";
        break;
        case "4": chosenlanguage = "it";
        break;
        case "5": chosenlanguage = "es";
        break;
    }
    changeDisplayedFlag();
}

/**
 * This function changes the image, which is displayed in the dropdown menu of the language select button
 */
function changeDisplayedFlag(){
    let element = document.getElementById("chosenLanguageFlag");
    switch (chosenlanguage){
        case "de": element.src = "img/Flag_of_Germany.png"; break;
        case "en": element.src = "img/Flag_of_England.png"; break;
        case "fr": element.src = "img/Flag_of_France.png"; break;
        case "it": element.src = "img/Flag_of_Italy.png"; break;
        case "es": element.src = "img/Flag_of_Spain.png"; break;
    }
    changeLanguageOnTheSite();
}

/**
 * This method enables the scroll-bar on the right-side of the chat window
 */
function scrollToBottom() {
    const chatTextArea = document.getElementById("chatTextArea");
    chatTextArea.scrollTop = chatTextArea.scrollHeight;
}

/**
 * This method changes the language of every html element to the chosen language
 * It is also called once during the loading process of the page to minimize the content of the html file
 */
function changeLanguageOnTheSite(){

    let articleGuide = document.getElementById("guideArticle");
    let chatMessageInput = document.getElementById("chatTextInput");
    let usernameInput = document.getElementById("nicknameArea");
    let saveButton = document.getElementById("userSettingSaveButton");
    let sendButton = document.getElementById("sendButton");
    let userNameLabel = document.getElementById("userNameLabel");
    let languageLabel = document.getElementById("languageLabel");
    let userListLabel = document.getElementById("userListLabel");
    let chatWindow = document.getElementById("chatTextArea");
    let footerElement = document.getElementById("footerArea");

    switch (chosenlanguage){
        case "de":
            articleGuide.innerHTML =
                "<u>Getting Started with Virtual Meet</u><br>" +
                "Willkommen bei Virtual Meet! Hier ist eine schnelle Anleitung, um dir den Einstieg zu erleichtern:<br>" +
                "<br>" +
                "<b>1. Nutzernamen und Sprache auswählen</b><br>" +
                "Bevor du loslegst, wähle einen Nutzernamen und deine bevorzugte Sprache aus. Vergiss nicht auf „Speichern“ zu drücken<br>" +
                "<b>2. Senden einer Nachricht</b><br>" +
                "Um eine Nachricht zu senden, gebe einfach deinen Text in das Textfeld ein und klicke auf „Senden“. Deine Nachricht wird dann an alle anderen Chatteilnehmer gesendet.<br>" +
                "<b>3. Beteiligung des Chatbots an der Konversation</b><br>" +
                "Wenn du möchtest, dass der Chatbot sich an der Konversation beteiligt, erwähne einfach seinen Namen in deiner Nachricht. Unser Chatbot heißt „botify“. botify reagiert anschließend automatisch auf deine Nachricht.<br>" +
                "Zum Beispiel: „botify, wie ist aktuell die Stimmung im Chat?“<br>" +
                "<b>4. Aktive Nutzer</b><br>" +
                "Auf der linken Seite des Bildschirms findest du eine Liste aller aktiven User. Neben dem Nutzernamen wird auch die eingestellte Sprache angezeigt.<br>" +
                "<b>5. Anzeige der aktuellen Stimmung im Chat:</b><br>" +
                "Hinter jeder Nachricht siehst du einen Indikator, der die aktuelle Stimmung im Chat anzeigt. Dieser Indikator wird von ganz alleine berechnet. Du musst also nichts machen!<br>" +
                "<br>" +
                "Das war's! Du bist nun bereit, Virtual Meet zu nutzen und mit anderen Usern zu kommunizieren. <br>" +
                "Viel Spaß! 😊";
            chatMessageInput.placeholder = "Nachricht eingeben...";
            usernameInput.placeholder = "Benutzername eingeben..."
            chatWindow.placeholder = "Bitte geben Sie einen Benutzernamen ein, wählen Sie eine Sprache und senden Sie eine Nachricht, um den Chatroom zu betreten...";
            saveButton.textContent = "Sichern";
            sendButton.textContent = "Senden";
            userNameLabel.textContent = "Benutzername";
            languageLabel.textContent = "Sprache"
            userListLabel.textContent = "Aktive Benutzer";
            footerElement.innerHTML =
                "        <u>Nutzungsbedingungen </u><br>\n" +
                "        Durch die Nutzung dieses Chat-Tools stimmen Sie zu, dass Sie die folgenden Nutzungsbedingungen gelesen, verstanden und akzeptiert haben. Bitte lesen Sie sie sorgfältig durch:<br>\n" +
                "        Allgemeine Nutzung: Dieses Tool dient der Kommunikation und dem Informationsaustausch. Jede Nutzung zu illegalen Zwecken ist strengstens untersagt.<br>\n" +
                "        Haftungsausschluss: Die Betreiber des Chat-Tools übernehmen keine Haftung für Schäden, die durch die Nutzung dieses Tools entstehen. Die Nutzer kommunizieren auf eigene Gefahr.<br>\n" +
                "        Inhaltsverantwortung: Die Nutzer sind für die von ihnen geteilten Inhalte selbst verantwortlich. Illegale, schädliche oder rechtswidrige Inhalte sind verboten.<br>\n" +
                "        Datenschutz: Die Nutzer erkennen an, dass die Privatsphäre in einem Online-Chat nur bedingt geschützt werden kann. Persönliche Informationen sollten mit Vorsicht behandelt werden.<br>\n" +
                "        Änderungen der Nutzungsbedingungen: Die Betreiber behalten sich das Recht vor, diese Nutzungsbedingungen jederzeit ohne Vorankündigung zu ändern. Die fortgesetzte Nutzung des Tools nach solchen Änderungen gilt als Zustimmung zu den neuen Bedingungen.<br>\n" +
                "        Indem Sie dieses Tool nutzen, erklären Sie sich mit diesen Bedingungen einverstanden.<br>";
            break;
        case "en":
            articleGuide.innerHTML =
                "<u>Getting Started with Virtual Meet</u><br>" +
                "Welcome to Virtual Meet! Here's a quick guide to get you started:<br>" +
                "<br>" +
                "<b>1. Select username and language</b><br>" +
                "Before you get started, choose a username and your preferred language. Don't forget to press \"Save\".<br>" +
                "<b>2. Sending a message</b><br>" +
                "To send a message, simply enter your text in the text field and click Send. Your message will then be sent to all other chat participants.<br>" +
                "<b>3. Chatbot participation in the conversation</b><br>" +
                "If you want the chatbot to join the conversation, simply mention its name in your message. Our chatbot is called “botify”. botify then automatically responds to your message.<br>" +
                "For example: “botify, what is the current mood in the chat?”<br>" +
                "<b>4. Active users</b><br>" +
                "On the left side of the screen you will find a list of all active users. In addition to the user name, the language set is also displayed.<br>" +
                "<b>5. Display the current mood in the chat:</b><br>" +
                "Behind each message you will see an indicator that shows the current mood in the chat. This indicator is calculated all by itself. So you don't have to do anything!<br>" +
                "<br>" +
                "That's it! You are now ready to use Virtual Meet and communicate with other users.<br>" +
                "Have fun! 😊";
            chatMessageInput.placeholder = "Enter a message...";
            usernameInput.placeholder = "Enter a username..."
            chatWindow.placeholder = "Please enter a username, select a language and send a message to enter the chatroom...";
            saveButton.textContent = "Save";
            sendButton.textContent = "Send";
            userNameLabel.textContent = "Username";
            languageLabel.textContent = "Language"
            userListLabel.textContent = "Current Users";
            footerElement.innerHTML =
                "<u>Terms of Use</u><br>" +
                "By using this chat tool, you agree that you have read, understood, and accepted the following terms of use. Please read them carefully:<br>" +
                "General Use: This tool is for communication and information exchange purposes. Any use for illegal purposes is strictly prohibited.<br>" +
                "Disclaimer: The operators of the chat tool do not assume any liability for damages arising from the use of this tool. Users communicate at their own risk.<br>" +
                "Content Responsibility: Users are responsible for the content they share. Illegal, harmful, or unlawful content is prohibited.<br>" +
                "Privacy: Users acknowledge that privacy in an online chat can only be protected to a limited extent. Personal information should be handled with care.<br>" +
                "Changes to the Terms of Use: The operators reserve the right to change these terms of use at any time without notice. Continued use of the tool after such changes constitutes acceptance of the new terms.<br>" +
                "By using this tool, you agree to these terms.";
            break;
        case "fr":
            articleGuide.innerHTML =
                "<u>Premiers pas avec Virtual Meet</u><br>" +
                "Bienvenue sur Rencontre Virtual Meet ! Voici un guide rapide pour vous aider à démarrer :<br>" +
                "<br>" +
                "<b>1. Sélectionnez le nom d'utilisateur et la langue</b><br>" +
                "Avant de commencer, choisissez un nom d'utilisateur et votre langue préférée. N'oubliez pas d'appuyer sur \"Enregistrer\".<br>" +
                "<b>2. Envoi d'un message</b><br>" +
                "Pour envoyer un message, saisissez simplement votre texte dans le champ de texte et cliquez sur Envoyer. Votre message sera ensuite envoyé à tous les autres participants au chat.<br>" +
                "<b>3. Participation du chatbot à la conversation</b><br>" +
                "Si vous souhaitez que le chatbot rejoigne la conversation, mentionnez simplement son nom dans votre message. Notre chatbot s'appelle « botify ». botify répond alors automatiquement à votre message.<br>" +
                "Par exemple : « botify, quelle est l'ambiance actuelle dans le chat ?<br>" +
                "<b>4. Utilisateurs actifs</b><br>" +
                "Sur le côté gauche de l'écran, vous trouverez une liste de tous les utilisateurs actifs. Outre le nom d'utilisateur, la langue définie est également affichée.<br>" +
                "<b>5. Affichez l'ambiance actuelle dans le chat :</b><br>" +
                "Derrière chaque message, vous verrez un indicateur qui montre l'ambiance actuelle du chat. Cet indicateur est calculé tout seul. Vous n’avez donc rien à faire !<br>" +
                "<br>" +
                "C'est ça! Vous êtes maintenant prêt à utiliser Virtual Meet et à communiquer avec d'autres utilisateurs.<br>" +
                "Amusez-vous! 😊";
            chatMessageInput.placeholder = "Entrez votre message...";
            usernameInput.placeholder = "Saisissez votre nom d'utilisateur..."
            chatWindow.placeholder = "Veuillez saisir un nom d'utilisateur et sélectionner une langue pour accéder au salon de discussion...";
            saveButton.textContent = "Sauver";
            sendButton.textContent = "Envoyer";
            userNameLabel.textContent = "Nom d'utilisateur";
            languageLabel.textContent = "Langue"
            userListLabel.textContent = "Utilisateurs actuels";
            footerElement.innerHTML =
                "<u>Conditions d'Utilisation</u><br>" +
                "En utilisant cet outil de chat, vous acceptez d'avoir lu, compris et accepté les conditions d'utilisation suivantes. Veuillez les lire attentivement :<br>" +
                "Utilisation Générale : Cet outil est destiné à la communication et à l'échange d'informations. Toute utilisation à des fins illégales est strictement interdite.<br>" +
                "Avertissement : Les opérateurs de l'outil de chat n'assument aucune responsabilité pour les dommages résultant de l'utilisation de cet outil. Les utilisateurs communiquent à leurs propres risques.<br>" +
                "Responsabilité du Contenu : Les utilisateurs sont responsables du contenu qu'ils partagent. Les contenus illégaux, nuisibles ou illicites sont interdits.<br>" +
                "Protection de la Vie Privée : Les utilisateurs reconnaissent que la vie privée dans un chat en ligne ne peut être protégée que de manière limitée. Les informations personnelles doivent être traitées avec prudence.<br>" +
                "Modifications des Conditions d'Utilisation : Les opérateurs se réservent le droit de modifier ces conditions d'utilisation à tout moment sans préavis. L'utilisation continue de l'outil après de telles modifications constitue une acceptation des nouvelles conditions.<br>" +
                "En utilisant cet outil, vous acceptez ces conditions.";
            break;
        case "it":
            articleGuide.innerHTML =
                "<u>Iniziare con Virtual Meet</u><br>" +
                "Benvenuto su Virtual Meet! Ecco una guida rapida per iniziare:<br>" +
                "<br>" +
                "<b>1. Seleziona nome utente e lingua</b><br>" +
                "Prima di iniziare, scegli un nome utente e la tua lingua preferita. Non dimenticare di premere \"Salva\".<br>" +
                "<b>2. Invio di un messaggio</b><br>" +
                "Per inviare un messaggio, inserisci semplicemente il testo nel campo di testo e fai clic su Invia. Il tuo messaggio verrà quindi inviato a tutti gli altri partecipanti alla chat.<br>" +
                "<b>3. Partecipazione del chatbot alla conversazione</b><br>" +
                "Se vuoi che il chatbot si unisca alla conversazione, menziona semplicemente il suo nome nel tuo messaggio. Il nostro chatbot si chiama “botify”. botify risponde quindi automaticamente al tuo messaggio.<br>" +
                "Ad esempio: \"botify, qual è l'umore attuale nella chat?\"<br>" +
                "<b>4. Utenti attivi </b><br>" +
                "Sul lato sinistro dello schermo troverai un elenco di tutti gli utenti attivi. Oltre al nome utente viene visualizzata anche la lingua impostata.<br>" +
                "<b>5. Visualizza lo stato d'animo attuale nella chat:</b><br>" +
                "Dietro ogni messaggio vedrai un indicatore che mostra lo stato d'animo attuale nella chat. Questo indicatore è calcolato da solo. Quindi non devi fare nulla!<br>" +
                "<br>" +
                "Questo è tutto! Ora sei pronto per utilizzare Virtual Meet e comunicare con altri utenti.<br>" +
                "Divertiti! 😊";
            chatMessageInput.placeholder = "Inserisci il tuo messaggio...";
            usernameInput.placeholder = "Inserire username..."
            chatWindow.placeholder = "Inserisci un nome utente, seleziona una lingua e invia un messaggio per entrare nella chatroom...";
            saveButton.textContent = "Salva";
            sendButton.textContent = "Inviare";
            userNameLabel.textContent = "Nome utente";
            languageLabel.textContent = "Lingua"
            userListLabel.textContent = "Utenti attivi";
            footerElement.innerHTML =
                "<u>Termini di Utilizzo</u><br>" +
                "Utilizzando questo strumento di chat, accetti di aver letto, compreso e accettato i seguenti termini di utilizzo. Si prega di leggerli attentamente:<br>" +
                "Uso Generale: Questo strumento è destinato alla comunicazione e allo scambio di informazioni. Qualsiasi uso per scopi illegali è severamente proibito.<br>" +
                "Esclusione di Responsabilità: Gli operatori dello strumento di chat non assumono alcuna responsabilità per danni derivanti dall'uso di questo strumento. Gli utenti comunicano a proprio rischio.<br>" +
                "Responsabilità dei Contenuti: Gli utenti sono responsabili per i contenuti che condividono. Contenuti illegali, dannosi o illeciti sono proibiti.<br>" +
                "Privacy: Gli utenti riconoscono che la privacy in una chat online può essere protetta solo in modo limitato. Le informazioni personali dovrebbero essere trattate con cautela.<br>" +
                "Modifiche ai Termini di Utilizzo: Gli operatori si riservano il diritto di modificare questi termini di utilizzo in qualsiasi momento senza preavviso. L'uso continuato dello strumento dopo tali modifiche costituisce accettazione dei nuovi termini.<br>" +
                "Utilizzando questo strumento, accetti questi termini.";
            break;
        case "es":
            articleGuide.innerHTML =
                "<u>Comenzando con Virtual Meet</u><br>" +
                "¡Bienvenidos a Virtual Meet! Aquí tienes una guía rápida para empezar:<br>" +
                "<br>" +
                "<b>1. Seleccione nombre de usuario e idioma</b><br>" +
                "Antes de comenzar, elija un nombre de usuario y su idioma preferido. No olvides presionar \"Guardar\".<br>" +
                "<b>2. Enviar un mensaje</b><br>" +
                "Para enviar un mensaje, simplemente ingrese su texto en el campo de texto y haga clic en Enviar. Luego, su mensaje se enviará a todos los demás participantes del chat.<br>" +
                "<b>3. Participación del chatbot en la conversación. </b><br>" +
                "Si desea que el chatbot se una a la conversación, simplemente mencione su nombre en su mensaje. Nuestro chatbot se llama \"botify\". Luego, botify responde automáticamente a su mensaje.<br>" +
                "Por ejemplo: \"botify, ¿cuál es el estado de ánimo actual en el chat?\"<br>" +
                "<b>4. Usuarios activos </b><br>" +
                "En el lado izquierdo de la pantalla encontrarás una lista de todos los usuarios activos. Además del nombre de usuario, también se muestra el idioma configurado.<br>" +
                "<b>5. Muestra el estado de ánimo actual en el chat:</b><br>" +
                "Detrás de cada mensaje verás un indicador que muestra el estado de ánimo actual en el chat. Este indicador se calcula por sí solo. ¡Así que no tienes que hacer nada!<br>" +
                "<br>" +
                "¡Eso es todo! Ahora está listo para utilizar Virtual Meet y comunicarse con otros usuarios.<br>" +
                "¡Divertirse! 😊";
            chatMessageInput.placeholder = "Ingrese su mensaje...";
            usernameInput.placeholder = "Introduzca su nombre de usuario..."
            chatWindow.placeholder = "Por favor ingrese un nombre de usuario, seleccione un idioma y envíe un mensaje para ingresar a la sala de chat...";
            saveButton.textContent = "Ahorrar";
            sendButton.textContent = "Enviar";
            userNameLabel.textContent = "Usuario";
            languageLabel.textContent = "Idioma"
            userListLabel.textContent = "Usuarios activos";
            footerElement.innerHTML =
                "<u>Términos de Uso</u><br>" +
                "Al utilizar esta herramienta de chat, usted acepta que ha leído, entendido y aceptado los siguientes términos de uso. Por favor, léalos cuidadosamente:<br>" +
                "Uso General: Esta herramienta es para fines de comunicación e intercambio de información. Cualquier uso con fines ilegales está estrictamente prohibido.<br>" +
                "Descargo de Responsabilidad: Los operadores de la herramienta de chat no asumen ninguna responsabilidad por los daños resultantes del uso de esta herramienta. Los usuarios se comunican bajo su propio riesgo.<br>" +
                "Responsabilidad del Contenido: Los usuarios son responsables del contenido que comparten. Está prohibido el contenido ilegal, dañino o ilícito.<br>" +
                "Privacidad: Los usuarios reconocen que la privacidad en un chat en línea solo puede protegerse de manera limitada. La información personal debe manejarse con cuidado.<br>" +
                "Cambios en los Términos de Uso: Los operadores se reservan el derecho de cambiar estos términos de uso en cualquier momento sin previo aviso. El uso continuado de la herramienta después de tales cambios constituye la aceptación de los nuevos términos.<br>" +
                "Al utilizar esta herramienta, usted acepta estos términos.";
            break;
    }
}
/**
 * Adds an EventListener that enables the function to send messages with the "Enter" button
 */
document.addEventListener('keydown', function(event){
    let element = document.getElementById("chatTextInput");
    if(event.key === "Enter" && document.activeElement === element){
       document.getElementById("sendButton").click();
    }
});

/**
 * Adds an EventListener that is responsible for the dropdown menu of the language select button.
 * Tt gets all HTML "a" element that are in the dropdown-content div and saves it in a NodeList.
 * Every Element gets appointed a function that is being executed after being clicked.
 * There the chosen value (language) gets set and will be displayed as the chosen language in the UI
 */
document.addEventListener('DOMContentLoaded', function() {
  var dropdownLinks = document.querySelectorAll('.dropdown-content a');
  var hiddenInput = document.getElementById('dropdownValue');

  dropdownLinks.forEach(function(link) {
      link.addEventListener('click', function(e) {
      var value = this.getAttribute('data-value');
      hiddenInput.value = value;
      selectLanguage();
    });
  });
});

/**
 * Adds an EventListener that is responsible for saving the user settings IF the user is in the input field and presses "Enter"
 */
document.addEventListener("keydown", function(event) {
    let element = document.getElementById("nicknameArea");
    if (event.key === "Enter" && document.activeElement === element) {
        event.preventDefault();
        saveUserSettings();
        document.getElementById("chatTextInput").focus();
    }
});