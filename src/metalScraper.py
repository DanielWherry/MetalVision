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
            headers = {"accept":"*/*","accept-encoding":"gzip, deflate, br, zstd","accept-language":"en-US,en;q=0.9","cookie":"PHPSESSID=0017e50d7ef5e13712dda5f8e3991ea2; masessid=7UXCK17167117; __utma=235797405.2012761494.1742864914.1742864914.1742864914.1; __utmc=235797405; __utmz=235797405.1742864914.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utmt=1; cf_clearance=DE9sEFaiV.xuNtkeor6lAX6vdTBJstUfXhBCWhgzMSs-1742866328-1.2.1.1-pWOMCajw8N3xTLr6JdMhiCSB32sUZ4WDqcLG63J2C.BbyNx0V7v1.Dzah4jlejNlHC5djUqTwInYEAz9GySKp1T7AlGW0IRSkNDtWOfYdAy_3Nh7pKB2cOU_IsG0cG9_ZFlRYHwUhpawLz2NhSLYUviWzV6NFMx6o2Qz4WMDi5DzEQhHGwOXPM76HqqI.8rDz3mw8_SSqpKE6mPl.U5dizeqo3Hpw1kpmHPSCQliCzOcRvKHBQ7yQ93Bw7BBTtraPtq.cuSJVWfM459JdjA.GDjWBKMr7uln7NtksXfz3vDmceWsClMO4GuW.BV6u3dk5yStBohI7cNyIahGTJlTNC3EzAqE0IfUu5VW4GX4CxcEL8RHlBwbCCpUA94cM7WwIZDqke1T.Sr4QPK5iVjMLvjIVdIUOCcisf5nAhPRleo; __utmb=235797405.31.10.1742864914","priority":"u=1, i","referer":"https://www.metal-archives.com/bands/A_Balance_of_Power/3540352307","sec-ch-ua":"\"Chromium\";v=\"134\", \"Not:A-Brand\";v=\"24\", \"Google Chrome\";v=\"134\"","sec-ch-ua-arch":"\"x86\"","sec-ch-ua-bitness":"\"64\"","sec-ch-ua-full-version":"\"134.0.6998.118\"","sec-ch-ua-full-version-list":"\"Chromium\";v=\"134.0.6998.118\", \"Not:A-Brand\";v=\"24.0.0.0\", \"Google Chrome\";v=\"134.0.6998.118\"","sec-ch-ua-mobile":"?0","sec-ch-ua-model":"\"\"","sec-ch-ua-platform":"\"Windows\"","sec-ch-ua-platform-version":"\"10.0.0\"","sec-fetch-dest":"empty","sec-fetch-mode":"cors","sec-fetch-site":"same-origin","user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36","x-requested-with":"XMLHttpRequest"}

            response = requests.get(full_url, headers=headers)
            response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)

            print(response.status_code)
            html_content = response.content.decode("utf-8")

            soup = BeautifulSoup(html_content, 'html.parser')

            # Find the band name and logo image URL (adjust selectors as needed)
            band_name_element = soup.find('h1', class_='band_name')
            logo_image_element = soup.find('a', {"id":"logo"}) 

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

            time.sleep(5) # Be nice to the server.
        except requests.exceptions.RequestException as e:
            print(f"Error scraping {full_url}: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

# Example usage (replace with your actual URLs and directory)
# base_url = 'https://www.metal-archives.com'
# #https://www.metal-archives.com/lists/A
# band_page_urls = ['band1.html', 'band2.html', 'band3.html'] # create a list of all of your urls.
data_dir = 'C:\\bin\\MetalVision\\MetalVision\\data'


base_url = 'https://www.metal-archives.com'
#https://www.metal-archives.com/lists/A
band_page_urls = ['/bands/A_Balance_of_Power']
scrape_band_data(base_url, band_page_urls, data_dir)