import os
import shutil
import json

# A script to clears the shared and saved images directories

def clear_folder(folder_path):
    if os.path.exists(folder_path):
        for item in os.listdir(folder_path):
            item_path = os.path.join(folder_path, item)
            if os.path.isfile(item_path):
                os.remove(item_path)
            elif os.path.isdir(item_path):
                shutil.rmtree(item_path)
    else:
        print(f"Folder {folder_path} does not exist.")

with open('config.json', 'r') as file:
    data = json.load(file)

uploads_folder = data.get('UPLOAD_FOLDER')
shares_folder = data.get('SHARES_FOLDER')

clear_folder(uploads_folder)
clear_folder(shares_folder)

print(f"Cleared folders: {uploads_folder} and {shares_folder}.")
