import requests
from bs4 import BeautifulSoup
import json

# URL to scrape
url = "https://xaviers.ac/"

# Send GET request to fetch the content
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    soup = BeautifulSoup(response.content, 'html.parser')

    # Example: Scraping all text from paragraph tags (you can modify this based on the structure you need)
    paragraphs = soup.find_all('p')
    paragraph_texts = [para.get_text() for para in paragraphs]

    # You can also scrape other elements like titles, links, etc.
    # Example: Scraping all links (anchor tags)
    links = soup.find_all('a', href=True)
    link_urls = [link['href'] for link in links]

    # Creating a dictionary to store the scraped data
    data = {
        "paragraphs": paragraph_texts,
        "links": link_urls
    }

    # Save the data to a JSON file
    with open("xaviers_data.json", "w") as json_file:
        json.dump(data, json_file, indent=4)

    print("Scraped data saved to 'xaviers_data.json'")
else:
    print(f"Failed to retrieve the page. Status code: {response.status_code}")
