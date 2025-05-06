import speech_recognition as sr
import os
import ollama


r = sr.Recognizer()
mic = sr.Microphone()

# Create notes directory if it doesn't exist
if not os.path.exists('notes'):
    os.makedirs('notes')

# (Optional) Calibrate the mic to ambient noise in a temporary context
with mic as source:
    r.adjust_for_ambient_noise(source)
    print("Calibrated for ambient noise.")

# Start background listening (no `with` here!)
print("Listening in background...")
stop_listening = r.listen_in_background(mic, lambda recognizer, audio: handle_audio(recognizer, audio))

# Callback function must be defined BEFORE calling listen_in_background
def handle_audio(recognizer, audio):
    try:
        text = recognizer.recognize_google(audio)
        print("You said:", text)
        
        # Save to file with timestamp
        filename = "notes/speech_notes.txt"
        with open(filename, "a") as f:
            f.write(f"{text}\n")
        print(f"Appended to {filename}")
        
    except Exception as e:
        print("Error:", e)

input("Press Enter to stop listening...\n")

# Stop the listener
stop_listening()


with open("notes/speech_notes.txt") as f:
    notes_text = f.read()

response = ollama.chat(
    model="mistral",
    messages=[
        {"role": "user", "content": "Summarize the following notes:\n" + notes_text}
    ]
)

print("Summary:")
print(response["message"]["content"])