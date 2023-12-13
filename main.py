import requests
import re
from bs4 import BeautifulSoup

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

            # Extract data from the first table (Crops table)
            for table in tables:
                crop_name = table.find_all("a")[1].text
                harvest_time = table.find(string=re.compile("Total: "))
                sell_price_cell = table.find_all(string=re.compile('g\n\t'))

                crops_info.append({"Crop": crop_name, "Harvest Time": harvest_time, "Sell Price": sell_price_cell})

            # Print the harvested data for each crop
            for crop in crops_info:
                item_number = 0
                print("------------")
                print(f"Crop: {crop['Crop']}, Harvest Time: {crop['Harvest Time']}")
                print(f"--Sell Prices-- ")
                for i in crop['Sell Price']:
                    if item_number == 0:
                        print("Base level: ", i)
                    elif item_number == 1:
                        print("Silver Quality: ", i)
                    elif item_number == 2:
                        print("Gold Quality: ", i)
                    elif item_number == 3:
                        print("Iridium Quality: ", i)
                    item_number += 1

        else:
            print("Failed to retrieve data from the website")
    except requests.RequestException as e:
        print(f"Request Exception: {e}")

# Call the function to get crop data
get_crop_data()
