import os
import json

lib = os.path.join('library', 'library.json')

class Library:
    def __init__(self, library_path=lib):
        self.library_path = library_path
        self.data = self._load_library()

    def _load_library(self):
        """Loads the library JSON file"""
        try:
            with open(self.library_path, 'r', encoding='utf-8') as file:
                return json.load(file)
        except FileNotFoundError:
            print("Library file not found!")
            return []
        except json.JSONDecodeError:
            print("JSON format error in library file!")
            return []

    def fetch_info(self, plant_name):
        """Fetches plant info by name"""
        plant_name = plant_name.strip().lower()
        for plant in self.data:
            if plant.get("crop_name", "").lower() == plant_name:
                return plant
        return {"error": f"No data found for '{plant_name}'"}

    def list_all_plants(self):
        """Lists all available plants in library"""
        return [plant.get("crop_name", "") for plant in self.data if plant.get("crop_name")]