import customtkinter as ctk
# from customtkinter import filedialog # Added for file dialog
import datetime # Add this import
from PIL import Image, ImageTk # Import Pillow
import os # For joining paths

class ChatWindow(ctk.CTk):
    def __init__(self, chat_service):
        super().__init__()
        self.title("AI Image Generator")
        self.geometry("800x700") # Increased height a bit for thumbnail

        self.chat_service = chat_service # This will be set by MainApplication
        # self.current_uploaded_image_path = None # To store path from file dialog before sending with prompt
        # self.current_uploaded_image_thumbnail = None # To hold the CTkImage for the thumbnail

        # Main frame
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.pack(fill=ctk.BOTH, expand=True, padx=10, pady=10)

        # Chat display area
        # Use a CTkScrollableFrame to hold individual message bubbles/frames
        self.chat_scrollable_frame = ctk.CTkScrollableFrame(self.main_frame, fg_color="transparent")
        self.chat_scrollable_frame.pack(fill=ctk.BOTH, expand=True, padx=5, pady=5)
        self.chat_scrollable_frame.columnconfigure(0, weight=1) # Allow content to expand

        # Input frame
        self.input_outer_frame = ctk.CTkFrame(self.main_frame) # Outer frame for input elements
        self.input_outer_frame.pack(fill=ctk.X, padx=5, pady=(0,5)) # pady only at bottom

        # Frame for upload button and thumbnail
        self.upload_area_frame = ctk.CTkFrame(self.input_outer_frame, fg_color="transparent")
        self.upload_area_frame.pack(fill=ctk.X, pady=(5,0)) # pady only at top

        # Frame for prompt input and send button
        self.prompt_send_frame = ctk.CTkFrame(self.input_outer_frame, fg_color="transparent")
        self.prompt_send_frame.pack(fill=ctk.X, pady=5)
        
        self.prompt_input = ctk.CTkEntry(self.prompt_send_frame, placeholder_text="Enter your prompt here...", font=("Segoe UI", 13))
        self.prompt_input.pack(side=ctk.LEFT, fill=ctk.X, expand=True, padx=(0, 5))
        self.prompt_input.bind("<Return>", self._on_send_prompt)

        self.send_button = ctk.CTkButton(self.prompt_send_frame, text="Send", command=self._on_send_prompt, font=("Segoe UI", 12))
        self.send_button.pack(side=ctk.LEFT)

    def _on_send_prompt(self, event=None):
        """Handles sending a prompt (text and any pre-uploaded image)."""
        prompt_text = self.prompt_input.get().strip()
        
        # if not prompt_text and not self.current_uploaded_image_path:
        if not prompt_text:
            # self.add_message_to_display(sender="System", message="Please enter a prompt or upload an image.")
            self.add_message_to_display(sender="System", message="Please enter a prompt.")
            return
        
        if self.chat_service:
            self.chat_service.handle_user_prompt(
                text_prompt=prompt_text # if prompt_text else " ", # Send a space if no text but image exists
                # uploaded_image_path=self.current_uploaded_image_path
            )
            self.prompt_input.delete(0, ctk.END)
            # self._clear_uploaded_image_thumbnail() # Clear thumbnail and path
        else:
            print("ChatService not available.")

    # def _clear_uploaded_image_thumbnail(self):
    #     self.current_uploaded_image_path = None
    #     self.current_uploaded_image_thumbnail = None
    #     self.thumbnail_label.configure(image=None)
    #     self.thumbnail_label.image = None # Keep reference
    #     self.uploaded_image_filename_label.configure(text="")

    # def _on_upload_image(self):
    #     """Handles selecting an image file to be used with the next prompt."""
    #     filepath = filedialog.askopenfilename(
    #         title="Select an Image",
    #         filetypes=([
    #             ("Image Files", "*.png *.jpg *.jpeg *.bmp *.gif"),
    #             ("All Files", "*.*")
    #         ])
    #     )
    #     if filepath:
    #         self.current_uploaded_image_path = filepath
    #         filename = os.path.basename(filepath)
            
    #         try:
    #             img = Image.open(filepath)
    #             img.thumbnail((50, 50)) # Create a 50x50 thumbnail
    #             self.current_uploaded_image_thumbnail = ctk.CTkImage(light_image=img, dark_image=img, size=(img.width, img.height))
                
    #             self.thumbnail_label.configure(image=self.current_uploaded_image_thumbnail)
    #             self.thumbnail_label.image = self.current_uploaded_image_thumbnail # Keep reference
    #             self.uploaded_image_filename_label.configure(text=filename)
    #         except Exception as e:
    #             self.current_uploaded_image_path = None # Clear if error loading
    #             self.current_uploaded_image_thumbnail = None
    #             self.thumbnail_label.configure(image=None)
    #             self.thumbnail_label.image = None
    #             self.uploaded_image_filename_label.configure(text="Error loading thumbnail")
    #             self.add_message_to_display(sender="System", message=f"Error displaying thumbnail: {e}")
    #     else:
    #         self.current_uploaded_image_path = None # No need to explicitly clear if dialog is cancelled, already handled by _clear_uploaded_image_thumbnail on send

    def add_message_to_display(self, sender: str, message: str = None, image_path: str = None, is_loading: bool = False):
        """Adds a message or an image to the chat display using individual frames for better layout."""
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        
        # Determine alignment based on sender
        if sender.lower() == "you":
            anchor = "e" # Right align
            frame_bg = "#2b2b2b" # Darker gray for user, adjust as needed for theme
            text_color = "white"
        elif sender.lower() == "bot":
            anchor = "w" # Left align
            frame_bg = "#1e1e1e" # Slightly lighter for bot, adjust as needed
            text_color = "lightgray"
        else: # System, error, etc.
            anchor = "w" # Default to left for system messages
            frame_bg = "transparent" # Or a specific color for system messages
            text_color = "gray"
            if "error" in message.lower() if message else False:
                text_color = "red"
            if is_loading:
                text_color = "orange"

        # Create a frame for the entire message bubble
        # Pack this bubble_frame into self.chat_scrollable_frame
        # The bubble_frame itself will use grid to place timestamp/sender and content
        
        # We will create a message_frame that sticks to one side of the chat_scrollable_frame
        outer_message_frame = ctk.CTkFrame(self.chat_scrollable_frame, fg_color="transparent")
        # Add sticky based on anchor later

        # Content Frame (holds text or image)
        content_frame = ctk.CTkFrame(outer_message_frame, fg_color=frame_bg, corner_radius=10)

        # Sender and Timestamp
        header_text = f"{sender} [{timestamp}]"
        header_label = ctk.CTkLabel(content_frame, text=header_text, font=("Segoe UI", 11, "italic"), text_color=text_color)
        header_label.pack(padx=10, pady=(5,0), anchor="nw")

        if message:
            msg_label = ctk.CTkLabel(content_frame, text=message, wraplength=self.chat_scrollable_frame.winfo_width() - 100, justify=ctk.LEFT if anchor == 'w' else ctk.RIGHT, text_color=text_color, font=("Segoe UI", 14))
            msg_label.pack(padx=10, pady=(0,10), anchor="w")

        if image_path:
            try:
                pil_image = Image.open(image_path)
                # Resize for display, e.g., max width 300
                max_width = 300
                if pil_image.width > max_width:
                    scale = max_width / pil_image.width
                    new_height = int(pil_image.height * scale)
                    pil_image = pil_image.resize((max_width, new_height), Image.LANCZOS)

                ctk_image = ctk.CTkImage(light_image=pil_image, dark_image=pil_image, size=(pil_image.width, pil_image.height))
                img_label = ctk.CTkLabel(content_frame, image=ctk_image, text="")
                img_label.image = ctk_image # keep reference
                img_label.pack(padx=10, pady=10, anchor="w")
            except Exception as e:
                error_msg = f"Error displaying image {os.path.basename(image_path)}: {e}"
                err_label = ctk.CTkLabel(content_frame, text=error_msg, text_color="red", wraplength=self.chat_scrollable_frame.winfo_width() - 100, justify=ctk.LEFT)
                err_label.pack(padx=10, pady=10, anchor="w")
        
        # Pack the content_frame within outer_message_frame
        content_frame.pack(padx=5, pady=2, anchor=anchor) # Anchor inside its parent for alignment

        # Pack the outer_message_frame to the chat_scrollable_frame, making it stick to one side or the other
        if anchor == 'e': # User message
            outer_message_frame.pack(fill=ctk.X, padx=(50,5), pady=2) # Push to right
        else: # Bot or System message
            outer_message_frame.pack(fill=ctk.X, padx=(5,50), pady=2) # Push to left
            
        self.update_idletasks() # Important for scrollbar to know the new content size
        self.chat_scrollable_frame._parent_canvas.yview_moveto(1.0) # Scroll to bottom

# The __main__ part for independent testing needs to be updated to reflect ChatService dependency
if __name__ == '__main__':
    class DummyChatServiceForUI:
        def __init__(self, ui_view):
            self.ui_view = ui_view

        def handle_user_prompt(self, text_prompt=None, uploaded_image_path=None):
            print(f"DummyChatServiceForUI received: text='{text_prompt}', image='{uploaded_image_path}'")
            
            # Simulate user message
            if text_prompt and text_prompt.strip() != "":
                 self.ui_view.add_message_to_display("You", message=text_prompt)
            # if uploaded_image_path:
            #     # In a real scenario, the user's uploaded image might also be shown as a "You: [image]" message
            #     # For now, the thumbnail serves this purpose before sending.
            #     # Let's simulate the bot acknowledging the upload if no text_prompt
            #     if not text_prompt or text_prompt.strip() == "":
            #         self.ui_view.add_message_to_display("You", message=f"(Uploaded {os.path.basename(uploaded_image_path)})")

            # Simulate bot "generating" message
            self.ui_view.add_message_to_display("Bot", message="Generating, please wait...", is_loading=True)
            
            # Simulate bot response (text and/or image) after a delay
            def _dummy_response():
                if text_prompt and text_prompt.strip() != "": # and not uploaded_image_path: # Removed uploaded_image_path condition
                    self.ui_view.add_message_to_display("Bot", message=f"Okay, I will generate an image based on: '{text_prompt}'.")
                    # Simulate image generation - create a dummy image file for testing
                    dummy_image_path = "dummy_generated_image.png"
                    try:
                        img = Image.new('RGB', (200, 150), color = 'skyblue')
                        img.save(dummy_image_path)
                        self.ui_view.add_message_to_display("Bot", image_path=dummy_image_path)
                    except Exception as e:
                        self.ui_view.add_message_to_display("Bot", message=f"Error creating dummy image: {e}")

                # elif uploaded_image_path:
                #     original_filename = os.path.basename(uploaded_image_path)
                #     self.ui_view.add_message_to_display("Bot", message=f"Okay, processing '{original_filename}' with prompt: '{text_prompt}'.")
                #     # Simulate image-to-image - create another dummy image
                #     dummy_image_path_i2i = "dummy_i2i_generated_image.png"
                #     try:
                #         img = Image.new('RGB', (200, 150), color = 'lightgreen')
                #         img.save(dummy_image_path_i2i)
                #         self.ui_view.add_message_to_display("Bot", image_path=dummy_image_path_i2i)
                #     except Exception as e:
                #         self.ui_view.add_message_to_display("Bot", message=f"Error creating dummy i2i image: {e}")
                elif not text_prompt or text_prompt.strip() == "": # Only text prompt (no prompt was given)
                    self.ui_view.add_message_to_display("Bot", message="I received no text. How can I assist?")

            self.ui_view.after(2000, _dummy_response) # Simulate delay

    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")
    
    app = ChatWindow(chat_service=None)
    dummy_service = DummyChatServiceForUI(ui_view=app)
    app.chat_service = dummy_service
    
    # Add some initial messages for testing layout
    app.add_message_to_display("System", "Welcome to the AI Image Generator!")
    # app.add_message_to_display("You", "Hello, make me a cat astronaut.")
    # app.add_message_to_display("Bot", "Generating, please wait...", is_loading=True)

    app.mainloop() 