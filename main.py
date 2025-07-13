import requests, random

def get_api_key():
    try:
        with open("API_KEY.txt", 'r') as file:
            key = file.read().strip()
            return key
    except FileNotFoundError:
        print("\nError! API KEY file could not be found\n.")
        return None


def get_data(API_KEY, page_no=None):
    BASE_URL = "https://hadithapi.com/public/api/hadiths"    

    params = {
        "apiKey": API_KEY
    }

    if page_no:
        params["page"] = page_no

    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()
        return response.json()
    except Exception as err:
        print(f"\nError: {err}\n")


def fetch_Hadith_Shareef(API_KEY):  
    data_one = get_data(API_KEY)
    if not data_one:
        return

    total_pages = data_one["hadiths"]["last_page"]
    page = random.randint(1, total_pages)

    data = get_data(API_KEY, page) or data_one

    list_Hadiths = data["hadiths"]["data"]
    num = random.randint(0, len(list_Hadiths) - 1)
    return list_Hadiths[num]


def display_Hadith_Shareef(Hadith_Shareef):
    print()
    if Hadith_Shareef.get("headingEnglish"):
        print(Hadith_Shareef["headingEnglish"])
    print()
    print(Hadith_Shareef["englishNarrator"])
    print()
    print(Hadith_Shareef["hadithEnglish"])
    print()

    book = Hadith_Shareef["bookSlug"]
    chapter = Hadith_Shareef["chapter"]["chapterEnglish"]
    chapter_no = Hadith_Shareef["chapter"]["chapterNumber"]
    statusHadith = Hadith_Shareef["status"]

    print(f"Book: {book}")
    print(f"Chapter no. {chapter_no}: {chapter}")
    print(f"Status: {statusHadith}")
    print()


def main():
    API_KEY = get_api_key()
    if not API_KEY:
        print("\nAPI key is missing. Please ensure 'API_KEY.txt' exists.\n")
        return
    print("\nConnecting to Hadith server... Please wait.\n")
    while True:        
        Hadith_Shareef = fetch_Hadith_Shareef(API_KEY)
        if not Hadith_Shareef:
            print("\nUnable to fetch Hadith. Trying again....\n")
            continue
        display_Hadith_Shareef(Hadith_Shareef)
        again = input("Show another? (Y/N): ").strip().lower()
        if again.startswith('n'):
            break

main()
