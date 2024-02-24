from ttkbootstrap import Labelframe, Label, Entry, Button
from settings import *
from datetime import datetime
from threading import Thread
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException, WebDriverException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions
from datetime import date, datetime
from time import sleep
from subprocess import check_output
from winsound import PlaySound, Beep
from os.path import isfile
from traceback import format_exc
from logging import error
from psutil import virtual_memory

def launch_browser(url):
    options = ChromeOptions()
    options.add_experimental_option("detach", True)
    options.add_argument("--headless")
    options.add_argument("disable-infobars")
    options.add_argument("--disable-extensions")
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-application-cache')
    options.add_argument('--disable-gpu')
    options.add_argument("--disable-dev-shm-usage")
    driver = Chrome(options=options, service=Service(ChromeDriverManager().install()))
    driver.execute_cdp_cmd("Network.setCacheDisabled", {"cacheDisabled":True})
    driver.get(url)
    return driver


def get_refresh_time(curr_minute):
    return curr_minute + 30 if curr_minute < 30 else curr_minute - 30


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
            command=self.to_ping_or_not_to_ping
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


    def to_ping_or_not_to_ping(self):
        address = self.ip_address.get()
        seconds = self.seconds.get()
        if self.is_valid_ip(address) and self.is_valid_interval(seconds):
            Thread(target=self.ping_ip).start()
        else:
            self.temp.config(bootstyle="danger", text=f"Invalid Entries\nIP Must use IPv4 Format. Ex: 127.0.0.1\nSeconds must be between 0.5s and 300")


    def is_valid_ip(self, address):
        nums = []
        octets = address.split(".")
        if len(octets) != 4:
            return False
        
        for octet in octets:
            try:
                nums.append(int(octet))
            except:
                return False
            
        for num in nums:
            if num < 0 or num > 255:
                return False
        
        return True
    

    def is_valid_interval(self, num):
        try:
            new_num = int(num)
        except ValueError:
            try:
                new_num = float(num)
            except:
                return False
        except:
            return False

        if new_num < 0.5 or new_num > 300:
            return False
        return True


    def stop_ping(self):
        if self.continue_pinging:
            self.continue_pinging = False
            self.temp.config(bootstyle="warning")
            self.ceased.config(text="Ping Cancelled")


class MonitorBuddyFrame(Labelframe):
    def __init__(self):
        super().__init__(bootstyle="warning", text=" Monitor Buddy ♡ ")

        # PLanning out implementation of monitoring multiple sites
        self.urls = {
            "FECC": "http://100.67.114.250/alert-log",      #Connect2First
            "LES": "http://100.93.114.250/alert-log",       #LexNet
            "CECC": "http://100.78.114.250/alert-log",      #Empower
            "CCECC": "http://100.77.114.250/alert-log"      #ClayCounty
        }

        # FECC
        self.url = "http://100.67.114.250/alert-log"
        self.newest_alert_xpath = "//*[@id=\"alertlog\"]/tbody/tr[1]"
        self.libre_password_path = "creds\\libre\\fecc.txt"
        self.browser = self.launch_browser()

        # Changing label used for invalid creds and logging in message
        self.temp = Label(
            self,
            bootstyle="danger",
            text="\n\n",
            font=(FONT_STYLE, 12)
        )
        self.temp.grid(row=3, column=1, columnspan=3, sticky="ew")

        if isfile(self.libre_password_path):
            with open(self.libre_password_path, "r") as file:
                u, p = file.readline().split(",")
            self.login(ex_user=u, ex_pass=p)
        else:
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


    def launch_browser(self):
        options = ChromeOptions()
        options.add_experimental_option("detach", True)
        options.add_argument("--headless")
        driver = Chrome(options=options, service=Service(ChromeDriverManager().install()))
        driver.get(self.url)
        return driver
    
    def login(self, ex_user=None, ex_pass=None):
        self.temp.config(bootstyle="success", text="Logging in...")
        uname = ex_user if ex_user else self.username.get()
        pword = ex_pass if ex_pass else self.password.get()

        self.browser.find_element(By.NAME, "username").send_keys(uname)
        self.browser.find_element(By.NAME, "password").send_keys(pword)
        self.browser.find_element(By.CSS_SELECTOR, ".btn-primary").click()
        sleep(1)
        
        try:
            a = self.browser.find_element(By.NAME, "username").is_displayed()
            b = self.browser.find_element(By.NAME, "password").is_displayed()
        except NoSuchElementException:
            self.logged_in(uname, pword)
        else:
            self.temp.config(bootstyle="danger", text="Invalid Credentials")
            self.browser.refresh()
            sleep(2)

    def logged_in(self, u, p):
        MonitoringActiveFrame(self.browser).tkraise()
        with open(self.libre_password_path, "w") as file:
            file.write(f"{u},{p}".strip())


class MonitoringActiveFrame(Labelframe):
    def __init__(self, browser):
        super().__init__(bootstyle="warning", text=" Monitor Buddy ♡ ")
        self.browser = browser
        self.newest_alert_xpath = "//*[@id=\"alertlog\"]/tbody/tr[1]"
        self.main_thread = Thread(target=self.get_data)
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

        self.timestamp_label = Label(
            self.recent_alert_frame,
            bootstyle="info",
            text="Timestamp: ",
            font=(FONT_STYLE, 10)
        )
        self.timestamp_label.grid(column=0, row=0, padx=25, sticky="nsw")

        self.timestamp = Label(
            self.recent_alert_frame,
            bootstyle="warning",
            text="",
            font=(FONT_STYLE, 12)
        )
        self.timestamp.grid(column=2, row=0, columnspan=3, padx=25, sticky="wns")

        self.device_label = Label(
            self.recent_alert_frame,
            bootstyle="info",
            text="Device: ",
            font=(FONT_STYLE, 10)
        )
        self.device_label.grid(column=0, row=1, padx=25, sticky="nsw")

        self.device = Label(
            self.recent_alert_frame,
            bootstyle="warning",
            text="",
            font=(FONT_STYLE, 12)
        )
        self.device.grid(column=2, row=1, columnspan=3, padx=25, sticky="wns")

        self.alert_label = Label(
            self.recent_alert_frame,
            bootstyle="info",
            text="Alert: ",
            font=(FONT_STYLE, 10)
        )
        self.alert_label.grid(column=0, row=2, padx=25, sticky="nsw")

        self.alert = Label(
            self.recent_alert_frame,
            bootstyle="warning",
            text="",
            font=(FONT_STYLE, 12)
        )
        self.alert.grid(column=2, row=2, columnspan=3, padx=25, sticky="wns")

        self.severity_label = Label(
            self.recent_alert_frame,
            bootstyle="info",
            text="Severity: ",
            font=(FONT_STYLE, 10)
        )
        self.severity_label.grid(column=0, row=3, padx=25, sticky="nsw")

        self.severity = Label(
            self.recent_alert_frame,
            bootstyle="warning",
            text="",
            font=(FONT_STYLE, 12)
        )
        self.severity.grid(column=2, row=3, columnspan=3, padx=25, sticky="wns")


    def change_button(self):
        button_text = self.begin_button.cget("text")
        if button_text == "Click to begin easy monitoring":
            self.begin_button.config(text = "Click to end easy monitoring")
            self.main_thread.start()
        elif button_text == "Click to end easy monitoring":
            self.begin_button.config(text = "Monitoring Ended. Click to re-launch buddy")
            self.stop_thread = True
            self.browser.quit()
        elif button_text == "Monitoring Ended. Click to re-launch buddy":
            self.begin_button.config(bootstyle="warning", text="Re-launching buddy. Please hold...")
            sleep(1)
            MonitorBuddyFrame().tkraise()

    
    def get_data(self):

        last_device = ""
        last_alert = ""
        while not self.stop_thread:
            time_to_sleep = 12
            try:
                WebDriverWait(self.browser, 20).until(expected_conditions.presence_of_element_located((By.XPATH, self.newest_alert_xpath)))
                newest_entry = self.browser.find_element(By.XPATH, self.newest_alert_xpath)
            except TimeoutException:
                print("\n\tTimed Out. Refreshing...\n")
            except WebDriverException as err:
                print(f"\n\tError encountered with Web Driver:\n\t\t{err}\n")
                self.stop_thread = True
            except Exception as e:
                print("\nUnknown Error:\n")
                error(format_exc(e))
                self.stop_thread = True
            else:
                data = newest_entry.text
                if data == 'Loading...':
                    time_to_sleep = 4
                else:
                    entries = [entry for entry in data.split("\n") if entry != ""]
                    timestamp, device, rest = entries
                    raw_alert = rest.split(" ")
                    severity = raw_alert.pop()
                    formatted_alert = " ".join(raw_alert)

                    if formatted_alert != last_alert or device != last_device:
                        self.update_display(timestamp, device, formatted_alert, severity)
                        PlaySound("assets\\audio\\FECC_new_alert.wav", 0)
                        last_alert = formatted_alert
                        last_device = device
            if not self.stop_thread:
                self.browser.refresh()
                sleep(time_to_sleep)
        #Gracefully shut down browser when breaking
        self.browser.close()
        self.browser.quit()
        


    def update_display(self, timestamp, device, alert, severity):
        self.timestamp.config(text=timestamp)
        self.device.config(text=device)
        self.alert.config(text=alert)
        self.severity.config(text=severity, bootstyle="danger" if severity == "critical" else "success")


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


class TinyMonitoringFrame(Labelframe):
    def __init__(self, parent, coop, start_column, start_row):
        super().__init__(parent, bootstyle="info.TLabelframe", text=f" {coop} ")
        
        self.urls = {
            "fecc": "http://100.67.114.250/alert-log",          #Connect2First
            "les": "http://100.93.114.250/alert-log",           #LexNet
            "empower": "http://100.78.114.250/alert-log",       #Empower
            "claycounty": "http://100.77.114.250/alert-log"     #ClayCounty
        }
        self.start_column = start_column
        self.start_row = start_row
        self.coop_unformatted = coop
        self.coop = coop.lower()
        self.url = self.urls[self.coop]
        self.libre_password_path = f"creds\\libre\\{self.coop}.txt"
        self.parent = parent

        self.grid(
            column = self.start_column,
            row = self.start_row,
            columnspan=3, 
            rowspan=5, 
            padx=40, 
            pady=40, 
            sticky="nsew"
        )
        self.columnconfigure((0, 1, 2), weight=1)
        self.rowconfigure((0, 1, 2, 3, 4), weight=1)

        if isfile(self.libre_password_path):
            with open(self.libre_password_path, "r") as file:
                u, p = file.readline().split(",")
            self.login(ex_user=u, ex_pass=p)
        else:
            self.description = Label(
                self,
                bootstyle="warning",
                text=f"Enter Libre Creds for {self.coop_unformatted}",
                font=(FONT_STYLE, 9)
            )
            self.description.grid(column=1, row=0, columnspan=3, pady=10, sticky="new")


            self.username_label = Label(
                self,
                bootstyle="warning",
                text="Username",
                font=(FONT_STYLE, 9)
            )
            self.username_label.grid(padx=15, pady=10, column=0, row=1, sticky="se")
            self.username = Entry(
                self,
                bootstyle="info"
            )
            self.username.grid(padx=15, pady=10, column=1, row=1, sticky="sw")


            self.password_label = Label(
                self,
                bootstyle="warning",
                text="Password",
                font=(FONT_STYLE, 9)
            )
            self.password_label.grid(padx=10, pady=10, column=0, row=2, sticky="se")
            self.password = Entry(
                self,
                bootstyle="info",
                show="*"
            )
            self.password.grid(padx=10, pady=10, column=1, row=2, sticky="sw")


            self.login_button = Button(
                self,
                bootstyle="info-outline",
                text="Login",
                cursor="hand2",
                command=self.login
            )
            self.login_button.grid(padx=40, pady=20, column=0, row=3, columnspan=3, sticky="e")

    
    def login(self, ex_user=None, ex_pass=None):
        self.browser = launch_browser(self.url)
        uname = ex_user if ex_user else self.username.get()
        pword = ex_pass if ex_pass else self.password.get()

        self.browser.find_element(By.NAME, "username").send_keys(uname)
        self.browser.find_element(By.NAME, "password").send_keys(pword)
        self.browser.find_element(By.CSS_SELECTOR, ".btn-primary").click()
        sleep(1)

        try:
            a = self.browser.find_element(By.NAME, "username").is_displayed()
            b = self.browser.find_element(By.NAME, "password").is_displayed()
        except NoSuchElementException:
            self.logged_in(uname, pword)
        else:
            self.temp.config(bootstyle="danger", text="Invalid Credentials")
            self.browser.refresh()
            sleep(2)

    def logged_in(self, u, p):
        TinyActiveFrame(self.parent, self.browser, self.coop_unformatted, self.start_column, self.start_row, self.url, u, p).tkraise()
        with open(self.libre_password_path, "w") as file:
            file.write(f"{u},{p}".strip())


class TinyActiveFrame(Labelframe):
    def __init__(self, parent, browser, coop, start_column, start_row, url, uname, pword):
        super().__init__(parent, bootstyle="info.TLabelframe", text=f" {coop} ")

        self.parent = parent
        self.browser = browser
        self.coop = coop
        self.start_column = start_column
        self.start_row = start_row
        self.url = url
        self.username = uname
        self.password = pword
        self.stop_thread = False
        self.newest_alert_xpath = "//*[@id=\"alertlog\"]/tbody/tr[1]"
        self.main_thread = Thread(target=self.get_data, daemon=True)

        self.alert_sounds = {
            "FECC": "assets\\audio\\FECC_new_alert.wav",            #Connect2First
            "LES": "assets\\audio\\LES_new_alert.wav",              #LexNet
            "Empower": "assets\\audio\\Empower_new_alert.wav",      #Empower
            "ClayCounty": "assets\\audio\\ClayCounty_new_alert.wav" #ClayCounty
        }
        self.months = [
            "Jan",
            "Feb",
            "Mar",
            "Apr",
            "May",
            "June",
            "July",
            "Aug",
            "Sep",
            "Oct",
            "Nov",
            "Dec"
        ]

        self.grid(
            column = self.start_column,
            row = self.start_row,
            columnspan=3, 
            rowspan=5, 
            padx=40, 
            pady=40, 
            sticky="nsew"
        )
        self.columnconfigure((0, 1, 2), weight=1)
        self.rowconfigure((0, 1, 2, 3, 4), weight=1)

        self.description = Label(
            self,
            bootstyle="info",
            text=f"Welcome to Monitor Buddy for {self.coop}",
            font=(FONT_STYLE, 10)
        )
        self.description.grid(column=0, row=0, columnspan=2, padx=20, pady=10, sticky="new")

        self.begin_button = Button(
            self,
            bootstyle="info-outline",
            text="Start",
            cursor="hand2",
            command=self.change_button
        )
        self.begin_button.grid(padx=30, pady=10, column=2, row=0, sticky="ne")

        self.timestamp_label = Label(
            self,
            bootstyle="info",
            text="Timestamp: ",
            font=(FONT_STYLE, 11)
        )
        self.timestamp_label.grid(column=0, row=1, pady=5, padx=25, sticky="nsw")

        self.timestamp = Label(
            self,
            bootstyle="warning",
            text="",
            font=(FONT_STYLE, 11)
        )
        self.timestamp.grid(column=1, row=1, columnspan=2, pady=5, padx=10, sticky="wns")

        self.device_label = Label(
            self,
            bootstyle="info",
            text="Device: ",
            font=(FONT_STYLE, 11)
        )
        self.device_label.grid(column=0, row=2, pady=5, padx=25, sticky="nsw")

        self.device = Label(
            self,
            bootstyle="warning",
            text="",
            font=(FONT_STYLE, 11)
        )
        self.device.grid(column=1, row=2, columnspan=2, pady=5, padx=10, sticky="wns")

        self.alert_label = Label(
            self,
            bootstyle="info",
            text="Alert: ",
            font=(FONT_STYLE, 11)
        )
        self.alert_label.grid(column=0, row=3, pady=5, padx=25, sticky="nsw")

        self.alert = Label(
            self,
            bootstyle="warning",
            text="",
            font=(FONT_STYLE, 11)
        )
        self.alert.grid(column=1, row=3, columnspan=2, pady=5, padx=10, sticky="wns")

        self.severity_label = Label(
            self,
            bootstyle="info",
            text="Severity: ",
            font=(FONT_STYLE, 11)
        )
        self.severity_label.grid(column=0, row=4, pady=5, padx=25, sticky="nsw")

        self.severity = Label(
            self,
            bootstyle="warning",
            text="",
            font=(FONT_STYLE, 11)
        )
        self.severity.grid(column=1, row=4, columnspan=2, pady=5, padx=10, sticky="wns")

    
    def change_button(self):
        button_text = self.begin_button.cget("text")
        if button_text == "Start":
            self.begin_button.config(text = "End")
            self.main_thread.start()
        elif button_text == "End":
            self.begin_button.config(text = "Ended. Relaunch?")
            self.stop_thread = True
            self.browser.quit()
        elif button_text == "Ended. Relaunch?":
            self.begin_button.config(bootstyle="warning", text="Please hold...")
            sleep(1)
            TinyMonitoringFrame(self.parent, self.coop, self.start_column, self.start_row).tkraise()


    def get_data(self):
        last_device = ""
        last_alert = ""
        while not self.stop_thread:
            current_memory_usage = virtual_memory()[2]      #int value of percentage used 
            time_to_sleep = 10
            try:
                WebDriverWait(self.browser, 20).until(expected_conditions.presence_of_element_located((By.XPATH, self.newest_alert_xpath)))
                newest_entry = self.browser.find_element(By.XPATH, self.newest_alert_xpath)
            except TimeoutException:
                print("Timed Out. Refreshing")
            except Exception as e:
                self.stop_thread = True
                error(format_exc(e))
            else:
                data = newest_entry.text
                if data == 'Loading...':
                    time_to_sleep = 4
                else:
                    entries = [entry for entry in data.split("\n") if entry != ""]
                    timestamp, device, rest = entries
                    raw_alert = rest.split(" ")
                    severity = raw_alert.pop()
                    formatted_alert = " ".join(raw_alert)

                    if formatted_alert != last_alert or device != last_device:
                        self.update_display(timestamp, device, formatted_alert, severity)
                        PlaySound(self.alert_sounds[self.coop], 0)
                        last_alert = formatted_alert
                        last_device = device
                        print(last_alert, last_device)
            
            if not self.stop_thread:
                if current_memory_usage >= 90:
                    print(f"\nCurrent Memory Usage: {current_memory_usage}%")
                    start_time_string = datetime.now().strftime("%H:%M:%S")
                    print(f"Initiating restart of browsers to keep memory usage low. Started at: {start_time_string}\n")
                    self.browser.quit()
                    sleep(3)
                    self.browser = launch_browser(self.url)
                    sleep(5)
                    self.login_after_restart()
                    sleep(2)
                    end_time_string = datetime.now().strftime("%H:%M:%S")
                    print(f"\nFull restart completed at: {end_time_string}")
                    print(f"New Memory Usage: {virtual_memory()[2]}%\n")
                    Beep(100, 1500)
                    Beep(100, 1500)

                else:
                    self.browser.refresh()
                    sleep(time_to_sleep)
        #Gracefully shut down browser when breaking
        self.browser.quit()

    def update_display(self, timestamp, device, alert, severity):
        my_date, time = timestamp.split(" ")
        year, month, day = my_date.split("-")
        hour, minute, second = time.split(":")
        month_word = self.months[int(month) - 1]
        hour = int(hour) if hour != "0" else 12
        if hour > 12:
            hour -= 12
            tense = "P.M."
        else:
            tense = "A.M."
        
        detected_date = str(date.today())
        if my_date == detected_date:
            self.timestamp.config(text=f"Today at {hour if hour != 0 else 12}:{minute} {tense}")
        else:
            self.timestamp.config(text=f"{month_word} {day}, {year} at {hour if hour != 0 else 12}:{minute} {tense}")

        self.device.config(text=device)
        self.alert.config(text=alert)
        self.severity.config(text=severity.upper(), bootstyle="danger" if severity == "critical" else "warning")

    def login_after_restart(self):
        self.browser.find_element(By.NAME, "username").send_keys(self.username)
        self.browser.find_element(By.NAME, "password").send_keys(self.password)
        self.browser.find_element(By.CSS_SELECTOR, ".btn-primary").click()
        sleep(1)


class MonitorBuddyEnhanced(Labelframe):
    def __init__(self):
        super().__init__(bootstyle="warning", text=" Monitor 4 at once? A bit overbearing but ok boss ")

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
        self.rowconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8, 9), weight=1)

        self.fecc_frame = TinyMonitoringFrame(self, "FECC", 0, 0)
        self.les_frame = TinyMonitoringFrame(self, "LES", 3, 0)
        self.empower_frame = TinyMonitoringFrame(self, "Empower", 0, 5)
        self.clay_frame = TinyMonitoringFrame(self, "ClayCounty", 3, 5)