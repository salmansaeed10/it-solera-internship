# Project13-Voice-Based-Email-System

## Project Overview
The Voice-Based Email System is a voice-controlled application that allows users to interact with their Gmail accounts through speech. By utilizing text-to-speech and speech recognition technologies, users can perform various email functions like reading, composing, sending, and navigating emails through different folders— all by using voice commands.

## Features
  Login Functionality: Log in to Gmail directly from the application.
  Compose Email: Create a new email by speaking the content.
  Read Emails: Listen to emails read out loud to you.
  Send Emails: Send emails through voice commands.
  Folder Navigation: Navigate between different email folders like Inbox, Sent, Trash, etc.
  Speech-to-Text & Text-to-Speech Support: Convert speech to text for commands and convert email content to speech.

## Technology Stack
  Python: Core language for development.
  pyttsx3: Library used for text-to-speech conversion.
  SpeechRecognition: Library used for speech-to-text conversion.
  SMTP & IMAP Servers: Used for sending and receiving requests from Gmail.

## How It Works

### Login to Gmail:
The application prompts you to log in to your Gmail account.
You provide the login credentials, which are used to authenticate through Gmail's SMTP and IMAP servers.

### Compose Email:
When you speak the content, the speech-to-text system converts it into text and populates the email content.

### Send, Read, Write, and Navigate Emails:
You can send emails or listen to the ones you received.
The application allows you to navigate between different email folders (Inbox, Sent, Trash).

## Requirements
Python 3.x
Gmail account
Libraries: pyttsx3, SpeechRecognition, smtplib, imaplib
