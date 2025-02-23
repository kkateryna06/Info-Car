# Info-Car

## How to Run the Project

### 1. Fill in the configuration file: Open the _config.txt_ file and fill in the following lines:  

**TELEGRAM_TOKEN = 'your_telegram_token'** - The Telegram bot token you get from BotFather  

**CHAT_ID = 'your_chat_id'**               - Your chat ID in Telegram where the bot will send messages 

**LOGIN = 'your_login'**                   - The login you use on the website https://info-car.pl 

**PASSWORD = 'your_password'**             - The password for your account on https://info-car.pl  

### 2. Install dependencies: Make sure you have all the necessary libraries installed. You can do this by running:  

**pip install -r requirements.txt**

### 3. Run the project: To run the project, simply use the command:

**python main.py**

## Code Description
The script runs every 15 minutes to fetch the nearest exam date from info-car.pl. If the exam is within the next 25 days, it sends a Telegram notification to the user with the exam date.