import speech_recognition as spr
import pytesseract
from PIL import Image
from googletrans import Translator
from tkinter import filedialog
from gtts import gTTS
import os
import tkinter as tk

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'

padding = 10
        


class TranslatorApp(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.grid()
        self.create_widgets()

        self.recog = spr.Recognizer()
        self.mic = spr.Microphone()
        self.translator = Translator()
        self.from_lang = 'en'
        self.to_lang = 'kn'
        self.master.config(bg="#F5F5F5")
        
        

    def create_widgets(self):
        
        self.hello_button = tk.Button(self)
        self.hello_button["text"] = "Say Hello to Translate"
        self.hello_button["command"] = self.say_hello
        self.hello_button.grid(row=0, column=0, padx=padding, pady=padding)

        # Add an upload button for image recognition
        self.upload_button = tk.Button(self)
        self.upload_button["text"] = "Upload Image"
        self.upload_button["command"] = self.upload_image
        self.upload_button.grid(row=5, column=1, padx=padding, pady=padding)

        # Add a label to display the recognized text from the uploaded image
        self.image_text_label = tk.Label(self, text="")
        self.image_text_label.grid(row=5, column=1, padx=padding, pady=padding)

        self.speak_button = tk.Button(self)
        self.speak_button["text"] = "Speak the Sentence"
        self.speak_button["command"] = self.speak_sentence
        self.speak_button.grid(row=1, column=0, padx=padding, pady=padding)

        self.status_label = tk.Label(self, text="Status: Ready")
        self.status_label.grid(row=2, column=0, padx=padding, pady=padding)

        self.text_box = tk.Text(self, height=10, width=50)
        self.text_box.grid(row=3, column=0, padx=padding, pady=padding)

        # Add a dropdown menu for selecting the language to be translated
        self.lang_label = tk.Label(self, text="Select Language to Translate to:")
        self.lang_label.grid(row=4, column=0, padx=padding, pady=padding)
        self.lang_var = tk.StringVar()
        self.lang_var.set("Hindi")
        self.lang_menu = tk.OptionMenu(self, self.lang_var,"Hindi","Kannada","malayalam","telgu","Japanese","Tamil","Bengali","Russian","Urdu")
        self.lang_menu.grid(row=4, column=1, padx=padding, pady=padding)

    
    def upload_image(self):
        # Open a file dialog to select an image file
        filetypes = [("Image files", "*.png;*.jpg;*.jpeg")]
        file_path = tk.filedialog.askopenfilename(filetypes=filetypes)

        # Use pytesseract to recognize text from the image
        if file_path:
            try:
                image = Image.open(file_path)
                text = pytesseract.image_to_string(image)
                self.image_text_label.config(text="Recognized text: " + text)
                print(text)
                


                # Translate the recognized text
                text_to_translate = self.translator.translate(text, src=self.from_lang, dest=self.to_lang)
                translation = text_to_translate.text
                self.text_box.insert(tk.END, "Output: " + translation + "\n")
                print(self.from_lang, self.to_lang)
                

                # Speak the translated text
                print(self.from_lang, self.to_lang)
                speak = gTTS(text=translation, lang=self.to_lang, slow=False)
                speak.save("translated_voice.mp3")
                os.system("start translated_voice.mp3")
                self.status_label.config(text="Status: Translation Completed")

            except OSError as e:
                self.status_label.config(text=f"Status: Unable to open image file: {e}")

            except spr.RequestError as e:
                self.status_label.config(text=f"Status: Unable to provide Required Output: {e}")
            
    def say_hello(self):
        with self.mic as source:
            self.status_label.config(text="Status: Speak 'Hello' to initiate the Translation")
            self.recog.adjust_for_ambient_noise(source, duration=0.2)
            audio = self.recog.listen(source)
            hello_text = self.recog.recognize_google(audio)
            hello_text = hello_text.lower()

        if 'hello' in hello_text:
            self.status_label.config(text="Status: Speak a Sentence to be Translated")

    def speak_sentence(self):
        with self.mic as source:
            self.recog.adjust_for_ambient_noise(source, duration=0.2)
            audio = self.recog.listen(source)
            self.sentence_to_translate = self.recog.recognize_google(audio)
            self.text_box.insert(tk.END, "Input: " + self.sentence_to_translate + "\n")

        try:
            # Get the selected language from the dropdown menu
            lang = self.lang_var.get()
            if lang == "Hindi":
                self.to_lang = "hi"
            elif lang == "Kannada":
                self.to_lang = "kn"
            elif lang == "malayalam":
                self.to_lang = "ml"
            elif lang == "Japanese":
                self.to_lang = "ja"
            elif lang == "Tamil":
                self.to_lang = "ta"
            elif lang == "Bengali":
                self.to_lang = "bn"
            elif lang == "Russian":
                self.to_lang = "ru"
            elif lang == "Urdu":
                self.to_lang = "ur"
            elif lang == "telgu":
                self.to_lang = "te"
            


            text_to_translate = self.translator.translate(self.sentence_to_translate, src=self.from_lang,
                                                           dest=self.to_lang)
            text = text_to_translate.text
            self.text_box.insert(tk.END, "Output: " + text + "\n")
            
            speak = gTTS(text=text, lang=self.to_lang, slow=False)
            speak.save("captured_voice.mp3")
            os.system("start captured_voice.mp3")
            self.status_label.config(text="Status: Translation Completed")

        except spr.UnknownValueError:
            self.status_label.config(text="Status: Unable to Understand the Input")

        except spr.RequestError as e:
            self.status_label.config(text=f"Status: Unable to provide Required Output: {e}")


root = tk.Tk()
app = TranslatorApp(master=root)
app.mainloop()
