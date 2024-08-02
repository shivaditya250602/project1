import tkinter as tk
from tkinter import messagebox
import speech_recognition as sr
import threading

class SpeechToTextApp:
    def __init__(self, master):
        self.master = master
        master.title("Speech to Text")
        master.geometry("400x300")
        master.configure(bg="black")
        
        self.label = tk.Label(master, text="Click 'Start' to begin speech recognition",background='green',foreground='dark blue')
        self.label.pack(pady=10)

        self.text_area = tk.Text(master, height=10, width=50,background='black',foreground='white')
        self.text_area.pack(pady=10)

        self.start_button = tk.Button(master, text="Start", command=self.start_recognition,background='red',foreground='white')
        self.start_button.pack(pady=5)

        self.stop_button = tk.Button(master, text="Stop", command=self.stop_recognition, state=tk.DISABLED,background='red',foreground='white')
        self.stop_button.pack(pady=5)
       
        self.exit_button = tk.Button(master,text="Exit",command=self.exiting,background='red',foreground='white')
        self.exit_button.pack(pady=5)
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.is_listening = False

    def start_recognition(self):
        self.is_listening = True
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.label.config(text="Listening... Speak now")

        thread = threading.Thread(target=self.recognize_speech)
        thread.start()

    def stop_recognition(self):
        self.is_listening = False
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.label.config(text="Click 'Start' to begin speech recognition")

    def recognize_speech(self):
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source)

            while self.is_listening:
                try:
                    audio = self.recognizer.listen(source, timeout=5)
                    text = self.recognizer.recognize_google(audio)
                    self.text_area.insert(tk.END, text + "\n")
                except sr.WaitTimeoutError:
                    pass
                except sr.UnknownValueError:
                    pass
                except sr.RequestError as e:
                    messagebox.showerror("API Error", f"Could not request results from Google Speech Recognition service; {e}")
                    self.stop_recognition()
    def exiting(self):
        exit()
if __name__ == "__main__":
    root = tk.Tk()
    app = SpeechToTextApp(root)
    root.mainloop()