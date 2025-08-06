import smtplib
import pyttsx3
import speech_recognition as sr
from login import login
from helper import speak, logout, listen
from compose import compose_email
from inbox import inbox
from trash import trash
from important import important

"""username = dummyjohn513@gmail.com
password = uuaizknexnflninb
"""

class EmailAssistant:
    def __init__(self):
        self.engine = pyttsx3.init()
        self.recognizer = sr.Recognizer()
        self.smtp_server = None
        self.imap_server = None
        self.email_address = None
        self.login()

    def login(self):
        self.smtp_server, self.imap_server, self.email_address = login()
        if self.smtp_server is None or self.imap_server is None:
            speak("Login failed. Exiting.")
            exit()

    def main(self):

        speak("Say 'compose' to start writing an email, 'inbox' to navigate inbox page, 'important' to navigate important page, 'trash' to navigate trash page, or 'logout' to quit.")
        
        while True:
            command = listen()
            if command:
                if 'compose' in command.lower():
                    compose_email(self.smtp_server, self.email_address, self.main)
                elif 'inbox' in command.lower():
                    inbox(self.imap_server, self.main)
                elif 'important' in command.lower():
                    important(self.imap_server, self.main)
                elif 'trash' in command.lower():
                    trash(self.imap_server, self.main)
                elif 'logout' in command.lower():
                    speak("Exiting.")
                    logout(self.smtp_server, self.imap_server)
                    break
                else:
                    speak("Command not recognized. Please try again.")

if __name__ == "__main__":
    assistant = EmailAssistant()
    assistant.main()
