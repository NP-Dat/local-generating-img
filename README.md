# AI Image Generation Chat App

## 1. Overview

This Python GUI application allows users to generate images using AI models through a chat-like interface. Users can provide text prompts and optionally an initial image to guide the generation process. Generated images are saved locally.

## 2. Core Features

*   **Chat-like UI:** Interface resembling ChatGPT for user interaction.
*   **Text Prompting:** Users can input text descriptions to generate images.
*   **Image-to-Image Prompting:** Users can upload an image to be used as a base for generation, along with a text prompt.
*   **Image Generation:** Utilizes AI models like `stabilityai/sd-turbo` via the `diffusers` library.
*   **Local Storage:** Generated images are automatically saved to a `storage/` folder.
*   **SOLID Principles:** The project aims to adhere to SOLID principles in its code and structure.

## 3. Key Technologies & Libraries

*   **Python 3.x**
*   **GUI Framework:** (e.g., Tkinter with `customtkinter`, PyQt/PySide)
*   **Hugging Face `diffusers`**
*   **`Pillow` (PIL)**
*   **`torch`**
*   **`transformers` & `accelerate`**

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
│   ├── image_generator_service.py # Interface for sd-turbo model
│   └── storage_service.py      # Handles saving/loading images
├── models/                     # (Optional) Data models for messages, prompts
│   ├── __init__.py
│   └── message.py
├── storage/                    # Directory for storing generated images (created automatically)
├── assets/                     # (Optional) For icons, default images, etc.
├── requirements.txt            # Python package dependencies
├── documents/
│   ├── plan.md                 # Project plan
│   └── execution-instructions.md # Specific execution notes
└── README.md                   # This file
```

## 5. Setup and Installation

1.  **Clone the repository (if applicable).**

2.  **Create and activate a virtual environment:**
    *   It's highly recommended to use a virtual environment.
    *   PowerShell or Terminal with root is `image-gen-chat-app` folder:
        ```powershell
        python -m venv .venv
        .\.venv\Scripts\Activate.ps1
        ```
    *   Bash/Zsh:
        ```bash
        python3 -m venv .venv
        source .venv/bin/activate
        ```

3.  **Install dependencies from `requirements.txt`:**
    ```bash
    python -m pip install -r requirements.txt
    ```

4.  **PyTorch with CUDA (Important for GPU acceleration):**
    *   The standard `torch` installed via `requirements.txt` might not be compiled with CUDA support or for your specific CUDA version.
    *   **Ensure you have an NVIDIA GPU and the appropriate NVIDIA CUDA Toolkit installed on your system (Windows).**
    *   Uninstall the default torch, torchvision, and torchaudio:
        ```bash
        python -m pip uninstall torch torchvision torchaudio
        ```
    *   Install PyTorch, torchvision, and torchaudio compatible with your CUDA version (example for CUDA 11.8):
        ```bash
        python -m pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
        ```
        *Note: Adjust `cu118` to your installed CUDA version (e.g., `cu121` for CUDA 12.1). Visit the [PyTorch website](https://pytorch.org/get-started/locally/) for the correct command for your setup.*

## 6. Models Used

This application is designed to work with models from Hugging Face, primarily using the `diffusers` library.
*   **`stabilityai/sd-turbo`**: A FAST, LIGHT WEIGHT text-to-image model. Good for general purposes, animals, and objects. May have limitations with human figures.
*   **`Heartsync/NSFW-Uncensored`**: An alternative model, potentially for anime-style uncensored  (NSFW content). (It is so heavy. Make sure your device can run it, because it is really heavy).

The `image_generator_service.py` handles loading and interacting with these models.

## 7. Usage

1.  Ensure all setup steps are completed and your virtual environment is activated.
2.  Run the main application:
    ```bash
    python main.py
    ```
3.  The GUI will open, allowing you to type prompts or upload images for generation.
4.  Generated images will be saved in the `storage/` directory.

## 8. Development Notes

*   Refer to `documents/plan.md` for the detailed project plan and development phases.
*   `documents/execution-instructions.md` contains specific notes on environment setup and model testing.
*   The project aims to follow SOLID principles.

---
*This README was partially generated with AI assistance.*
