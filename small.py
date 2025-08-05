# import whisper

# model = whisper.load_model("large-v3", device="cpu")  # use CPU if you want

# # Use task='translate' to get everything in English
# result = model.transcribe("minified.mp4", language="ne", task="transcribe")

# print(result["text"])


# Save the transcription to a text file
# with open("small.txt", "w", encoding="utf-8") as f:
#     f.write(result["text"])

# print("✅ Transcription saved to 'small.txt'")
# import whisper

# # Check if CUDA is available
# # device = "cuda" if torch.cuda.is_available() else "cpu"
# # print(f"Using device: {device}")

# # Load the model and move it to GPU
# model = whisper.load_model("medium").to("cpu")

# # Transcribe using the model (Whisper internally handles device)
# result = model.transcribe("minified.mp4", language="ne")
# print("Detected language:", result.get("language"))

# print(result["text"])
