import os
from datetime import datetime
from PIL import Image
import re # For sanitizing filename

class StorageService:
    def __init__(self, storage_folder="storage"):
        self.storage_folder = storage_folder
        # Ensure the storage folder is relative to this file's directory or a known base path
        # For simplicity, assuming it's relative to where main.py is run and is just "storage"
        # If main.py is in project root, and this service is in services/,
        # then storage_folder should be "../storage" or an absolute path.
        # For now, assuming "storage" at the project root.
        # A better approach might be to pass the absolute path from main.py
        
        # Correcting path to be relative to the project root, assuming main.py is at the root
        # This script is in image-gen-chat-app/services/
        # storage/ is in image-gen-chat-app/
        # So, from this script's location, it should be "../storage"
        # However, the app is likely run from the root, where 'storage' is correct.
        # The init in __main__ of this script shows StorageService() which implies storage relative to CWD.
        # For now, let's stick to `storage_folder` being relative to CWD, which should be the project root.

        try:
            os.makedirs(self.storage_folder, exist_ok=True)
            print(f"Storage folder '{self.storage_folder}' ensured at CWD: {os.getcwd()}.")
        except OSError as e:
            print(f"Error creating storage directory '{self.storage_folder}': {e}")

    def _sanitize_filename(self, text: str, max_length: int = 50) -> str:
        if not text:
            return ""
        # Remove special characters, replace spaces with underscores
        s_text = re.sub(r'[^a-zA-Z0-9_\\-\\.]', '', text.replace(' ', '_'))
        return s_text[:max_length]

    def save_image(self, image: Image.Image, prompt_text: str = None, original_filename: str = None) -> str | None:
        if not isinstance(image, Image.Image):
            print("Error: Invalid image object provided for saving.")
            return None

        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            base_filename = "generated_image"
            
            if original_filename:
                # Sanitize and use part of the original filename if generating from an existing image
                s_orig_name = self._sanitize_filename(original_filename.split('.')[0]) # Remove extension
                base_filename = f"from_{s_orig_name}"
            
            if prompt_text:
                s_prompt = self._sanitize_filename(prompt_text)
                if original_filename: # img2img
                    filename = f"{base_filename}_with_{s_prompt}_{timestamp}.png"
                else: # text2img
                    filename = f"{s_prompt}_{timestamp}.png"
            else:
                filename = f"{base_filename}_{timestamp}.png"
                
            filepath = os.path.join(self.storage_folder, filename)
            
            image.save(filepath, "PNG")
            print(f"Image saved successfully to {filepath}")
            return filepath
        except Exception as e:
            print(f"Error saving image to {self.storage_folder} (path: {filepath if 'filepath' in locals() else 'unknown'}): {e}")
            return None

    def load_image(self, image_path: str) -> Image.Image | None:
        """Loads an image from the given filepath and returns a PIL Image object."""
        try:
            if not os.path.exists(image_path):
                print(f"Error: Image file not found at {image_path}")
                return None
            
            image = Image.open(image_path).convert("RGB") # Convert to RGB for consistency
            print(f"Image loaded successfully from {image_path}")
            return image
        except Exception as e:
            print(f"Error loading image from {image_path}: {e}")
            return None

if __name__ == '__main__':
    # Example Usage (requires Pillow)
    print("Attempting to initialize StorageService...")
    # Note: This example will create a folder named "image-gen-chat-app/storage"
    # relative to where this script is run if it doesn't exist.
    storage_service = StorageService() # Uses default storage_folder
    # Or specify a different one: storage_service = StorageService(storage_folder="my_custom_storage")

    if os.path.exists(storage_service.storage_folder):
        print("StorageService initialized. Attempting to save a dummy image...")
        # Create a dummy image for testing
        try:
            dummy_image = Image.new('RGB', (100, 100), color = 'blue')
            saved_path = storage_service.save_image(dummy_image)

            if saved_path:
                print(f"Dummy image was saved to: {saved_path}")
                # You can check your file system for this image.
                # os.remove(saved_path) # Clean up the dummy image if you want
                # print(f"Cleaned up dummy image: {saved_path}")
            else:
                print("Failed to save the dummy image.")
        except Exception as e:
            print(f"An error occurred during the dummy image saving test: {e}")
    else:
        print(f"StorageService could not ensure creation of storage folder: {storage_service.storage_folder}")

    print("Example usage finished.") 