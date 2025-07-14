import requests, random, webbrowser, pyperclip, time
from threading import Thread
from queue import Queue, Empty

FILE_NAME = "API_KEY.txt"
API_URL = "https://hadithapi.com/public/api/hadiths"
NUM_PAGES = 5  # How many pages to fetch
Hadiths_Shown = 0


def save_api_key(API_KEY: str):
    try:
        with open(FILE_NAME, 'w') as file:
            file.write(API_KEY)
    except Exception as e:
        print(f"An Error Occurred: {e}")


def is_valid_api(API_KEY):
    try:
        response = requests.get(API_URL, params={"apiKey": API_KEY})        
        if response.status_code == 401:
            return False
    except ConnectionError:
        print("\nUnable to connect. Please check your internet connection.\n")
    except Exception as err:
        print(f"\nError: {err}\n")
    return True

        
def handle_missing_api_key():
    print("\nAn API key is required to fetch Hadiths from HadithAPI.\n")
    if not input("\nDo you want to sign-up on https://hadithapi.com and get an API key for free now? (Y/N): ").strip().lower().startswith("y"):
        print("\n\n\nFollow the instructions in README.md to fix the issue manually.\n\n")
        return None
    print("\nOpening the HadithAPI sign-up page in your browser...")
    print(
        "\nHow to set up your API key automatically:\n"
        "\n1. Sign up for free on the website."
        "\n2. Copy the API key (Ctrl + C)."
        "\n3. Leave the rest to us — we'll grab it from your clipboard!\n"
        "\nDon't close this window while doing this."
    )
    time.sleep(2)
    webbrowser.open("https://hadithapi.com")
    time.sleep(60)
    while True:
        time.sleep(3)
        if not input("\nHave you copied the API-key to clipboard? (Y/N): \n").lower().strip().startswith("y"):
            print("\nNo worries — just copy your API key to the clipboard when you're ready.")
            continue
        API_KEY = pyperclip.paste().strip()
        if is_valid_api(API_KEY):
            save_api_key(API_KEY)
            print("\n\n\nAPI-key validated successfully!\n\nFetching Hadith Shareef....")
            return API_KEY
        else:
            print(f"\n❌ The API key you copied ({API_KEY}) is invalid. Please copy the correct one.")


def get_api_key():
    try:
        with open(FILE_NAME, 'r') as file:
            return file.read().strip()
    except FileNotFoundError:
        print("API_KEY.txt missing!")
        return handle_missing_api_key()


# 🧵 PRODUCER: Fetch pages and put into queue
def producer(queue, API_KEY):
    for i in range(NUM_PAGES):
        page = random.randint(1, 100)
        # print(f"\nFetching page {page}...\n")
        try:
            response = requests.get(API_URL, params={"apiKey": API_KEY, "page": page})
            response.raise_for_status()
            data = response.json()
            for Hadith in data["hadiths"]["data"]:
                queue.put(Hadith)
        except ConnectionError:
            print("\nUnable to connect. Please check your internet connection.\n")
        except Exception as e:
            print(f"Error fetching page {page}: {e}")
    queue.put(None)  # Sentinel to tell consumer: Done


# 📦 Helper to extract useful info
def get_details(Hadith: dict):
    return (
        Hadith.get("bookSlug", ""),
        Hadith.get("chapter", {}).get("chapterEnglish", ""),
        Hadith.get("chapter", {}).get("chapterNumber", ""),
        Hadith.get("status", "")
    )


def is_complete(Hadith):
    if not all([Hadith.get("headingEnglish"), Hadith.get("englishNarrator"), Hadith.get("hadithEnglish")]):
        return False
    if not all(get_details(Hadith)):
        return False
    return True


def display_Hadith(Hadith: dict):
    heading, Narrator, english_Hadith = Hadith["headingEnglish"], Hadith["englishNarrator"], Hadith["hadithEnglish"]
    book, chapter, chap_no, status = get_details(Hadith)
    book = book.replace("-", " ").title()
    content = (
        "\n" + "=" * 50 + "\n"
        f"\nHeading: {heading}\n"
        f"\nNarrator: {Narrator}\n"
        f"\nHadith: {english_Hadith}\n"
        f"\nBook: {book}"
        f"\nChapter {chap_no}: {chapter}"
        f"\nStatus: {status}" +
        "\n\n" + "=" * 50 + "\n\n"
    )
    print(content)


# 🧵 CONSUMER: Filter and display Hadiths from queue
def consumer(queue: Queue):
    global Hadiths_Shown
    while True:
        try:
            Hadith = queue.get(timeout=10)
            if Hadith is None:
                break  # Done
            if is_complete(Hadith):
                display_Hadith(Hadith)
                Hadiths_Shown += 1
                if input("\nShow another Hadith? (Y/N): ").strip().lower().startswith('n'):
                    break
        except Empty:
            break


def banner():
    """Displays a welcome banner for the user."""
    print("=" * 50)
    print("\nWelcome to Hadith Fetcher")
    print("Powered by HadithAPI.com\n")
    print("=" * 50 + "\n")


def main():
    banner()
    API_KEY = get_api_key()
    if not API_KEY:
        print("\nHave a nice day!\n")
        return

    print("\nConnecting to Hadith server...\n")
    queue = Queue()
    
    producer_thread = Thread(target=producer, args=(queue, API_KEY))
    consumer_thread = Thread(target=consumer, args=(queue,))

    producer_thread.start()
    consumer_thread.start()

    producer_thread.join()
    consumer_thread.join()
    if Hadiths_Shown == 0:
        print("\nNo complete Hadith found. Try again...\n")

    print("\nHave a nice day!\n")


if __name__ == "__main__":
    main()