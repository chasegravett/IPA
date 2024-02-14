from secret import username, password
from time import sleep
from winsound import PlaySound
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions



url = "http://100.67.114.250/alert-log"
newest_alert_xpath = "//*[@id=\"alertlog\"]/tbody/tr[1]"



def main():
    new_driver = launch_browser()
    new_driver.find_element(By.NAME, "username").send_keys(username)
    new_driver.find_element(By.NAME, "password").send_keys(password)
    new_driver.find_element(By.CSS_SELECTOR, ".btn-primary").click()
    
    last_device = ""
    last_alert = ""

    while True:
        try:
            WebDriverWait(new_driver, 20).until(expected_conditions.presence_of_element_located((By.XPATH, newest_alert_xpath)))
            newest_entry = new_driver.find_element(By.XPATH, newest_alert_xpath)
        except:
            print("failed")
            break
        else:
            data = newest_entry.text
            if data == 'Loading...':
                print("Loading. Trying again...")
                sleep(2)
            else:
                entries = [entry for entry in data.split("\n") if entry != ""]
                timestamp, device, rest = entries

                raw_alert = rest.split(" ")
                severity = raw_alert.pop()
                formatted_alert = " ".join(raw_alert)

                alert_string = f"""\n\tAlert Info:
                Timestamp: {timestamp}
                Device Name: {device}
                Alert: {formatted_alert}
                Severity: {severity}\n"""

                if formatted_alert != last_alert and device != last_device:
                    print(alert_string)
                    PlaySound("..\\assets\\audio\\C2FI_New_Alert.wav", 0)
                    last_alert = formatted_alert
                    last_device = device
                    print(f"Last alert changed to {last_alert}")
                    print(f"Last device changed to {last_device}")

                new_driver.refresh()
                sleep(10)
    
def launch_browser():
    options = ChromeOptions()
    options.add_experimental_option("detach", True)
    options.add_argument("--headless")
    driver = Chrome(options=options, service=Service(ChromeDriverManager().install()))
    driver.get(url)
    return driver



if __name__ == "__main__":
    main()