# Info-Car

## How to Run the Project

### 1. Fill in the configuration file: Open the _config.txt_ file and fill in the following lines:  
> All values in the config.txt file must be enclosed in single quotes ('') and written with the correct letter case

**CHROME_DRIVER_PATH = 'your_chromedriver_path'** - The path to the chromedriver.exe file on your computer

#### Telegram-related variables
**TELEGRAM_TOKEN = 'your_telegram_token'** - The Telegram bot token you get from BotFather  

**CHAT_ID = 'your_chat_id'**               - Your chat ID in Telegram where the bot will send messages 

#### Login credentials for Info-Car
**LOGIN = 'your_login'**                   - The login you use on the website https://info-car.pl 

**PASSWORD = 'your_password'**             - The password for your account on https://info-car.pl  

#### Bot settings
**THEORETICAL_TERMS = 'True'**             - If set to 'True', the bot will check and send available dates for the theoretical exam

**AUTO_BOOKING = 'True'**                  - If set to 'True', the bot will automatically book the exam when a suitable slot is found

**THEORETICAL_EXAM_ALERT_THRESHOLD = '7'** - The threshold in days for triggering an exam notification

**PRACTICAL_EXAM_ALERT_THRESHOLD = '14'**  - The threshold in days for triggering an exam notification

#### Personal details for exam registration
**FIRST_NAME = 'Name'**                    - Your first name

**LAST_NAME = 'Holub'**                    - Your last name

**PESEL = '12345'**                        - Your PESEL number

**PKK = '12345'**                          - Your PKK

**CATEGORY = 'b'**                         - The driving license category

**EMAIL = 'email@gmail.com'**              - Your email address

**PHONE_NUMBER = '12345'**                 - Your phone number

**PROVINCE = 'dolnośląskie'**              - The province in Poland where you want to take the exam. (The correct name should be verified on info-car.pl to avoid errors)

**WORD = 'word-wrocław'**                  - The specific exam center, WORD. (The correct name should be verified on info-car.pl to avoid errors)

### 2. Install dependencies: Make sure you have all the necessary libraries installed. You can do this by running:  

**pip install -r requirements.txt**

### 3. Run the project: To run the project, simply use the command:

**python main.py**

## Code Description
The script runs at a frequency depending on the time of day to fetch the nearest exam dates from info-car.pl.
The user can configure the number of days in advance to receive notifications.
Additionally, if auto-booking is enabled, the script will attempt to register the user for the earliest available _practice_ exam date that meets the set conditions.
The process will stop at the payment step, keeping the browser window open and waiting for the user to complete the transaction manually.

Before running the script, you need to download the ChromeDriver compatible with your version of Google Chrome. https://developer.chrome.com/docs/chromedriver/downloads/version-selection

<span style="color: red;">Warning:</span>

1. Ensure that all user data is entered correctly; otherwise, the script will not be able to book an exam.
2. Check the exact spelling of your province (województwo) and WORD (ośrodek egzaminacyjny) on the info-car.pl and enter them in the corresponding fields, preserving the letter case.