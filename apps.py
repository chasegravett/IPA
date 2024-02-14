import customtkinter
from settings import *

class MainApp(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.geometry(f"{SCREEN_WIDTH}x{SCREEN_HEIGHT}")
        self.title("IPA - the Irby Personal Assistant")
        self.grid_columnconfigure(0, weight=1)

        self.button = customtkinter.CTkButton(self, text="Click me!", command=self.button_callback)
        self.button.grid(row=0, column=0, padx=20, pady=20)

    
    def button_callback(self):
        print("Button pressed")