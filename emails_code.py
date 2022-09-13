from bs4 import BeautifulSoup
import time
import requests
import re

homepage = 'https://www.babywiggle.com/'

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.102 Safari/537.36 Avast/104.1.18182.102'
}

valid_emails = []

def get_links(headers, page):
    response = requests.get(url=page, headers=headers)
    html = response.text

    find_emails(html)

    if page == homepage:
        soup = BeautifulSoup(html, 'html.parser')

        all_links = soup.find_all('a', href=True)

        valid_links = []
        for link in all_links:
            link = link.get('href')
            if homepage in link:
                valid_links.append(link)
            else:
                if 'https://' not in link and 'http://' not in link:
                    valid_links.append(homepage + link)

        valid_links = list(dict.fromkeys(valid_links))

        return valid_links

def find_emails(html):
    raw_emails = re.findall(r'[\w.+-]+@[\w-]+\.[\w.-]+', html)

    email_suffix = ['.com', '.net', '.org', '.cc', '.co']

    if len(raw_emails) != 0:
        for email in raw_emails:
            for suffix in email_suffix:
                if suffix in email:
                    digit_count = 0
                    for i in email:
                        if i.isnumeric():
                            digit_count += 1
                    if digit_count < 10:
                        valid_emails.append(email)

    time.sleep(0.1)

def main():
    home_links = get_links(headers, homepage)
    print(len(home_links))

    for i, link in enumerate(home_links):
        print(f'{i}. {link}')
        get_links(headers, link)

    if len(valid_emails) != 0:
        emails = list(dict.fromkeys(valid_emails))

        for email in emails:
            print(email)

if __name__ == '__main__':
    main()