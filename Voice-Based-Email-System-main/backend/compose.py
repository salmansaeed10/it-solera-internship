import smtplib
from email.mime.text import MIMEText
from helper import preprocess_text, listen, speak, logout

def compose_email(server, email, main):
    """Composes an email based on user's speech input and sends it."""

    while True:
        speak("Please say the email subject.")
        subject = listen()
        if subject is None:
            speak("Could not understand the subject. Please try again.")
            continue
        
        if 'main menu' in subject.lower():
            speak("Returning to the main menu.")
            main()  # Call the main function
            return
        
        speak("Please say the email body. Say 'uppercase' before any letter you want to be capitalized.")
        body = ""
        while True:
            word = listen()
            if word is None:
                speak("Could not understand the body content. Please try again.")
                continue
            
            if 'main menu' in word.lower():
                speak("Returning to the main menu.")
                main()  # Call the main function
                return
            
            if word.lower() == 'uppercase':
                speak("Speak the uppercase letter.")
                uppercase_letter = listen()
                if uppercase_letter is None:
                    speak("Could not understand the uppercase letter. Please try again.")
                    continue
                body += uppercase_letter.upper()
            else:
                body += word
            
            if 'done' in word.lower() or 'finish' or 'finished' in word.lower():
                break
        
        speak('Please say the recipient email address')
        recipient_email = listen()
        if recipient_email is None:
            speak("Could not understand the recipient email. Please try again.")
            continue
        
        if 'main menu' in recipient_email.lower():
            speak("Returning to the main menu.")
            main()  # Call the main function
            return
        
        recipient_email = preprocess_text(recipient_email)
        print(recipient_email)

        speak("Do you want to send this email? Say 'Yes' to send, 'No' to cancel, 'Back' to return to the main menu, or 'Exit' to quit.")
        confirmation = listen()
        if confirmation is None:
            speak("Could not understand your response. Please try again.")
            continue
        
        if 'back' in confirmation.lower():
            speak("Returning to the main menu.")
            main()  # Call the main function
            return
        
        if 'exit' in confirmation.lower():
            speak("Exiting.")
            logout()  # Assuming logout function is available in your helper
            return
        
        if 'yes' in confirmation.lower():
            msg = MIMEText(body)
            msg['Subject'] = subject
            msg['From'] = email
            msg['To'] = recipient_email

            try:
                server.sendmail(email, [recipient_email], msg.as_string())
                speak("Email sent successfully!")
            except smtplib.SMTPException as e:
                speak(f"Failed to send the email: {e}")
        elif 'no' in confirmation.lower():
            speak("Email composition cancelled.")
        else:
            speak("Unknown response. Please say 'Yes' to send, 'No' to cancel, 'Back' to return to the main menu, or 'Exit' to quit.")
