from ttkbootstrap import Window, Label, Labelframe, Button, Style
from settings import *
from frames import *


class BaseApp(Window):

    def __init__(self):
        super().__init__(themename="darkly")

        self.title("The Irby Personal Assistant")
        self.iconbitmap("assets/logo.ico")
        self.geometry(f"{SCREEN_WIDTH}x{SCREEN_HEIGHT}")

        self.columnconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8, 9), weight=1)
        self.rowconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8), weight=1)

        self.welcome_message_frame = Labelframe(
            text=" Powered by Chase ",
            style="warning.TLabelframe"
        )
        self.welcome_message_frame.grid(row=0, column=0, padx=25, pady=25, sticky="nw", columnspan=6)

        self.welcome_message = Label(
            self.welcome_message_frame,
            text="IPA - The Irby Personal Assistant",
            font=(FONT_STYLE, 22), 
            bootstyle="warning"
        )
        self.welcome_message.grid(row=0, column=0, padx=25, pady=15)


        self.tools_frame = Labelframe(style="warning.TLabelframe", text=" Tools ")
        self.tools_frame.grid(
            column=8, 
            row=0, 
            padx=35, 
            pady=25, 
            columnspan=2, 
            rowspan=8, 
            sticky="nsew"
        )
        self.tools_frame.columnconfigure((0, 1, 2), weight=1)
        self.tools_frame.rowconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8, 9), weight=1)

        self.button_list = [
            "", 
            "", 
            "MXK Help", 
            "Juniper Help",
            "Tech Troubleshooting", 
            "Helpful IPs", 
            "Other Tool", 
            "Other Tool", 
            "Other Tool", 
            "Other Tool", 
            "Other Tool"
            ]

        self.tool_button_style = Style()
        self.tool_button_style.configure("info.Outline.TButton", font=(FONT_STYLE, 12))

        self.pinger_button = Button(
                self.tools_frame,
                bootstyle="info.Outline.TButton",
                text=" Continuous Ping ",
                cursor="hand2",
                command= lambda: PingerFrame().tkraise()
        )
        self.pinger_button.grid(row=0, column=0, columnspan=3, sticky="nsew", pady=25, padx=40)

        self.monitor_buddy_button = Button(
            self.tools_frame,
            bootstyle="info.Outline.TButton",
            text=" Monitor Buddy ",
            cursor="hand2",
            command= lambda: MonitorBuddyFrame().tkraise()
        )
        self.monitor_buddy_button.grid(row=1, column=0, columnspan=3, sticky="nsew", pady=25, padx=40)

        self.test_frame_button = Button(
            self.tools_frame,
            bootstyle="info.Outline.TButton",
            text=" Test Frame ",
            cursor="hand2",
            command= lambda: TestFrame().tkraise()
        )
        self.test_frame_button.grid(row=2, column=0, columnspan=3, sticky="nsew", pady=25, padx=40)

        for i in range(3, len(self.button_list) - 1):
            bname = self.button_list[i]
            temp = Button(
                self.tools_frame,
                bootstyle="info.Outline.TButton",
                text=f" {bname} ",
                cursor="hand2",
                command=lambda: TemporaryFrame().tkraise()
            )
            temp.grid(row=i, column=0, columnspan=3, sticky="nsew", pady=25, padx=40)

        
        self.monitor_buddy_button = Button(
            self.tools_frame,
            bootstyle="info.Outline.TButton",
            text=" Back to Dashboard ",
            cursor="hand2",
            command= lambda: WelcomeFrame().tkraise()
        )
        self.monitor_buddy_button.grid(row=len(self.button_list) - 1, column=0, columnspan=3, sticky="nsew", pady=25, padx=40)

        WelcomeFrame().tkraise()
