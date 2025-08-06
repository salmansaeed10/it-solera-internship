# # import necessary laibraries
# import os
# import wave
# import pyaudio
# import pyttsx3
# from pynput import keyboard
# from groq import Groq

# # Initialize the Groq client (replace with your API key)
# GROQ_API_KEY = "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"
# client = Groq(api_key=GROQ_API_KEY)

# # Initialize the TTS engine
# engine = pyttsx3.init()

# # Set the speech rate
# engine.setProperty('rate', 150)  # Adjust this value to make the voice slower or faster

# # Define recording parameters
# CHUNK = 1024 #number of audio frames per buffer. 
# FORMAT = pyaudio.paInt16  #each audio sample is stored as a 16-bit signed integer (2 bytes per sample).
# CHANNELS = 1 #number of audio channels to be recorded
# RATE = 44100 # how many audio samples are captured per second.

# recording = False  # Track recording state
# frames = []  # To store audio frames

# # function for stop when press enter or esc
# def on_press(key):
#     """
#     Callback function to handle key presses.
#     Stops the recording when Enter or Esc is pressed.
#     """
#     global recording
#     if key == keyboard.Key.enter or key == keyboard.Key.esc:
#         recording = False
#         print("\nRecording stopped.")
#         return False  # Stop listening for key presses

# #function to record the audio
# def record_audio():
#     """
#     Records audio and stops based on key press.
#     """
#     global recording, frames
#     recording = True  # Start recording

#     p = pyaudio.PyAudio()

#     stream = p.open(format=FORMAT,
#                     channels=CHANNELS,
#                     rate=RATE,
#                     input=True,
#                     frames_per_buffer=CHUNK)

#     print("Recording... Press 'Enter' or 'Esc' to stop.")

#     while recording:
#         data = stream.read(CHUNK)
#         frames.append(data)

#     stream.stop_stream()
#     stream.close()
#     p.terminate()

# # function to save the audio
# def save_audio():
#     """
#     Saves the recorded audio to a file named 'audio.mp3'.
#     """
#     filename = 'audio.mp3'  # Save the file as audio.mp3
#     wf = wave.open(filename, 'wb')
#     wf.setnchannels(CHANNELS)
#     wf.setsampwidth(pyaudio.PyAudio().get_sample_size(FORMAT))
#     wf.setframerate(RATE)
#     wf.writeframes(b''.join(frames))
#     wf.close()
    
#     print(f"Audio saved as: {filename}")
#     return filename

# # conversion of audio to text and then text to audio
# def transcribe_audio(audio_file):
#     """
#     Transcribes the saved audio using Groq API.
#     """
#     try:
#         with open(audio_file, 'rb') as f:
#             transcription = client.audio.transcriptions.create(
#                 file=f,
#                 model="distil-whisper-large-v3-en",
#                 prompt="Specify context or spelling",  # Optional
#                 response_format="json",  # Optional
#                 language="en",  # Optional
#                 temperature=0.0  # Optional
#             )

#         # Speak the transcribed text
#         engine.say(transcription.text)
#         engine.runAndWait()

#         print(f"Transcription: {transcription.text}")

#     except Groq.APIError as e:
#         print(f"Groq API Error: {e}")


# if __name__ == "__main__":
#     # Listen for key presses to stop recording
#     listener = keyboard.Listener(on_press=on_press)
#     listener.start()

#     # Start recording audio
#     record_audio()

#     # Wait for listener to finish (when recording stops)
#     listener.join()

#     # Save and process the recorded audio
#     saved_audio = save_audio()
#     transcribe_audio(saved_audio)

#     # Clean up the saved file (optional)
#     # os.remove(saved_audio)
