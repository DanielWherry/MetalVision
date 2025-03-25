import requests
from bs4 import BeautifulSoup
import os
import urllib.request
import time

def scrape_band_data(base_url, band_page_urls, data_dir):
    """Scrapes band names and logo images from a website."""

    for url in band_page_urls:
        try:
            full_url = base_url + url #if the url is a relative path.
            response = requests.get(full_url)
            response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)

            soup = BeautifulSoup(response.content, 'html.parser')

            # Find the band name and logo image URL (adjust selectors as needed)
            band_name_element = soup.find('h1', class_='band-name') #example selector.
            logo_image_element = soup.find('img', class_='band-logo') #example selector.

            if band_name_element and logo_image_element:
                band_name = band_name_element.text.strip()
                logo_url = logo_image_element['src']

                # Create band directory
                band_dir = os.path.join(data_dir, band_name)
                os.makedirs(band_dir, exist_ok=True)

                # Download logo image
                image_path = os.path.join(band_dir, 'logo.jpg') # change the file extention if needed.
                urllib.request.urlretrieve(logo_url, image_path)

                print(f"Downloaded logo for {band_name}")
            else:
                print(f"Could not find band name or logo on {full_url}")

            time.sleep(1) # Be nice to the server.
        except requests.exceptions.RequestException as e:
            print(f"Error scraping {full_url}: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

# Example usage (replace with your actual URLs and directory)
base_url = 'https://www.example-metal-site.com/'
band_page_urls = ['band1.html', 'band2.html', 'band3.html'] # create a list of all of your urls.
data_dir = 'metal_logos'

scrape_band_data(base_url, band_page_urls, data_dir)