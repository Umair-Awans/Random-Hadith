# 📚 Random Hadith Fetcher  
*A Multithreaded Python Tool with Clean Output*

A simple yet powerful Python script that fetches random Hadiths from [HadithAPI](https://hadithapi.com/) using a **producer-consumer threading model**. The displayed Hadiths are well-formatted, and only valid (complete) ones are shown.

---

## ✨ Features

- 🧵 **Multithreaded design**  
  Producer fetches Hadiths, Consumer displays them
- ✅ Only **complete Hadiths** are shown  
  (Heading, Narrator, Text, Book, Chapter, and Status)
- 📦 **Clean output** with headings
- 🔁 **Browse multiple Hadiths** in one session — press Enter to continue, or type `n` to quit
- 🔐 **Handles missing API key** automatically:
  - Launches HadithAPI in your browser
  - Reads API key from clipboard (`pyperclip`)
  - Validates and saves it
- 📉 Alerts you if **no valid Hadiths** are found

---

## 🧠 How It Works

### 🧵 Producer Thread
Fetches Hadiths from `NUM_PAGES` random pages using HadithAPI and puts each Hadith into a queue.

### 🧵 Consumer Thread
Reads Hadiths from the queue one-by-one, validates them, and displays formatted output to the user.

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/Umair-Awans/Random-Hadith.git
cd Random-Hadith
```
2. Install Dependencies

Install the required packages:

pip install requests pyperclip

3. API Key Setup

You do not need to manually create API_KEY.txt anymore!

The script will:

    Open HadithAPI in your browser

    Ask you to sign up and copy the API key

    Read it from your clipboard

    Validate and save it automatically ✅

    Prefer manual setup? Create a file called API_KEY.txt and paste your key in it.

4. Run the Script

python main.py

You’ll see a Hadith with headings displayed in your terminal.

Press Enter to see another, or type n to quit.
📌 Example Output

==================================================

Heading: Excellence of Performing Wudu Perfectly

Narrator: Abu Hurairah (RA)

Hadith: The Messenger of Allah (ﷺ) said: "When a Muslim or a believer washes his face..."

Book: Sahih Muslim
Chapter 2: Ablution
Status: Sahih

==================================================

💡 Future Ideas

    🔍 Add search/filter by Book, Narrator, or Topic

    🖼️ Convert to GUI using PyQt5

    💾 Save favorite Hadiths to a file

    🌙 Add support for Arabic Hadith display

📜 License

MIT License – free to use and modify with attribution.

Made with ❤️ by Umair
Visit HadithAPI.com


---