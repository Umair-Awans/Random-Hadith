# 📚 Random Hadith Fetcher (Multithreaded with Clean Output)

A simple yet powerful Python script that fetches random Hadiths from [HadithAPI](https://hadithapi.com/) using a **producer-consumer threading model**. The displayed Hadiths are well-formatted for clarity, and only valid (complete) ones are shown.

---

## ✨ Features

- 🧵 Multithreaded design: Producer fetches data, Consumer displays it
- ✅ Only **complete Hadiths** are shown (with Heading, Narrator, Text, Book/Chapter Info, and Status)
- 📦 Clean output format with **headings** for better readability
- 🔁 User can browse multiple Hadiths in one session, or exit anytime
- ⚠️ Handles missing API keys and connection errors gracefully
- 📉 Informs the user if **no valid Hadiths** were found in the session

---

## 🧠 How It Works

- **Producer Thread:**  
  Fetches Hadiths from `NUM_PAGES` random pages using the HadithAPI and puts individual Hadiths into a queue.

- **Consumer Thread:**  
  Pulls Hadiths from the queue one-by-one, validates them, and displays them with a readable format.  
  User can press Enter to see more, or type `n` to exit early.

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/Umair-Awans/Random-Hadith.git
cd Random-Hadith

2. Install Dependencies

Only one external package is needed:

pip install requests

🔐 API Key Setup

    Go to HadithAPI.com and sign up for a free API key

    Save your key in a file named:

API_KEY.txt

▶️ Running the Script

python main.py

    You’ll see a cleanly formatted Hadith

    Press Enter to view more, or type n to quit

📌 Example Output

==================================================

Heading: Excellence of Performing Wudu Perfectly

Narrator:
Abu Hurairah (RA)

📖 Hadith: The Messenger of Allah (ﷺ) said: "When a Muslim or a believer washes his face..."

📚 Book: Sahih Muslim
📂 Chapter 2: Ablution
✅ Status: Sahih

==================================================


✅ Future Ideas

    Add search or filter options (by Book, Narrator, Topic)

    Convert to GUI using PyQt5

    Save favorite Hadiths to a file

    Add support for Hadiths in Arabic

📜 License

MIT License – free to use and modify with attribution.

Made with ❤️ by Umair


---
