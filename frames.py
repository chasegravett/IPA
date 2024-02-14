from ttkbootstrap import Labelframe, Label, Entry, Button
from settings import *
from subprocess import check_output
from time import sleep
from datetime import datetime
import threading
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions


class PingerFrame(Labelframe):
    def __init__(self):
        super().__init__(bootstyle="warning", text=" Pinger ")

        self.continue_pinging = True
        self.ERROR_MESSAGES = [
        "destination host unreachable.",
        "destination net unreachable.",
        "request timed out.",
        "ping request could not find host.",
        ]

        self.grid(
            column=0, 
            row=1, 
            padx=50, 
            pady=25, 
            columnspan=7, 
            rowspan=7, 
            sticky="nsew"
        )

        self.columnconfigure((0, 1, 2, 3, 4, 5), weight=1)
        self.rowconfigure((0, 1, 2, 3, 4), weight=1)

        self.description = Label(
            self,
            bootstyle="info",
            text=r"      Start a Continuous Ping      ",
            font=(FONT_STYLE, 14)
        )
        self.description.grid(column=1, row=0, columnspan=4, padx=20, pady=20, sticky="new")


        self.ip_address_label = Label(
            self,
            bootstyle="warning",
            text="I.P. Address",
            font=(FONT_STYLE, 10)
        )
        self.ip_address_label.grid(padx=65, column=0, row=1, sticky="sw")
        self.ip_address = Entry(
            self,
            bootstyle="info",
            text="I.P. Address"
        )
        self.ip_address.grid(padx=60, pady=20, column=0, row=2, sticky="nw")


        self.seconds_label = Label(
            self,
            bootstyle="warning",
            text="How many seconds?",
            font=(FONT_STYLE, 10)
        )
        self.seconds_label.grid(padx=60, column=1, row=1, sticky="sw")
        self.seconds = Entry(
            self,
            bootstyle="info"
        )
        self.seconds.grid(padx=60, pady=20, column=1, row=2, sticky="nw")


        self.ip_address_button = Button(
            self,
            bootstyle="info-outline",
            text="Start Ping",
            cursor="hand2",
            command=threading.Thread(target=self.ping_ip).start
        )
        self.ip_address_button.grid(pady=20, column=2, row=2, sticky="nw")


        self.stop_ping_button = Button(
            self,
            bootstyle="info-outline",
            text="Stop Ping",
            cursor="hand2",
            command=self.stop_ping
        )
        self.stop_ping_button.grid(pady=20, column=3, row=2, sticky="nw")


        self.temp = Label(
            self,
            bootstyle="warning",
            text="\n\n",
            font=(FONT_STYLE, 12)
        )
        self.temp.grid(row=3, column=1, columnspan=3, sticky="sew")


        self.ceased = Label(
            self,
            bootstyle="danger",
            text="   ",
            font=(FONT_STYLE, 12)
        )
        self.ceased.grid(pady=20, row=4, column=1, columnspan=3, sticky="new")


    def ping_ip(self):
        self.ceased.config(text="")
        address = self.ip_address.get()
        try:
            seconds = int(self.seconds.get())
        except:
            seconds = float(self.seconds.get())

        while self.continue_pinging:
            values = str(check_output(f"ping {address} -n 1")).strip().split(r"\r\n")
            response = values[2].split(": ")[1]
            now = datetime.now().strftime("%H : %M : %S")
            
            if response.lower().strip() in self.ERROR_MESSAGES:
                self.temp.config(bootstyle="danger", text=f"Error occurred with ping to {address} at  {now} .\nResponse info: {response}\n\tCeasing ping")
                self.continue_pinging = False
            else:
                self.temp.config(bootstyle="success", text=f"Ping to {address} at  {now}  was successful.\nResponse info: {response}\nNext ping in {seconds} seconds.")
                sleep(seconds)


    def stop_ping(self):
        if self.continue_pinging:
            self.continue_pinging = False
            self.temp.config(bootstyle="warning")
            self.ceased.config(text="Ping Cancelled")

class MonitorBuddyFrame(Labelframe):
    def __init__(self):
        super().__init__(bootstyle="warning", text=" Monitor Buddy ♡ ")

        self.url = "http://100.67.114.250/alert-log"
        self.newest_alert_xpath = "//*[@id=\"alertlog\"]/tbody/tr[1]"

        self.browser = self.launch_browser()

        self.grid(
            column=0, 
            row=1, 
            padx=50, 
            pady=25, 
            columnspan=7, 
            rowspan=7, 
            sticky="nsew"
        )

        self.columnconfigure((0, 1, 2, 3, 4, 5), weight=1)
        self.rowconfigure((0, 1, 2, 3, 4), weight=1)

        self.description = Label(
            self,
            bootstyle="info",
            text="Enter Your Libre Credentials",
            font=(FONT_STYLE, 16)
        )
        self.description.grid(column=1, row=0, columnspan=4, padx=20, pady=20, sticky="new")


        self.username_label = Label(
            self,
            bootstyle="warning",
            text="Username",
            font=(FONT_STYLE, 10)
        )
        self.username_label.grid(padx=65, column=0, row=1, sticky="sw")
        self.username = Entry(
            self,
            bootstyle="info"
        )
        self.username.grid(padx=60, pady=20, column=0, row=2, sticky="nw")


        self.password_label = Label(
            self,
            bootstyle="warning",
            text="Password",
            font=(FONT_STYLE, 10)
        )
        self.password_label.grid(padx=60, column=1, row=1, sticky="sw")
        self.password = Entry(
            self,
            bootstyle="info",
            show="*"
        )
        self.password.grid(padx=60, pady=20, column=1, row=2, sticky="nw")


        self.login_button = Button(
            self,
            bootstyle="info-outline",
            text="Login to begin Monitoring",
            cursor="hand2",
            command=self.login
        )
        self.login_button.grid(pady=20, column=2, row=2, columnspan=2, sticky="nw")


        self.temp = Label(
            self,
            bootstyle="danger",
            text="\n\n",
            font=(FONT_STYLE, 12)
        )
        self.temp.grid(row=3, column=1, columnspan=3, sticky="ew")


    def launch_browser(self):
        options = ChromeOptions()
        options.add_experimental_option("detach", True)
        options.add_argument("--headless")
        driver = Chrome(options=options, service=Service(ChromeDriverManager().install()))
        driver.get(self.url)
        return driver
    
    def login(self):
        self.temp.config(bootstyle="success", text="Logging in...")
        uname = self.username.get()
        pword = self.password.get()

        self.browser.find_element(By.NAME, "username").send_keys(uname)
        self.browser.find_element(By.NAME, "password").send_keys(pword)
        self.browser.find_element(By.CSS_SELECTOR, ".btn-primary").click()
        sleep(1)

        try:
            a = self.browser.find_element(By.NAME, "username").is_displayed()
            b = self.browser.find_element(By.NAME, "password").is_displayed()
        except NoSuchElementException:
            self.logged_in()
        else:
            self.temp.config(bootstyle="danger", text="Invalid Credentials")
            self.browser.refresh()
            sleep(2)

    def logged_in(self):
        MonitoringActiveFrame(self.browser).tkraise()


class MonitoringActiveFrame(Labelframe):
    def __init__(self, browser):
        super().__init__(bootstyle="warning", text=" Monitor Buddy ♡ ")

        self.browser = browser
        self.newest_alert_xpath = "//*[@id=\"alertlog\"]/tbody/tr[1]"
        self.main_thread = threading.Thread(target=self.get_data)
        self.stop_thread = False

        self.grid(
            column=0, 
            row=1, 
            padx=50, 
            pady=25, 
            columnspan=7, 
            rowspan=7, 
            sticky="nsew"
        )

        self.columnconfigure((0, 1, 2, 3, 4, 5), weight=1)
        self.rowconfigure((0, 1, 2, 3, 4), weight=1)

        self.description = Label(
            self,
            bootstyle="info",
            text="Succesfully logged into Monitor Buddy for FECC",
            font=(FONT_STYLE, 16)
        )
        self.description.grid(column=0, row=0, columnspan=4, padx=50, pady=40, sticky="sew")

        self.begin_button = Button(
            self,
            bootstyle="info-outline",
            text="Click to begin easy monitoring",
            cursor="hand2",
            command=self.change_button
        )
        self.begin_button.grid(column=1, row=1, columnspan=2, sticky="new")

        self.recent_alert_frame = Labelframe(
            self,
            bootstyle="info.TLabelframe",
            text=" Most Recent Alert "
        )
        self.recent_alert_frame.grid(column=0, row=2, columnspan=4, rowspan=3, padx=50, pady=50, sticky="nsew")
        self.recent_alert_frame.columnconfigure((0, 1, 2, 3, 4), weight=1)
        self.recent_alert_frame.rowconfigure((0, 1, 2, 3), weight=1)


    def change_button(self):
        if self.begin_button.cget("text") == "Click to begin easy monitoring":
            self.begin_button.config(text = "Click to end easy monitoring")
            self.main_thread.start()
        else:
            self.begin_button.config(text = "Click to begin easy monitoring")
            self.stop_thread = True

    
    def get_data(self):
        pass


class TemporaryFrame(Labelframe):
    def __init__(self):
        super().__init__(bootstyle="warning", text=" Placeholder Frame ")

        self.grid(
            column=0, 
            row=1, 
            padx=50, 
            pady=25, 
            columnspan=7, 
            rowspan=7, 
            sticky="nsew"
        )

        self.columnconfigure((0, 1, 2, 3, 4, 5), weight=1)
        self.rowconfigure((0, 1, 2, 3, 4), weight=1)

        self.description = Label(
            self,
            bootstyle="info",
            text=r"   This function is coming soon!   ",
            font=(FONT_STYLE, 14)
        )
        self.description.grid(column=1, row=0, columnspan=4, padx=20, pady=20, sticky="new")


class WelcomeFrame(Labelframe):
    def __init__(self):
        super().__init__(bootstyle="warning", text=" Dashboard ")

        self.grid(
            column=0, 
            row=1, 
            padx=50, 
            pady=25, 
            columnspan=7, 
            rowspan=7, 
            sticky="nsew"
        )

        self.columnconfigure((0, 1, 2, 3, 4, 5), weight=1)
        self.rowconfigure((0, 1, 2, 3, 4), weight=1)

        self.description = Label(
            self,
            bootstyle="info",
            text=r"             Welcome!              ",
            font=(FONT_STYLE, 14)
        )
        self.description.grid(column=1, row=0, columnspan=4, padx=20, pady=20, sticky="new")