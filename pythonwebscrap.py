import re
import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urljoin  # Note: 'urlparse' is now part of 'urllib.parse' in Python 3

def get_links(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    links = [urljoin(url, link.get('href')) for link in soup.find_all('a', href=True)]
    return links

def find_phone_numbers_and_emails(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    content = soup.get_text()
    #phone_numbers = re.findall(r'\(?\b[2-9][0-9]{2}\)?[-. ]?[2-9][0-9]{2}[-. ]?[0-9]{4}\b', content)
    emails = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', content)
    return emails
    #return phone_numbers, emails

def scrape_website(url):
    #all_phone_numbers = {}
    all_emails = {}
    links = get_links(url)

    def process_link(link):
        try:
            # phone_numbers, emails = find_phone_numbers_and_emails(link)
            # for number in phone_numbers:
            #     all_phone_numbers[number] = link

            emails = find_phone_numbers_and_emails(link)
            for email in emails:
                all_emails[email] = link
        except Exception as e:
            print(f"Error processing link {link}: {e}")

    with ThreadPoolExecutor(max_workers=10) as executor:
        executor.map(process_link, links)

    return all_emails
    #return all_phone_numbers, all_emails

while True:
    url = input("Enter the URL of the website to scrape: ")  # Note: 'raw_input' is 'input' in Python 3
    emails = scrape_website(url)
    #phone_numbers, emails = scrape_website(url)

    # if phone_numbers:
    #     print("\nUS phone numbers found:")
    #     for number, source_url in phone_numbers.items():
    #         print('%s found on %s' % (number, source_url))
    # else:
    #     print("No US phone numbers found.")

    if emails:
        print("\nEmail addresses found:")
        for email, source_url in emails.items():
            print('%s found on %s' % (email, source_url))
    else:
        print("No email addresses found.")

    print("")
    print("--------------------------------")
    print("")

# if __name__ == "__main__":
#     url = input("Enter the URL of the website to scrape: ")  # Note: 'raw_input' is 'input' in Python 3
#     phone_numbers, emails = scrape_website(url)

#     if phone_numbers:
#         print("\nUS phone numbers found:")
#         for number, source_url in phone_numbers.items():
#             print('%s found on %s' % (number, source_url))
#     else:
#         print("No US phone numbers found.")

#     if emails:
#         print("\nEmail addresses found:")
#         for email, source_url in emails.items():
#             print('%s found on %s' % (email, source_url))
#     else:
#         print("No email addresses found.")
