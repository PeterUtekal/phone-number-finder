import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def get_links(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    links = [urljoin(url, link.get('href')) for link in soup.find_all('a', href=True)]
    return links

def find_phone_numbers(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    content = soup.get_text()
    phone_numbers = re.findall(r'\(?\b[2-9][0-9]{2}\)?[-. ]?[2-9][0-9]{2}[-. ]?[0-9]{4}\b', content)
    return phone_numbers

def scrape_website(url):
    all_phone_numbers = {}
    links = get_links(url)

    for index, link in enumerate(links):
        try:
            print(f'Processing link {index + 1}/{len(links)}: {link}')
            phone_numbers = find_phone_numbers(link)
            for number in phone_numbers:
                all_phone_numbers[number] = link
        except:
            print(f"Error processing link {index + 1}/{len(links)}: {link}")
            pass

    return all_phone_numbers

if __name__ == "__main__":
    url = input("Enter the URL of the website to scrape: ")
    phone_numbers = scrape_website(url)

    if phone_numbers:
        print("\nUS phone numbers found:")
        for number, source_url in phone_numbers.items():
            print(f'{number} found on {source_url}')
    else:
        print("No US phone numbers found.")

