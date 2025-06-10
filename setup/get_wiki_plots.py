import requests
import csv
from bs4 import BeautifulSoup
from pathlib import Path
from urllib3 import disable_warnings
from urllib3.exceptions import InsecureRequestWarning

disable_warnings(InsecureRequestWarning)

script_dir = Path(__file__).resolve().parent

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
    
def extract_plot_from_url(url) -> tuple:
    html_content = get_html_content(url)
    if html_content:
        plot_elements = extract_elements(html_content, '#Plot')
        synopsis_elements = extract_elements(html_content, '#Synopsis')
        title = extract_elements(html_content, '#firstHeading')
        elements = plot_elements or synopsis_elements
        if elements and title:
            title_text = title[0].get_text().strip()
            element = elements[0]
            siblings = element.parent.find_next_siblings()
            plots = []
            for sibling in siblings:
                if sibling.name == 'p':
                    plots.append(sibling.get_text().strip())
                elif sibling.name == 'div' and sibling.get('class') and 'mw-heading' in sibling['class']:
                    # break on encountering a non-paragraph element
                    break
            plot_text = " ".join(plots)
            return (title_text, plot_text)
        else:
            print("No elements found matching the selector.")
    return (None, None)

if __name__ == '__main__':
    selector = '#Plot'  # links containing film titles
    print(f"Current working directory: {script_dir}")
    all_movies_file = script_dir / 'assets/filelist.csv'
    plot_file = script_dir / 'assets/plots.csv'
    print(f"File will be saved to: {all_movies_file}")
    url = 'https://en.wikipedia.org/wiki/2_Fast_2_Furious'  # Example URL for a specific movie
    print(f"Processing URL: {url}")
    (title_text, plot_text) = extract_plot_from_url(url)
    print(f"Title: {title_text}")
    print(f"Plot: {plot_text}")
    with open(all_movies_file, 'r', newline='') as movies_file:
        with open(plot_file, 'w', newline='') as csvfile:
            reader = csv.reader(movies_file)
            writer = csv.writer(csvfile, delimiter='|')
            for index, url in enumerate(reader):
                (title_text, plot_text) = extract_plot_from_url(url[0])
                if title_text and plot_text:
                    writer.writerow([title_text, url[0], plot_text])
                    print(f"Plots saved for: {title_text}, index: {index}")
                else:
                    print(f"Failed to extract plot for: {url[0]}")

    