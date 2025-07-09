

# Job-Hunter


**Job Hunter** is a telegram bot searches multiple job boards  in real-time, scrapes relevant job postings, and compiles them into a clean, organized list. Why? Because its seamless and requires no login and that too without switching apps. Here is the Source code of the bot. It helps users discover job postings directly on Telegram. It fetches listings from multiple websites, applies filters, and presents clean results in chat.

---

## ⚙️ Features

- ✅ Search jobs by keyword, location and company.
- ✅ Pagination to browse results.
- ✅ Logging and error handling.
- ✅ Abort command anytime by `ReplyKeyboardButton`
---

## 🚀 Installation / Setup

Clear instructions on how to run it locally:
```
git clone https://github.com/pradeep-lit/Job-Hunter.git
cd Job-Hunter
pip install -r requirements.txt
```
Then, add your bot token (you can find it from [here](https://telegram.me/BotFather)) into `main.py` directly or using dotenv by just creating the `.env` file into the project folder and adding your token into the file.

Finally, run:
```
python main.py
```
---

## 💡 Usage

Command:
> /start — Start the bot
> /remotive — Search jobs on Remotive
> /internshala — Search jobs on Internshala
> /naukri — Search jobs on Naukri
---

## 🙏 Acknowledgments

- Libraries : `requests, python-dotenv, python-telegram-bot, bs4, ua-generator`
- Python
