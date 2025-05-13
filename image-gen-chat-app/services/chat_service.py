import threading # Add threading import

# Placeholder for ChatService
class ChatService:
    def __init__(self, image_generator_service, storage_service, ui_view):
        self.image_generator_service = image_generator_service
        self.storage_service = storage_service
        self.ui_view = ui_view  # To interact with the ChatWindow instance
        # self.uploaded_image_path = None # No longer needed here, passed directly to handle_user_prompt

    def _process_generation(self, text_prompt: str = None, uploaded_image_path: str = None):
        """Handles the actual image generation and storage in a separate thread."""
        generated_image_path_or_msg = None
        try:
            if text_prompt and not uploaded_image_path: # Text-to-image
                generated_image_pil = self.image_generator_service.generate_text_to_image(prompt=text_prompt)
                if generated_image_pil:
                    generated_image_path_or_msg = self.storage_service.save_image(generated_image_pil, prompt_text=text_prompt)
                else:
                    generated_image_path_or_msg = "Text-to-image generation failed."

            elif text_prompt and uploaded_image_path: # Image-to-image
                initial_pil_image = self.storage_service.load_image(uploaded_image_path) # Assumes load_image exists
                if not initial_pil_image: # Try to open directly if not loaded by storage service (e.g. if storage_service.load_image is basic)
                    try:
                        from PIL import Image
                        initial_pil_image = Image.open(uploaded_image_path).convert("RGB")
                    except Exception as e:
                        generated_image_path_or_msg = f"Failed to load initial image: {uploaded_image_path}. Error: {e}"
                        # Schedule UI update for this error
                        if self.ui_view:
                            self.ui_view.after(0, lambda: self.ui_view.add_message_to_display(sender="Bot", message=generated_image_path_or_msg))
                        return


                if initial_pil_image:
                    generated_image_pil = self.image_generator_service.generate_image_to_image(
                        prompt=text_prompt,
                        init_image=initial_pil_image
                    )
                    if generated_image_pil:
                        original_filename = uploaded_image_path.split('/')[-1]
                        generated_image_path_or_msg = self.storage_service.save_image(
                            generated_image_pil, 
                            prompt_text=text_prompt, 
                            original_filename=original_filename
                        )
                    else:
                        generated_image_path_or_msg = "Image-to-image generation failed."
                # else: # This case is now handled by the initial_pil_image check above
                # generated_image_path_or_msg = f"Failed to load initial image: {uploaded_image_path}"
            
            elif not text_prompt and uploaded_image_path:
                 generated_image_path_or_msg = "Please provide a text prompt to accompany the uploaded image."
            
            else:
                 generated_image_path_or_msg = "Please provide a text prompt."

            # Schedule the final UI update from the main thread
            if self.ui_view and generated_image_path_or_msg:
                if "failed" in generated_image_path_or_msg.lower() or "please provide" in generated_image_path_or_msg.lower() or "error" in generated_image_path_or_msg.lower():
                    self.ui_view.after(0, lambda msg=generated_image_path_or_msg: self.ui_view.add_message_to_display(sender="Bot", message=msg))
                else:
                    self.ui_view.after(0, lambda path=generated_image_path_or_msg: self.ui_view.add_message_to_display(sender="Bot", image_path=path))

        except Exception as e:
            error_message = f"Error during generation process: {str(e)}"
            print(f"ChatService Error in _process_generation: {error_message}") # Log to console
            if self.ui_view:
                self.ui_view.after(0, lambda msg=error_message: self.ui_view.add_message_to_display(sender="Bot", message=msg))


    def handle_user_prompt(self, text_prompt: str = None, uploaded_image_path: str = None):
        # Display user's textual prompt in the UI
        if self.ui_view and text_prompt and text_prompt.strip() != "": # Ensure text_prompt is not empty or just spaces
            self.ui_view.add_message_to_display(sender="You", message=text_prompt)
        
        # If an image was uploaded, ChatWindow shows a thumbnail. 
        # If only image and no text, ChatWindow sends " " as prompt.
        # We can add a user message for the uploaded image if desired, but thumbnail might be enough.
        # Example: if self.ui_view and uploaded_image_path and (not text_prompt or text_prompt.strip() == ""):
        #     self.ui_view.add_message_to_display(sender="You", message=f"(Image: {uploaded_image_path.split('/')[-1]})")


        # Add a "generating..." message to UI immediately
        if self.ui_view:
            self.ui_view.add_message_to_display(sender="Bot", message="Generating, please wait...", is_loading=True)

        # Start the generation in a new thread
        generation_thread = threading.Thread(
            target=self._process_generation,
            args=(text_prompt, uploaded_image_path)
        )
        generation_thread.start()

    # def set_uploaded_image(self, image_path: str):
    #     """Stores the path of an image uploaded by the user."""
    #     self.uploaded_image_path = image_path
    #     if self.ui_view:
    #         # Display a confirmation or the image thumbnail in the prompt area
    #         # For now, just confirming with a message
    #         self.ui_view.add_message_to_display(sender="System", message=f"Image selected: {image_path.split('/')[-1]}")
    #         self.ui_view.add_message_to_display(sender="You", image_path=image_path) # Also show in chat 