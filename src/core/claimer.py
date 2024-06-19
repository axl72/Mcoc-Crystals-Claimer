from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException
import locale
import time
import logging

logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def create_options() -> Options:
    opts = Options()
    opts.add_argument("--incognito")
    opts.add_argument("--start-maximized")
    opts.add_argument("--lang=es-EC")
    opts.add_argument(
        "user_agent='Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'"
    )
    opts.add_argument("--window-size=1366,768")
    opts.add_experimental_option(
        "prefs",
        {
            "download.default_directory": "",
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True,
        },
    )
    # opts.add_argument("--headless")  # Ejecuta en modo headless
    # opts.add_argument(
    # "--disable-gpu"
    # )  # Deshabilita la GPU (recomendado en modo headless)
    # opts.add_argument("--no-sandbox")  # Bypass OS security model
    # opts.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems
    return opts


class Claimer:
    def __init__(self, url: str, driver_path: str, email: str, password: str):
        self.url = url
        self.opts = create_options()
        self.service = Service()
        self.email = email
        self.password = password

    def claim_crystals(self):
        def find_element(condition):
            return WebDriverWait(driver, 25).until(
                EC.presence_of_element_located(condition)
            )

        locale.setlocale(locale.LC_TIME, "es_ES.UTF-8")

        driver = webdriver.Chrome(service=self.service, options=self.opts)
        driver.get(self.url)

        login_button = driver.find_element(By.CLASS_NAME, "login-button__text")
        login_button.click()
        iframe = driver.find_element(
            By.XPATH, '//iframe[contains(@src, "login-widget.xsolla.com/latest")]'
        )
        driver.switch_to.frame(iframe)
        continue_button = WebDriverWait(driver, 25).until(
            EC.presence_of_element_located(
                (By.CLASS_NAME, "login-form__primary-social__text")
            )
        )

        continue_button.click()

        driver.switch_to.window(driver.window_handles[-1])

        email_input = WebDriverWait(driver, 25).until(
            EC.presence_of_element_located((By.NAME, "email"))
        )

        email_input.send_keys(self.email)

        password_input = find_element((By.NAME, "password"))
        password_input.send_keys(self.password)

        submit_button = find_element((By.ID, "submit-button"))
        submit_button.click()

        input()
        driver.switch_to.window(driver.window_handles[0])

        # input()
        # acept_button = find_element((By.CLASS_NAME, "primary-social_button"))
        # acept_button.click()

        daily_crystal_button = WebDriverWait(driver, 50).until(
            EC.presence_of_element_located(
                (
                    By.ID,
                    "store-buy-button-6584994c6e497a772a787de4-0-com.kabam.marvel.dailyval.xs.free.000",
                )
            ),
        )
        try:
            driver.execute_script(
                "arguments[0].scrollIntoView();", daily_crystal_button
            )
            daily_crystal_button.click()
            driver.find_element(By.ID, "free-item-modal")
        except Exception as e:
            print(e)

        try:
            weekly_webstore_button = driver.find_element(
                By.ID,
                "store-buy-button-6584994c6e497a772a787de4-0-com.kabam.marvel.weeklyweb.xs.free.000",
            )

            driver.execute_script(
                "arguments[0].scrollIntoView();", weekly_webstore_button
            )
            weekly_webstore_button.click()
        except:
            pass
        logger("Process fineshed successfuly")
        driver.quit()
