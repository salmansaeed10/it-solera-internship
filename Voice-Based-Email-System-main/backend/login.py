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
from helper import speak,listen ,preprocess_text


#login Function
def login():
    speak("Please enter your email address.")
    #email = input("Please enter your email address: ")
    email = listen()
    speak("Please enter your app password.")
    # password = input("Please enter your app password: ")
    password = getpass.getpass(listen())
    email = preprocess_text(email)
    password = preprocess_text(password)

    print(email)
    print(password)  # For debugging only, remove in production

    try:
        # Connect to the SMTP server
        smtp_server = smtplib.SMTP('smtp.gmail.com', 587)
        smtp_server.starttls()  # Upgrade to a secure connection

        # Log in to the SMTP server
        smtp_server.login(email, password)
        speak("Logged in to SMTP server successfully!")

        # Connect to the IMAP server
        imap_server = imaplib.IMAP4_SSL("imap.gmail.com")

        # Log in to the IMAP server
        imap_server.login(email, password)
        speak("Logged in to IMAP server successfully!")

        return smtp_server, imap_server, email
    except smtplib.SMTPAuthenticationError:
        speak("Authentication failed. Please check your credentials or app password.")
    except smtplib.SMTPConnectError:
        speak("Failed to connect to the SMTP server. Check server and port.")
    except smtplib.SMTPException as e:
        speak(f"SMTP error occurred: {e}")
    except imaplib.IMAP4.error:
        speak("Failed to connect to the IMAP server. Check your credentials.")
    except Exception as e:
        speak(f"An error occurred: {e}")

    return None, None, None
