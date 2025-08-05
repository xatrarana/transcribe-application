import whisper

# Load the Whisper model
model = whisper.load_model("large-v3")

# Transcribe the audio file
result = model.transcribe("file.mp4", language="ne")

# Save the transcription to a text file
with open("transcription.txt", "w", encoding="utf-8") as f:
    f.write(result["text"])

print("✅ Transcription saved to 'transcription.txt'")
