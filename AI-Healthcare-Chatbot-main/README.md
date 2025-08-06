# Project12-AI-Healthcare-Chatbot

## Table of Contents
  1. Overview
  2. Features
  3. Project Structure
  4. Installation
  5. Usage
  6. Deployment
  7. Contributing
  
## Overview
The AI Healthcare Chatbot is designed to assist users in identifying diseases based on symptoms and suggesting appropriate treatments. It also offers functionality to book appointments with doctors and locate nearby hospitals or clinics. The chatbot leverages the LLaMA-3 model with prompt engineering to ensure it handles healthcare-specific queries effectively.

## Workflow Diagram
![Workflow Diagram For Healthcare chatbot](https://github.com/Abdul1302/Project12-AI-Healthcare-Chatbot/blob/main/Workflow%20Diagram%20For%20Healthcare%20chatbot.jpg)


## Features
  **Disease Identification:** Provides possible diagnoses based on user-reported symptoms.
  **Treatment Suggestions:** Recommends treatments for identified conditions.
  **Appointment Booking:** Schedules appointments with doctors based on their availability.
  **Location Services:** Helps users find nearby hospitals or clinics using a map interface.
  **Speech Integration:** Supports speech-to-text and text-to-speech for user interaction.

## Project Structure

  ### Model and Data Handling:
  Uses LLaMA-3 model with prompt engineering.
  Implements Retrieval-Augmented Generation (RAG) concept.
  Processes data from medical documents:
  Medicalstudyzone.com Pathoma 2023 PDF.pdf
  First Aid for the USMLE Step 1 2024 34th Edition [Medicalstudyzone.com]_compressed.pdf
  Embeddings are created using Hugging Face Mini Embedding model and stored in Pinecone vector database.

  ### Appointment Scheduling:
  Uses Python and Pandas to handle CSV files with doctor schedules.
  Books appointments based on available slots.
  User Interface:
  
  ### Built with React.
  Integrated with Leaflet for map-based location services.
  
## Interacting with the Chatbot:
  Use the text or speech input to report symptoms.
  Receive possible diagnoses and treatment suggestions.
  Book an appointment based on doctor availability.
  Find nearby hospitals or clinics using the integrated map.

## Deployment
This project is deployed on Vercel.

