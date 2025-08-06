
import smtplib
import pyttsx3
from email.mime.text import MIMEText
import getpass
import speech_recognition as sr
import imaplib
import email
from email.header import decode_header
from word2number import w2n
import keyboard
from helper import print_and_speak, recognize_speech, convert_words_to_number, logout


def inbox(mail, main):
    print_and_speak("Welcome to the inbox. You can say 'read' followed by the number to read an email, 'delete' followed by the number to delete an email, back to navigate to main menu or 'exit' to quit.")
    while True:
        command = recognize_speech()
        if command:
            if "read" in command:
                parts = command.split()
                if len(parts) == 2:
                    num = convert_words_to_number(parts[1])
                    if num is not None:
                        content = fetch_email(mail, num)
                        print_and_speak("Email content: " + content)
                    else:
                        print_and_speak("Invalid number format. Please say 'read' followed by a valid number.")
                else:
                    print_and_speak("Invalid command format. Please say 'read' followed by a number.")
            elif "delete" in command:
                parts = command.split()
                if len(parts) == 2:
                    num = convert_words_to_number(parts[1])
                    if num is not None:
                        result = delete_email(mail, num)
                        print_and_speak(result)
                    else:
                        print_and_speak("Invalid number format. Please say 'delete' followed by a valid number.")
                else:
                    print_and_speak("Invalid command format. Please say 'delete' followed by a number.")
            elif "exit" in command or "quit" in command:
                print_and_speak("Exiting the assistant.")
                logout()
                break
            elif "back" in command:
                main()
            else:
                print_and_speak("Unknown command. Please say 'read' followed by the number, 'delete' followed by the number, or 'exit' to quit.")


def delete_email(mail, index):
    mail.select('inbox')
    status, data = mail.search(None, 'ALL')
    email_ids = data[0].split()
    num_emails = len(email_ids)
    
    if index < 1 or index > num_emails:
        return f"Invalid email number. Please select a number between 1 and {num_emails}."

    email_id = email_ids[-index]
    mail.store(email_id, '+FLAGS', '\\Deleted')
    mail.expunge()
    return "Email deleted."


def fetch_email(mail, index):
    mail.select('inbox')
    status, data = mail.search(None, 'ALL')
    email_ids = data[0].split()
    num_emails = len(email_ids)
    
    if index < 1 or index > num_emails:
        return f"Invalid email number. Please select a number between 1 and {num_emails}."

    email_id = email_ids[-index]
    status, msg_data = mail.fetch(email_id, '(RFC822)')
    msg = email.message_from_bytes(msg_data[0][1])
    
    subject = decode_header(msg['Subject'])[0][0]
    if isinstance(subject, bytes):
        subject = subject.decode()

    if msg.is_multipart():
        for part in msg.walk():
            if part.get_content_type() == "text/plain":
                return part.get_payload(decode=True).decode()
    else:
        return msg.get_payload(decode=True).decode()

    return "No content found."
    

