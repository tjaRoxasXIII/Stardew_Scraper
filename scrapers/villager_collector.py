import requests
import re
from bs4 import BeautifulSoup
import json
import os
from tqdm import tqdm

def save_data_as_json(data):
    with open('villager_data.json', 'w') as file:
        json.dump(data, file)

def get_villagers_list():
    url = "https://stardewvalleywiki.com/Villagers"

    try:
        # Send a GET request to the URL
        response = requests.get(url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            print("Connection successful")
            soup = BeautifulSoup(response.content, "html.parser")

            tables = soup.find_all("li", {"class": "gallerybox"})
            villagers_info = []
            image_tag = tables[0].find("img")

            for table in tables:
                villager_name = table.find('p').find('a').text
                image_tag = table.find("img")

                if image_tag:
                    image_url = "https://stardewvalleywiki.com" + image_tag.get("src")
                else:
                    image_tag = None

                villagers_info.append(
                    {"Name": villager_name,
                    "Image URL": image_url}
                    )        

        download_images(villagers_info)

    except requests.RequestException as e:
        print(f"Request Exception: {e}")

    save_data_as_json(villagers_info)

def download_images(villagers_info):
    directory = "villager_images"
    downloaded_urls = set()  # Set to track downloaded image URLs

    if not os.path.exists(directory):
        os.makedirs(directory)

    # Initialize tqdm progress bar with total number of images to download
    with tqdm(total=len(villagers_info), desc="Downloading images") as pbar:
        for villager in villagers_info:
            image_url = villager["Image URL"]
            villager_name = villager["Name"]

            if image_url and image_url not in downloaded_urls:
                file_path = f"{directory}/{villager_name}.png"
                if not os.path.isfile(file_path):
                    try:
                        response = requests.get(image_url, stream=True)
                        if response.status_code == 200:
                            with open(file_path, "wb") as file:
                                for chunk in response.iter_content(chunk_size=1024):
                                    if chunk:
                                        file.write(chunk)
                            downloaded_urls.add(image_url)  # Add URL to set after download
                            pbar.update(1)  # Update progress for successful download
                    except requests.RequestException as e:
                        print(f"Error downloading image for {villager_name}: {e}")
                        continue


get_villagers_list()