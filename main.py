import requests
import re
from bs4 import BeautifulSoup
import json

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
            crop_seasons = ['Spring', 'Summer', 'Fall']


            # Extract data from the first table (Crops table)
            for index, table in enumerate(tables):
                crop_name = table.find_all("a")[1].text
                harvest_time = table.find(string=re.compile("Total: "))
                sell_price_cell = table.find_all(string=re.compile('g\n\t'))
                if index < 12:
                    crop_season = crop_seasons[0]
                elif index < 25 :
                    crop_season = crop_seasons[1]
                elif index < 35:
                    crop_season = crop_seasons[2]
                else:
                    crop_season = "Specialty Crop"
                
                crops_info.append({"Crop": crop_name, "Harvest Time": harvest_time, "Sell Price": sell_price_cell, "Grow Season": crop_season})

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
# Call the function to get crop data
get_crop_data()
