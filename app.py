import whisper
import asyncio
from googletrans import Translator
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.scrolledtext import ScrolledText
import pyperclip
from docx import Document
import threading

# Run blocking whisper/translation in separate thread to not freeze GUI
def run_transcription(filename, text_widget, btn_transcribe, selected_model):
    btn_transcribe.config(state="disabled")
    text_widget.delete("1.0", tk.END)
    text_widget.insert(tk.END, "Processing... Please wait.\n")

    def worker():
        try:
            # Load model (can be cached globally to improve speed)
            model = whisper.load_model(selected_model, device="cpu")

            # Transcribe & translate
            result = model.transcribe(filename, task="translate")
            english_text = result["text"]
            print(english_text)

            # Translate to Nepali
            translator = Translator()
            nepali_translation = asyncio.run(translator.translate(english_text, src='en', dest='ne'))

            # Update GUI
            text_widget.delete("1.0", tk.END)
            text_widget.insert(tk.END, nepali_translation.text)
        except Exception as e:
            text_widget.delete("1.0", tk.END)
            text_widget.insert(tk.END, f"Error: {str(e)}")
        finally:
            btn_transcribe.config(state="normal")

    threading.Thread(target=worker).start()

def copy_to_clipboard(text_widget):
    text = text_widget.get("1.0", tk.END).strip()
    if text:
        pyperclip.copy(text)
        messagebox.showinfo("Copied", "Text copied to clipboard!")
    else:
        messagebox.showwarning("Empty", "No text to copy!")

def save_to_doc(filename, text_widget):
    text = text_widget.get("1.0", tk.END).strip()
    if not text:
        messagebox.showwarning("Empty", "No text to save!")
        return

    if not filename:
        messagebox.showwarning("No file", "No audio/video file selected!")
        return

    # Save to Word doc with same base filename + .docx
    doc_filename = filedialog.asksaveasfilename(
        defaultextension=".docx",
        filetypes=[("Word Documents", "*.docx")],
        initialfile=filename.rsplit(".", 1)[0] + ".docx"
    )
    if doc_filename:
        doc = Document()
        doc.add_paragraph(text)
        doc.save(doc_filename)
        messagebox.showinfo("Saved", f"Transcript saved to:\n{doc_filename}")

def browse_file(entry, root):
    filename = filedialog.askopenfilename(
        title="Select Audio/Video file",
        filetypes=[("Audio/Video Files", "*.mp3 *.wav *.mp4 *.m4a *.flac *.aac *.ogg *.webm"), ("All files", "*.*")]
    )
    if filename:
        entry.delete(0, tk.END)
        entry.insert(0, filename)

def main():
    root = tk.Tk()
    root.title("Whisper Translate Nepali")
    root.geometry("700x500")

    tk.Label(root, text="Select audio/video file:").pack(pady=5)

    frame = tk.Frame(root)
    frame.pack(pady=5, fill=tk.X, padx=10)

    file_entry = tk.Entry(frame)
    file_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)

    browse_btn = tk.Button(frame, text="Browse", command=lambda: browse_file(file_entry, root))
    browse_btn.pack(side=tk.LEFT, padx=5)

     # Model selection
    model_frame = tk.Frame(root)
    model_frame.pack(pady=5)
    tk.Label(model_frame, text="Select Whisper Model:").pack(side=tk.LEFT)

    model_var = tk.StringVar(value="medium")  # Default to medium
    model_options = ["base", "medium", "large-v3"]
    model_menu = tk.OptionMenu(model_frame, model_var, *model_options)
    model_menu.pack(side=tk.LEFT, padx=5)

    text_widget = ScrolledText(root, wrap=tk.WORD, height=20)
    text_widget.pack(padx=10, pady=(4,10), fill=tk.BOTH, expand=True)

    btn_frame = tk.Frame(root)
    btn_frame.pack(pady=10)

    transcribe_btn = tk.Button(
        btn_frame,
        text="Transcribe & Translate",
        command=lambda: run_transcription(file_entry.get(), text_widget, transcribe_btn,model_var.get())
    )
    transcribe_btn.pack(side=tk.LEFT, padx=10)

    copy_btn = tk.Button(
        btn_frame,
        text="Copy to Clipboard",
        command=lambda: copy_to_clipboard(text_widget)
    )
    copy_btn.pack(side=tk.LEFT, padx=10)

    save_btn = tk.Button(
        btn_frame,
        text="Save as Word Document",
        command=lambda: save_to_doc(file_entry.get(), text_widget)
    )
    save_btn.pack(side=tk.LEFT, padx=10)

    root.mainloop()

if __name__ == "__main__":
    main()
