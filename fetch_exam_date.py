import subprocess
import subprocess
import time

from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

from date import is_less_than_x_days


def get_exam_date(driver, wait, radio_label):
    # Locate and click the radio button
    radio_button = wait.until(
        EC.presence_of_element_located(
            (By.XPATH, f'//input[@type="radio"][@aria-label="{radio_label}"]')
        )
    )
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", radio_button)
    try:
        radio_button.click()
    except:
        driver.execute_script("arguments[0].click();", radio_button)

    # Retrieve the exam date
    term_element = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div.accordion-header h5.m-0")))
    term_text = term_element.text

    # Retrieve the exam time
    exam_times_element = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "p.exam-time span")))
    exam_times = [elem.text for elem in exam_times_element]
    cleaned_exam_times = [item for item in exam_times if item != ""]

    return term_text, cleaned_exam_times


def fetch_data(LOGIN, PASSWORD, THEORETICAL_OR_PRACTICE, word_info, CHROME_DRIVER_PATH, PRACTICAL_EXAM_ALERT_THRESHOLD, THEORETICAL_EXAM_ALERT_THRESHOLD, user_info = None, is_booking = False):
    chrome_driver_path = CHROME_DRIVER_PATH
    # service = Service(chrome_driver_path)
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.set_window_size(400, 800)

    try:
        driver.get("https://info-car.pl/new/prawo-jazdy/sprawdz-wolny-termin")
        wait = WebDriverWait(driver, 20)

        # Click login button
        login_prompt_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, '//button[.//span[text()="Zaloguj się, aby kontynuować"]]'))
        )
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", login_prompt_button)
        try:
            login_prompt_button.click()
        except:
            driver.execute_script("arguments[0].click();", login_prompt_button)

        # Enter login credentials
        email_input = wait.until(EC.presence_of_element_located((By.ID, "username")))
        email_input.send_keys(LOGIN)
        password_input = wait.until(EC.presence_of_element_located((By.ID, "password")))
        password_input.send_keys(PASSWORD)
        login_button = wait.until(EC.element_to_be_clickable((By.ID, "register-button")))
        login_button.click()

        # Select "Egzamin na prawo jazdy (PKK)"
        radio_button = wait.until(
            EC.presence_of_element_located(
                (By.XPATH, '//span[text()="Egzamin na prawo jazdy (PKK)"]//preceding::input[@type="radio"]')
            )
        )
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", radio_button)
        try:
            radio_button.click()
        except:
            driver.execute_script("arguments[0].click();", radio_button)

        # Select province
        province_input = wait.until(EC.visibility_of_element_located((By.ID, "province")))
        driver.execute_script("arguments[0].click();", province_input)
        province_list = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "ul.results")))
        dolnoslaskie_option = driver.find_element(By.ID, word_info["province"])
        driver.execute_script("arguments[0].click();", dolnoslaskie_option)

        # Select exam center
        organization_input = wait.until(EC.visibility_of_element_located((By.ID, "organization")))
        driver.execute_script("arguments[0].click();", organization_input)
        result_list = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "ul.results")))
        word_wroclaw_option = driver.find_element(By.ID, word_info["word"])
        driver.execute_script("arguments[0].click();", word_wroclaw_option)

        # Select category (B)
        category_input = wait.until(EC.visibility_of_element_located((By.ID, "category-select")))
        driver.execute_script("arguments[0].click();", category_input)
        result_list = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "ul.results")))
        b_option = driver.find_element(By.ID, word_info["category"])
        driver.execute_script("arguments[0].click();", b_option)

        # Click "Next"
        next_button = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "ic-ghost-button .ghost-btn")))
        driver.execute_script("arguments[0].click();", next_button)
        wait = WebDriverWait(driver, 20)


        a = 0
        while True:
            a += 1
            time.sleep(1)

            # For practice exam
            if THEORETICAL_OR_PRACTICE == "p":
                # Retrieve practice exam date
                exam_term = get_exam_date(driver, wait, "PRACTICE")
                print(f"Practice exam date: {exam_term}")

                if is_less_than_x_days(exam_term[0][-5:], PRACTICAL_EXAM_ALERT_THRESHOLD):
                    break
                else:
                    time.sleep(6)

            # For theoretical exam
            elif THEORETICAL_OR_PRACTICE == "t":
                # Retrieve theoretical exam date
                exam_term = get_exam_date(driver, wait, "THEORY")
                print(f"Theoretical exam date: {exam_term}")

                if is_less_than_x_days(exam_term[0][-5:], THEORETICAL_EXAM_ALERT_THRESHOLD):
                    break
                else:
                    time.sleep(6)


            button = driver.find_element(By.CSS_SELECTOR, "button.ghost-btn.back")
            driver.execute_script("arguments[0].click();", button)

            # Select "Egzamin na prawo jazdy (PKK)"
            radio_button = wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, '//span[text()="Egzamin na prawo jazdy (PKK)"]//preceding::input[@type="radio"]')
                )
            )
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", radio_button)
            try:
                radio_button.click()
            except:
                driver.execute_script("arguments[0].click();", radio_button)

            # Select category (B)
            category_input = wait.until(EC.visibility_of_element_located((By.ID, "category-select")))
            driver.execute_script("arguments[0].click();", category_input)
            result_list = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "ul.results")))
            b_option = driver.find_element(By.ID, word_info["category"])
            driver.execute_script("arguments[0].click();", b_option)

            # Click "Next"
            next_button = wait.until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, "ic-ghost-button .ghost-btn")))
            driver.execute_script("arguments[0].click();", next_button)
            wait = WebDriverWait(driver, 20)


        if not is_booking:
            return exam_term


        message = (f"!!REJESTRACJA NA EGZAMIN PRAKTYCZNY\n"
                   f"DATA: {exam_term[0]}, {exam_term[1][0]}")
        subprocess.run(["python", "message.py", message])

        try:
            mobile_select = wait.until(
                EC.element_to_be_clickable((By.XPATH, '//div[@aria-label="Rozwijana lista"]'))
            )
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", mobile_select)
            time.sleep(1)

            try:
                mobile_select.click()
            except Exception as e:
                driver.execute_script("arguments[0].click();", mobile_select)

        except Exception as e:
            print(f"Error: {e}")

        confirm_button = driver.find_element(By.ID, "confirm-modal-btn")
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", confirm_button)
        time.sleep(1)
        driver.execute_script("arguments[0].click();", confirm_button)

        firstname_input = driver.find_element(By.ID, "firstname")
        firstname_input.send_keys(user_info["first_name"])

        firstname_input = driver.find_element(By.ID, "lastname")
        firstname_input.send_keys(user_info["last_name"])

        firstname_input = driver.find_element(By.ID, "pesel")
        firstname_input.send_keys(user_info["pesel"])

        firstname_input = driver.find_element(By.ID, "pkk")
        firstname_input.send_keys(user_info["pkk"])

        category_input = driver.find_element(By.ID, "category-select")
        category_input.send_keys(user_info["category"])
        category_input.send_keys(Keys.RETURN)

        firstname_input = driver.find_element(By.ID, "email")
        firstname_input.send_keys(user_info["email"])

        firstname_input = driver.find_element(By.ID, "phoneNumber")
        firstname_input.send_keys(user_info["phone_number"])

        checkbox = driver.find_element(By.ID, "regulations-text")
        driver.execute_script("arguments[0].click();", checkbox)

        next_button = driver.find_element(By.XPATH, "//span[text()='Dalej']")
        driver.execute_script("arguments[0].scrollIntoView(true);", next_button)
        time.sleep(1)
        next_button.click()

        next_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "next-btn")))
        next_button.click()

        time.sleep(2)

        button = driver.find_element(By.ID, "next-btn")
        driver.execute_script("arguments[0].scrollIntoView();", button)
        time.sleep(1)
        next_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "next-btn")))
        next_button.click()

        time.sleep(2)

        button = driver.find_element(By.XPATH, "//button[normalize-space()='Potwierdzam']")
        driver.execute_script("arguments[0].click();", button)

        time.sleep(2)

        input("Press any key...")
        return None


    except Exception as e:
        print(f"Error: {e}")

    finally:
        driver.quit()


