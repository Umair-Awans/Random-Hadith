import requests, random
from threading import Thread
from queue import Queue, Empty

API_URL = "https://hadithapi.com/public/api/hadiths"
NUM_PAGES = 5  # How many pages to fetch
NUM_SHOWN = 0


def get_api_key():
    try:
        with open("API_KEY.txt", 'r') as file:
            return file.read().strip()
    except FileNotFoundError:
        print("API_KEY.txt missing!")
        return None
        

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
    global NUM_SHOWN
    while True:
        try:
            Hadith = queue.get(timeout=10)
            if Hadith is None:
                break  # Done
            if is_complete(Hadith):
                display_Hadith(Hadith)
                NUM_SHOWN += 1
                if input("\nShow another Hadith? (Y/N): ").strip().lower().startswith('n'):
                    break
        except Empty:
            break
        

def main():
    API_KEY = get_api_key()
    if not API_KEY:
        return

    print("\nConnecting to Hadith server...\n")
    queue = Queue()
    
    producer_thread = Thread(target=producer, args=(queue, API_KEY))
    consumer_thread = Thread(target=consumer, args=(queue,))

    producer_thread.start()
    consumer_thread.start()

    producer_thread.join()
    consumer_thread.join()
    if NUM_SHOWN == 0:
        print("\nNo complete Hadith found. Try again...\n")

    print("\nHave a nice day!\n")


if __name__ == "__main__":
    main()