# Project Plan: AI Image Generation Chat App

## 1. Goal

To develop a Python GUI application that allows users to generate images using the `stabilityai/sdxl-turbo` model through a chat-like interface. Users can provide text prompts and optionally an initial image to guide the generation process. Generated images will be saved locally.

## 2. Core Features

*   **Chat-like UI:** Interface resembling ChatGPT for user interaction.
*   **Text Prompting:** Users can input text descriptions to generate images.
*   **Image-to-Image Prompting:** Users can upload an image to be used as a base for generation, along with a text prompt.
*   **Image Generation:** Utilizes the `stabilityai/sdxl-turbo` model via the `diffusers` library.
*   **Local Storage:** Generated images are automatically saved to a `storage/` folder.
*   **SOLID Principles:** Code and project structure will adhere to SOLID principles.

## 3. Key Technologies & Libraries

*   **Python 3.x**
*   **GUI Framework:** A suitable Python GUI framework (e.g., Tkinter with `customtkinter` for a modern look, or PyQt/PySide for more advanced features).
*   **Hugging Face `diffusers`:** For interacting with the `sdxl-turbo` model.
*   **`Pillow` (PIL):** For image manipulation (loading, displaying, saving).
*   **`torch`:** As a dependency for `diffusers`.
*   **`transformers` & `accelerate`:** As dependencies for `diffusers`.

## 4. Project Structure

```
image-gen-chat-app/
├── main.py                     # Main application entry point
├── ui/
│   ├── __init__.py
│   ├── chat_window.py          # Main chat window UI components
│   └── widgets.py              # Custom UI widgets (e.g., image display)
├── services/
│   ├── __init__.py
│   ├── chat_service.py         # Handles chat logic, orchestrates UI and generation
│   ├── image_generator_service.py # Interface for sdxl-turbo model
│   └── storage_service.py      # Handles saving/loading images
├── models/                     # (Optional) Data models for messages, prompts
│   ├── __init__.py
│   └── message.py
├── storage/                    # Directory for storing generated images (created automatically)
├── assets/                     # (Optional) For icons, default images, etc.
├── requirements.txt            # Python package dependencies
├── plan.md                     # This plan file
└── README.md                   # Project overview and setup instructions
```

## 5. Development Phases & Tasks

### Phase 1: Setup and Core Model Integration

1.  **Project Initialization:**
    *   Create the directory structure outlined above.
    *   Set up a virtual environment.
    *   Create `requirements.txt` with initial dependencies: `diffusers`, `transformers`, `accelerate`, `torch`, `Pillow`, and the chosen GUI library.
    *   Install dependencies: `pip install -r requirements.txt`.
2.  **Image Generator Service (`services/image_generator_service.py`):**
    *   Implement a class `ImageGeneratorService`.
    *   Method to load the `stabilityai/sdxl-turbo` model using `AutoPipelineForText2Image` and `AutoPipelineForImage2Image`.
        *   Handle `torch_dtype=torch.float16`, `variant="fp16"`.
        *   Move pipe to "cuda" if available, with a fallback or warning for CPU.
    *   Method for text-to-image generation:
        *   Input: text prompt.
        *   Parameters: `num_inference_steps=1`, `guidance_scale=0.0`.
        *   Output: PIL Image object.
    *   Method for image-to-image generation:
        *   Input: text prompt, initial PIL Image object.
        *   Parameters: `num_inference_steps` (e.g., 2), `strength` (e.g., 0.5), `guidance_scale=0.0`. Ensure `num_inference_steps * strength >= 1`.
        *   Resize input image to 512x512 if necessary.
        *   Output: PIL Image object.
    *   Basic error handling (e.g., model loading failure).
3.  **Storage Service (`services/storage_service.py`):**
    *   Implement a class `StorageService`.
    *   Method to save a PIL Image object to the `storage/` directory.
        *   Ensure the `storage/` directory exists.
        *   Generate unique filenames (e.g., timestamp-based).

### Phase 2: Basic UI and Chat Logic

1.  **Basic Chat Window (`ui/chat_window.py`):**
    *   Create the main application window.
    *   Add a non-editable area to display chat history (prompts and images).
    *   Add a text input field for user prompts.
    *   Add a "Send" button.
    *   Add a button to "Upload Image" for image-to-image tasks.
2.  **Chat Service (`services/chat_service.py`):**
    *   Implement a class `ChatService` to manage the application state and flow.
    *   Initialize `ImageGeneratorService` and `StorageService`.
    *   Method to handle user sending a prompt:
        *   Get text from the input field.
        *   Get an optional uploaded image.
        *   If only text, call text-to-image generation.
        *   If text and image, call image-to-image generation.
        *   Display the user's prompt (text and/or uploaded image thumbnail) in the chat display.
        *   Display a "generating..." message.
        *   Once generated, display the image in the chat display.
        *   Save the generated image using `StorageService`.
        *   Handle and display errors from the generation process.
3.  **Main Application (`main.py`):**
    *   Initialize the UI and the `ChatService`.
    *   Connect UI actions (send button, image upload) to `ChatService` methods.
    *   Start the GUI event loop.

### Phase 3: UI/UX Refinements and Styling

1.  **UI Enhancements:**
    *   Improve the layout and appearance of the chat window to better resemble ChatGPT.
        *   User prompts aligned to one side, AI responses (images) to the other.
        *   Scrollable chat history.
    *   Implement proper display of uploaded image thumbnails in the prompt area.
    *   Implement display of generated images directly in the chat flow.
    *   Add loading indicators during image generation.
    *   Clear input field after sending.
2.  **Error Handling:**
    *   Provide user-friendly error messages for common issues (e.g., no CUDA device, model download issues, generation errors).
3.  **Image Interaction:**
    *   (Optional) Allow users to click on a generated image to view it larger or save it manually.

### Phase 4: SOLID Principles Review and Finalization

1.  **Code Review:**
    *   Review the codebase against SOLID principles. Refactor where necessary to improve adherence.
    *   Ensure classes have single responsibilities.
    *   Check for proper use of abstractions and dependency management.
2.  **Testing:**
    *   Test text-to-image generation with various prompts.
    *   Test image-to-image generation with various prompts and initial images.
    *   Test UI responsiveness and error handling.
3.  **Documentation:**
    *   Update `README.md` with comprehensive setup and usage instructions.
    *   Add comments to the code where necessary for clarity (non-obvious parts).

## 6. SOLID Principles Application Rules

*   **Single Responsibility Principle (SRP):**
    *   `ImageGeneratorService`: Solely responsible for interacting with the `stabilityai/sdxl-turbo` model and generating images.
    *   `StorageService`: Solely responsible for saving and potentially loading images from the filesystem.
    *   `ChatWindow` (and its components): Solely responsible for UI presentation and user input.
    *   `ChatService`: Orchestrates the interaction between UI, image generation, and storage, managing the application's flow but delegating specific tasks.
*   **Open/Closed Principle (OCP):**
    *   The `ImageGeneratorService` could be designed around an interface (e.g., `BaseImageGenerator`) if we anticipate supporting other models in the future, allowing new generators to be added without modifying `ChatService`.
    *   UI components could be designed to be extendable.
*   **Liskov Substitution Principle (LSP):**
    *   If using inheritance (e.g., for different message types in the chat display), ensure subtypes are substitutable for their base types without altering correctness.
*   **Interface Segregation Principle (ISP):**
    *   Define specific interfaces if components have diverse clients. For example, the `ChatService` might implement different interfaces for what the UI needs versus what a potential background processing task might need.
*   **Dependency Inversion Principle (DIP):**
    *   High-level modules like `ChatService` will depend on abstractions (e.g., an `ImageGeneratorInterface` that `ImageGeneratorService` implements) rather than concrete implementations.
    *   Dependencies (like `ImageGeneratorService` and `StorageService`) should be injected into `ChatService` (e.g., via constructor) to facilitate testing and flexibility.

## 6.1 Model Details and Exploration

This section outlines the models considered and their characteristics based on initial testing:

*   **`stabilityai/sd-turbo`**: (done and ok with animal and things, not with human) - *Initial model considered/used.*
*   **`stabilityai/sdxl-turbo`**: (better and larger) - *Current primary model for text-to-image.*
*   **`Heartsync/NSFW-Uncensored`**: (trying and okay with uncensored but only anime theme)
*   **`UnfilteredAI/NSFW-gen-v2.1`**: (still too large)

Image-to-image functionality is currently disabled in the application.

## 7. Considerations & Future Enhancements

*   **Performance:** Image generation can be resource-intensive. Consider offloading to a separate thread to keep the UI responsive.
*   **Model Parameters:** Allow users to adjust parameters like `strength` for image-to-image (within valid ranges).
*   **Prompt History:** Save and allow users to recall previous prompts.
*   **Packaging:** Use PyInstaller or similar tools to create a distributable executable.
*   **Advanced Error Logging:** Implement more robust logging.
*   **Batch Generation:** Allow generating multiple images from a single prompt.
*   **CPU Fallback:** More gracefully handle systems without CUDA, possibly by using a CPU-compatible version or warning the user about performance.

This plan provides a structured approach to developing your application. Remember to commit your code frequently and test each component as you build it. 