import requests
from bs4 import BeautifulSoup
from pathlib import Path

script_dir = Path(__file__).resolve().parent

urls = [
    'https://en.wikipedia.org/wiki/List_of_films:_numbers',
    'https://en.wikipedia.org/wiki/List_of_films:_A',
    'https://en.wikipedia.org/wiki/List_of_films:_B',
    'https://en.wikipedia.org/wiki/List_of_films:_C',
    'https://en.wikipedia.org/wiki/List_of_films:_D',
    'https://en.wikipedia.org/wiki/List_of_films:_E',
    'https://en.wikipedia.org/wiki/List_of_films:_F',
    'https://en.wikipedia.org/wiki/List_of_films:_G',
    'https://en.wikipedia.org/wiki/List_of_films:_H',
    'https://en.wikipedia.org/wiki/List_of_films:_I',
    'https://en.wikipedia.org/wiki/List_of_films:_J-K',
    'https://en.wikipedia.org/wiki/List_of_films:_L',
    'https://en.wikipedia.org/wiki/List_of_films:_M',
    'https://en.wikipedia.org/wiki/List_of_films:_N-O',
    'https://en.wikipedia.org/wiki/List_of_films:_P',
    'https://en.wikipedia.org/wiki/List_of_films:_Q-R',
    'https://en.wikipedia.org/wiki/List_of_films:_S',
    'https://en.wikipedia.org/wiki/List_of_films:_T',
    'https://en.wikipedia.org/wiki/List_of_films:_U-W',
    'https://en.wikipedia.org/wiki/List_of_films:_X-Z'
]

def get_html_content(url):
    try:
        response = requests.get(url, verify=False)  # Disable SSL verification for simplicity
        response.raise_for_status()  # Raise an exception for bad status codes
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching URL: {e}")
        return None

def extract_elements(html_content, selector):
    if html_content:
        soup = BeautifulSoup(html_content, 'html.parser')
        elements = soup.select(selector)
        return elements
    else:
        return []

if __name__ == '__main__':
    url = 'https://en.wikipedia.org/wiki/List_of_films:_A'  # Movies starting with 'A'
    selector = 'div.div-col a'  # links containing film titles
    print(f"Current working directory: {script_dir}")
    file_name = script_dir / 'assets/filelist.csv'
    print(f"File will be saved to: {file_name}")
    for url in urls:
        print(f"Processing URL: {url}")
        html_content = get_html_content(url)
        if html_content:
            elements = extract_elements(html_content, selector)
            if elements:
                lines = ["https://en.wikipedia.org" + element['href'] + "\n" for element in elements]  
                with open(file_name, 'a') as new_file:
                    new_file.writelines(lines)
            else:
                print("No elements found matching the selector.")
