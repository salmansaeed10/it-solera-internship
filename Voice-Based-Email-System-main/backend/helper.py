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

#Initialize text-to-speech engine
engine = pyttsx3.init()
recognizer = sr.Recognizer()

# Recognize Speech
def recognize_speech():
    recognizer = sr.Recognizer()
    while True:
        if keyboard.is_pressed('esc'):
            print_and_speak("Exiting...")
            break
        with sr.Microphone() as source:
            print("Listening...")
            audio = recognizer.listen(source)
            try:
                command = recognizer.recognize_google(audio).lower()
                print(f"You said: {command}")
                return command
            except sr.UnknownValueError:
                print_and_speak("Sorry, I did not understand that. Please try again.")
            except sr.RequestError:
                print_and_speak("Sorry, there was an error with the speech recognition service.")
                break


#Preprocessing Function
def preprocess_text(text):
  """Processes speech recognition output for email and password."""
  # Lowercase for case-insensitive matching
  text = text.lower()

  # Remove spaces (important for email addresses and potentially passwords)
  text = ''.join(text.split())

  # Handle "at" variations for email addresses
  #text = text.replace('attherate ', '@')  # Additional handling for potential variations

  # Optionally, consider more advanced processing for passwords (e.g., special characters)
  temp=text
  special_chars = ['attherate','dot','underscore','dollar','hash','star','plus','minus','space','dash']
  for character in special_chars:
      while(True):
          pos=temp.find(character)
          if pos == -1:
              break
          else :
              if character == 'attherate':
                  temp=temp.replace('attherate','@')
              elif character == 'dot':
                  temp=temp.replace('dot','.')
              elif character == 'underscore':
                  temp=temp.replace('underscore','_')
              elif character == 'dollar':
                  temp=temp.replace('dollar','$')
              elif character == 'hash':
                  temp=temp.replace('hash','#')
              elif character == 'star':
                  temp=temp.replace('star','*')
              elif character == 'plus':
                  temp=temp.replace('plus','+')
              elif character == 'minus':
                  temp=temp.replace('minus','-')
              elif character == 'space':
                  temp = temp.replace('space', '')
              elif character == 'dash':
                  temp=temp.replace('dash','-')
  return temp

#Listen Function 
def listen():
  with sr.Microphone() as source:
    print("Listening...")
    recognizer.adjust_for_ambient_noise(source)  # Adjust for ambient noise
    audio = recognizer.listen(source)
    try:
        text = recognizer.recognize_google(audio)
        print("You said: " + text)
        return text
    except sr.UnknownValueError:
        speak("Sorry, I did not understand that.")
        return None
    except sr.RequestError:
        speak("Sorry, there was an error with the speech recognition service.")
        return None
    else:
       text = recognizer.recognize_google(audio)
       print("You said: " + text)
       return text


#Speak function
def speak(text):
  engine.say(text)
  engine.runAndWait()

#print & speak function
def print_and_speak(text):
    print(text)
    speak(text)

#Convert word to number
def convert_words_to_number(words):
  try:
    number = w2n.word_to_num(words)
    return number
  except ValueError:
    return None

#Fetch the email
def fetch_emails_from_folder(mail, folder):
    mail.select(folder)
    status, data = mail.search(None, 'ALL')
    email_ids = data[0].split()
    num_emails = len(email_ids)
    emails = []
    for index in range(num_emails):
        email_id = email_ids[-(index+1)]
        status, msg_data = mail.fetch(email_id, '(RFC822)')
        msg = email.message_from_bytes(msg_data[0][1])
        subject = decode_header(msg['Subject'])[0][0]
        if isinstance(subject, bytes):
            subject = subject.decode()
        emails.append((index + 1, subject))
    return emails

#Read the email
def read_emails_from_folder(mail, folder_name):
    while True:
        emails = fetch_emails_from_folder(mail, folder_name)
        for index, subject in emails:
            print_and_speak(f"{index}: {subject}")
        
        print_and_speak(f"Welcome to the {folder_name}. You can say 'read' followed by the number to read an email, 'menu' to return to the main menu, or 'logout' to log out.")
        command = recognize_speech()
        if command:
            if "read" in command:
                parts = command.split()
                if len(parts) == 2:
                    num = convert_words_to_number(parts[1])
                    if num is not None:
                        content = fetch_emails_from_folder(mail, num)
                        print_and_speak("Email content: " + content)
                    else:
                        print_and_speak("Invalid number format. Please say 'read' followed by a valid number.")
                else:
                    print_and_speak("Invalid command format. Please say 'read' followed by a number.")
            elif "menu" in command or "main menu" in command:
                return
            elif "logout" in command:
                print_and_speak("Logging out.")
                mail.logout()
                return
            elif "exit" in command or "quit" in command:
                print_and_speak("Exiting the assistant.")
                break
            else:
                print_and_speak("Unknown command. Please say 'read' followed by the number, 'menu' to return to the main menu, or 'logout' to log out.")


                  # Need editing in delete function
###############################################################
def delete_email(mail, index):
    #mail.select(folder)
    status, data = mail.search(None, 'ALL')
    email_ids = data[0].split()
    num_emails = len(email_ids)
    
    if index < 1 or index > num_emails:
        return f"Invalid email number. Please select a number between 1 and {num_emails}."

    email_id = email_ids[-index]
    mail.store(email_id, '+FLAGS', '\\Deleted')
    mail.expunge()
    return "Email deleted."
###############################################################

def logout(server, mail):
    speak("Exiting.")
    server.quit()
    mail.logout()
    speak("Logout Successfully!")


