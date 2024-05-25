# process_images.py
import os
from face_manager import add_user_from_image, user_exists_by_name

def process_images_from_folder(folder_path):
    # Ensure the folder exists
    if not os.path.exists(folder_path):
        print(f"The folder {folder_path} does not exist.")
        return

    # Process each image in the folder
    for image_name in os.listdir(folder_path):
        image_path = os.path.join(folder_path, image_name)
        try:
            # Extract user information from the filename
            parts = image_name.split('_')
            if len(parts) >= 5:
                firstname = parts[0]
                lastname = parts[1]
                # Combine firstname and lastname as username
                username = f"{firstname}_{lastname}"
                # Check if the user already exists before adding
                if not user_exists_by_name(username):
                    add_user_from_image(username, image_path)
                    print(f"User {username} has been added successfully.")
                else:
                    print(f"User {username} already exists. Skipping.")
            else:
                print(f"Filename {image_name} does not match the expected format. Skipping.")
        except Exception as e:
            print(f"An error occurred while processing {image_name}: {e}")

if __name__ == "__main__":
    # Define the path to the folder containing the images
    images_folder_path = input("Enter the path to the folder containing the images: ")
    process_images_from_folder(images_folder_path)
