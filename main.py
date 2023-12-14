import requests
import re
from bs4 import BeautifulSoup
import json
import os
from tqdm import tqdm #importing for a progress bar to view in the CLI

# method for storing all scraped data into a JSON file for local use
def save_data_as_json(data):
    with open('crop_data.json', 'w') as file:
        json.dump(data, file)

def get_crop_data():
    url = "https://stardewvalleywiki.com/Crops"

    try:
        # Send a GET request to the URL
        response = requests.get(url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            print("Connection successful")
            soup = BeautifulSoup(response.content, "html.parser")

            # Find all tables on the page
            tables = soup.find_all("table", {"class": "wikitable roundedborder"})
            crops_info = []
            image_tag = tables[0].find("img")

            # Extract data from the first table (Crops table)
            for index, table in enumerate(tables):
                crop_name = table.find_all("a")[1].text
                harvest_time = table.find(string=re.compile("Total: "))
                sell_price_cell = table.find_all(string=re.compile('g\n\t'))
                image_tag = table.find("img")  # Find the image tag

                if image_tag:
                    image_url = "https://stardewvalleywiki.com" + image_tag.get("src")
                else:
                    image_tag = None

                if index < 12:
                    crop_season = 'Spring'
                elif index < 25 :
                    crop_season = 'Summer'
                elif index < 35:
                    crop_season = 'Fall'
                else:
                    crop_season = "Specialty Crop"
                
                crops_info.append(
                    {"Crop": crop_name, 
                     "Harvest Time": harvest_time, 
                     "Sell Price": sell_price_cell, 
                     "Grow Season": crop_season,
                     "Image URL": image_url})
                
            download_images(crops_info)

            # Print the harvested data for each crop (used for testing only.  Can be removed)
            for crop in crops_info:
                item_number = 0
                print("------------")
                print(f"Crop: {crop['Crop']}, Harvest Time: {crop['Harvest Time']}, Grow Season: {crop['Grow Season']}")
                print(f"--Sell Prices-- ")
                for i in crop['Sell Price']:
                    if item_number == 0:
                        print("Regular: ", i)
                    elif item_number == 1:
                        print("Silver: ", i)
                    elif item_number == 2:
                        print("Gold: ", i)
                    elif item_number == 3:
                        print("Iridium: ", i)
                    item_number += 1

        else:
            print("Failed to retrieve data from the website")
    except requests.RequestException as e:
        print(f"Request Exception: {e}")

    save_data_as_json(crops_info)

def download_images(crops_info):
    directory = "crop_images"
    downloaded_urls = set()  # Set to track downloaded image URLs

    if not os.path.exists(directory):
        os.makedirs(directory)

    # Initialize tqdm progress bar with total number of images to download
    with tqdm(total=len(crops_info), desc="Downloading images") as pbar:
        for crop in crops_info:
            image_url = crop["Image URL"]
            crop_name = crop["Crop"]

            if image_url and image_url not in downloaded_urls:
                file_path = f"{directory}/{crop_name}.png"
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
                        print(f"Error downloading image for {crop_name}: {e}")
                        continue

# Call the function to get crop data
get_crop_data()
