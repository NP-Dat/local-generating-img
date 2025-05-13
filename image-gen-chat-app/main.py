import customtkinter as ctk
# import datetime # No longer needed here if dummy services are removed
from ui.chat_window import ChatWindow
from services.chat_service import ChatService
from services.image_generator_service import ImageGeneratorService # To be implemented
from services.storage_service import StorageService # To be implemented

# Dummy services for now, to be replaced by actual implementations from Phase 1
# class DummyImageGeneratorService: # Remove this class
#     def generate_text_to_image(self, prompt: str):
#         print(f"[DummyImageGeneratorService] Text to Image: {prompt}")
#         # Simulate returning a path to a generated image
#         return f"path/to/generated_{prompt.replace(' ','_')}.png"
# 
#     def generate_image_to_image(self, prompt: str, initial_image): # initial_image would be a PIL Image
#         print(f"[DummyImageGeneratorService] Image to Image: {prompt} with image {initial_image}")
#         # Simulate returning a path to a generated image
#         return f"path/to/generated_from_image_{prompt.replace(' ','_')}.png"
# 
# class DummyStorageService: # Remove this class
#     def save_image(self, image): # image would be a PIL image
#         filename = f"storage/saved_image_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
#         print(f"[DummyStorageService] Saving image to {filename}")
#         # In a real scenario, you'd save the image data to a file
#         # For the dummy, we just return the simulated path
#         return filename
# 
#     def load_image(self, image_path: str):
#         print(f"[DummyStorageService] Loading image from {image_path}")
#         # Simulate loading an image (e.g., return a placeholder or mock PIL image object)
#         return "dummy_pil_image_object"


class MainApplication:
    def __init__(self):
        ctk.set_appearance_mode("dark")  # Modes: "System" (default), "Dark", "Light"
        ctk.set_default_color_theme("blue")  # Themes: "blue" (default), "green", "dark-blue"

        # Initialize services (using actual services now)
        self.image_generator_service = ImageGeneratorService()
        self.storage_service = StorageService() # Assuming storage_folder default is "storage" at project root
        
        # ChatWindow needs a reference to ChatService, but ChatService also needs a reference to ChatWindow (ui_view).
        # We'll pass a reference of ChatWindow to ChatService after ChatWindow is initialized.
        # However, the ChatService needs the ui_view in its constructor.
        # A solution:
        # 1. Create ChatWindow instance first.
        # 2. Create ChatService instance, passing the ChatWindow instance as ui_view.
        # 3. Set the chat_service attribute in ChatWindow.

        self.chat_window = ChatWindow(chat_service=None) # Pass None initially
        self.chat_service = ChatService(
            image_generator_service=self.image_generator_service,
            storage_service=self.storage_service,
            ui_view=self.chat_window # Pass the chat_window instance here
        )
        self.chat_window.chat_service = self.chat_service # Now set the chat_service in ChatWindow

        # Connect UI actions to ChatService methods
        # The ChatWindow already binds <Return> and button clicks to its own methods.
        # These methods should then call the ChatService.
        # Let's refine ChatWindow's _on_send_prompt and _on_upload_image.

    def run(self):
        self.chat_window.mainloop()

if __name__ == "__main__":
    app = MainApplication()
    app.run() 