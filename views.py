from ttkbootstrap import Label, Labelframe
from settings import *
from base_app import BaseApp


class MainApp(BaseApp):

    def __init__(self):
        super().__init__()

        self.current_widget_frame = Labelframe(
            bootstyle="warning",
            text=" Current Widget "
         )
        self.current_widget_frame.grid(
            column=0, 
            row=1, 
            padx=50, 
            pady=25, 
            columnspan=7, 
            rowspan=7, 
            sticky="nsew"
        )

        self.home_page_description = Label(
            self.current_widget_frame,
            bootstyle="info",
            text="Welcome!",
            font=(FONT_STYLE, 16)
        )
        self.home_page_description.grid(padx=20, pady=20, sticky="nw")