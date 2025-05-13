import customtkinter as ctk
from customtkinter import filedialog # Added for file dialog
import datetime # Add this import

class ChatWindow(ctk.CTk):
    def __init__(self, chat_service):
        super().__init__()
        self.title("AI Image Generator")
        self.geometry("800x600")

        self.chat_service = chat_service # This will be set by MainApplication
        self.current_uploaded_image_path = None # To store path from file dialog before sending with prompt

        # Main frame
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.pack(fill=ctk.BOTH, expand=True, padx=10, pady=10)

        # Chat display area (non-editable)
        self.chat_display = ctk.CTkTextbox(self.main_frame, state="disabled", wrap="word", font=("Arial", 12))
        self.chat_display.pack(fill=ctk.BOTH, expand=True, padx=5, pady=5)

        # Input frame
        self.input_frame = ctk.CTkFrame(self.main_frame)
        self.input_frame.pack(fill=ctk.X, padx=5, pady=5)

        # Upload image button (moved before prompt input for better layout with potential thumbnail)
        self.upload_button = ctk.CTkButton(self.input_frame, text="Upload Image", command=self._on_upload_image)
        self.upload_button.pack(side=ctk.LEFT, padx=(0,5))

        # Text input field
        self.prompt_input = ctk.CTkEntry(self.input_frame, placeholder_text="Enter your prompt here...")
        self.prompt_input.pack(side=ctk.LEFT, fill=ctk.X, expand=True, padx=(0, 5))
        self.prompt_input.bind("<Return>", self._on_send_prompt) # Bind Enter key

        # Send button
        self.send_button = ctk.CTkButton(self.input_frame, text="Send", command=self._on_send_prompt)
        self.send_button.pack(side=ctk.LEFT)

    def _on_send_prompt(self, event=None):
        """Handles sending a prompt (text and any pre-uploaded image)."""
        prompt_text = self.prompt_input.get().strip()
        
        if not prompt_text and not self.current_uploaded_image_path:
            self.add_message_to_display(sender="System", message="Please enter a prompt or upload an image.")
            return
        
        if not prompt_text and self.current_uploaded_image_path:
            # If only an image is uploaded, we still need a prompt for image-to-image.
            # For sd-turbo, an empty prompt might work, but it's good practice to have one.
            # Or, we can decide that a prompt is always necessary.
            # For now, let's assume a prompt is beneficial even if it's generic.
            # Alternatively, we could disable send if only image is present and no text.
            # Let's prompt the user for text for now if only an image is present.
            self.add_message_to_display(sender="System", message="Please also enter a text prompt to accompany the image.")
            return

        if self.chat_service:
            # Pass both text and the currently staged uploaded image path
            self.chat_service.handle_user_prompt(
                text_prompt=prompt_text,
                uploaded_image_path=self.current_uploaded_image_path
            )
            self.prompt_input.delete(0, ctk.END) # Clear input field
            self.current_uploaded_image_path = None # Clear staged image path after sending
            # We might want to remove the "Image selected: ..." message or thumbnail here
        else:
            print("ChatService not available.")

    def _on_upload_image(self):
        """Handles selecting an image file to be used with the next prompt."""
        filepath = filedialog.askopenfilename(
            title="Select an Image",
            filetypes=([
                ("Image Files", "*.png *.jpg *.jpeg *.bmp *.gif"),
                ("All Files", "*.*")
            ])
        )
        if filepath:
            self.current_uploaded_image_path = filepath
            # Display some feedback in the UI that an image has been selected
            # For now, we'll use the chat display. Later, a dedicated area or thumbnail could be used.
            filename = filepath.split('/')[-1]
            self.add_message_to_display(sender="System", message=f"Image selected: {filename}. Enter prompt and send.")
            # No direct call to chat_service.handle_user_prompt here.
            # The image path is stored and will be sent with the next text prompt.
            # If you want ChatService to know immediately, you can call a method like:
            # if self.chat_service:
            # self.chat_service.set_uploaded_image(filepath)
        else:
            self.current_uploaded_image_path = None # Ensure it's cleared if dialog is cancelled

    def add_message_to_display(self, sender: str, message: str = None, image_path: str = None):
        """Adds a message or an image path to the chat display."""
        self.chat_display.configure(state="normal")
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        if sender:
            self.chat_display.insert(ctk.END, f"[{timestamp}] {sender}:\n")
        if message:
            self.chat_display.insert(ctk.END, f"{message}\n\n")
        if image_path:
            filename = image_path.split('/')[-1]
            self.chat_display.insert(ctk.END, f"[Image: {filename}]\n\n")
        self.chat_display.configure(state="disabled")
        self.chat_display.yview(ctk.END) # Scroll to the bottom

# The __main__ part for independent testing needs to be updated to reflect ChatService dependency
if __name__ == '__main__':
    class DummyChatServiceForUI:
        def __init__(self, ui_view):
            self.ui_view = ui_view
            self.uploaded_image_path = None

        def handle_user_prompt(self, text_prompt=None, uploaded_image_path=None):
            print(f"DummyChatServiceForUI received: text='{text_prompt}', image='{uploaded_image_path}'")
            if text_prompt:
                 self.ui_view.add_message_to_display("You", message=text_prompt)
            if uploaded_image_path:
                self.ui_view.add_message_to_display("You", image_path=uploaded_image_path)
            
            self.ui_view.add_message_to_display("Bot", message="Generating... (UI test)")
            if text_prompt and not uploaded_image_path:
                self.ui_view.add_message_to_display("Bot", image_path=f"simulated_text2img_{text_prompt[:10]}.png")
            elif text_prompt and uploaded_image_path:
                img_name = uploaded_image_path.split('/')[-1]
                self.ui_view.add_message_to_display("Bot", image_path=f"simulated_img2img_{img_name}")
            self.uploaded_image_path = None

        # def set_uploaded_image(self, image_path: str):
        #     self.uploaded_image_path = image_path
        #     filename = image_path.split('/')[-1]
        #     self.ui_view.add_message_to_display("System", message=f"Dummy: Image {filename} set for next prompt.")

    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")
    
    # For testing ChatWindow independently, we pass its instance to the dummy service
    app = ChatWindow(chat_service=None) # ChatService is usually injected by MainApplication
    dummy_service = DummyChatServiceForUI(ui_view=app)
    app.chat_service = dummy_service # Manually set the service for the test
    
    app.mainloop() 