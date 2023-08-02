import requests
from bs4 import BeautifulSoup
import os

def scrape_words_from_span_tags(url):
    # Send a request to the website and get the HTML content
    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code != 200:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")
        return []

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all span elements on the page
    spans = soup.find_all('a')

    # Extract the text within each span tag and split it into words
    words = []
    for span in spans:
        span_text = span.get_text().strip()
        if span_text:
            words.extend(span_text.split())

    return words


if __name__ == "__main__":
    words = ['eau', 'gay']
    month = -1
    day = -1
    year = -1
    startYear = 23
    endYear = 24

    for y in range(startYear, endYear):     # Loop for years
        year = str(y)
        for m in range(1, 13):  # Loop for months (1 to 12)
            if m < 10:
                month = '0' + str(m)
            else:
                month = str(m)
            for d in range(1, 32):  # Loop for days (1 to 31)
                if d < 10:
                    day = '0' + str(d)
                else:
                    day = str(d)
                url = f"https://www.xwordinfo.com/PS?date={month}/{day}/{year}"  # Replace this with the URL of the website you want to scrape
                print(url)
                words.append(scrape_words_from_span_tags(url))

        if words:
        # Save the words to a text file on the desktop
                    # Get the current working directory (current location of the Python script)
            current_dir = os.getcwd()
        # If you need to go up one level in the directory structure (optional)
            words_dir = os.path.dirname(current_dir) + "/WordProcessing"
            file_path = os.path.join(words_dir, f"scraped_words{year}.txt")

            with open(file_path, "w") as file:
                for word in words:
                    for w in word:
                        file.write(w + "\n")

            print(f"Scraped words have been saved to: {file_path}")
        else:
            print("No words found between <span> and </span> on the website.")
        words = []
