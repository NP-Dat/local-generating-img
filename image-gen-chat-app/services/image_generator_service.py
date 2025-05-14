import torch
# from diffusers import AutoPipelineForText2Image, AutoPipelineForImage2Image
from diffusers import AutoPipelineForText2Image
from PIL import Image

class ImageGeneratorService:
    def __init__(self):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        if self.device == "cpu":
            print("Warning: CUDA not available, falling back to CPU. Image generation will be slower.")

        self.text_to_image_pipe = None
        # self.image_to_image_pipe = None

        try:
            print("Loading text-to-image model...")
            self.text_to_image_pipe = AutoPipelineForText2Image.from_pretrained(
                "stabilityai/sdxl-turbo",
                torch_dtype=torch.float16,
                variant="fp16"
            )
            self.text_to_image_pipe.to(self.device)
            print("Text-to-image model loaded successfully.")

            # print("Loading image-to-image model...")
            # self.image_to_image_pipe = AutoPipelineForImage2Image.from_pretrained(
            #     "stabilityai/sdxl-turbo",
            #     torch_dtype=torch.float16,
            #     variant="fp16"
            # )
            # self.image_to_image_pipe.to(self.device)
            # print("Image-to-image model loaded successfully.")

        except Exception as e:
            print(f"Error loading models: {e}")
            # Optionally, re-raise the exception or handle it as per application's needs
            # For now, we'll let the service initialize with None pipes if loading fails.
            # The methods using these pipes will need to check if they are None.

    def generate_text_to_image(self, prompt: str) -> Image.Image | None:
        if not self.text_to_image_pipe:
            print("Error: Text-to-image pipeline not initialized.")
            return None
        try:
            print(f"Generating text-to-image for prompt: '{prompt[:50]}...'")
            image = self.text_to_image_pipe(
                prompt=prompt,
                num_inference_steps=1,
                guidance_scale=0.0
            ).images[0]
            print("Text-to-image generation successful.")
            return image
        except Exception as e:
            print(f"Error during text-to-image generation: {e}")
            return None

    # def generate_image_to_image(self, prompt: str, init_image: Image.Image) -> Image.Image | None:
    #     if not self.image_to_image_pipe:
    #         print("Error: Image-to-image pipeline not initialized.")
    #         return None
    #     try:
    #         print(f"Generating image-to-image for prompt: '{prompt[:50]}...'")
    #         # Resize initial image to 512x512 as recommended for sd-turbo
    #         resized_init_image = init_image.resize((512, 512))

    #         # Ensure num_inference_steps * strength >= 1
    #         # Example values:
    #         num_inference_steps = 2
    #         strength = 0.5 # Must be between 0 and 1

    #         if not (0 <= strength <= 1):
    #              print(f"Warning: Strength ({strength}) is outside the valid range [0, 1]. Clamping to 0.5.")
    #              strength = 0.5 # Default or clamp

    #         actual_steps = int(num_inference_steps * strength)
    #         if actual_steps < 1:
    #             print(f"Warning: Calculated steps (num_inference_steps * strength = {actual_steps}) is less than 1. Adjusting num_inference_steps or strength.")
    #             # Adjust to meet the condition, e.g., by ensuring at least 1 step
    #             # For simplicity, if strength is low, we might need more num_inference_steps
    #             # Or, if num_inference_steps is fixed, strength must be high enough.
    #             # Here, we prioritize getting at least 1 step.
    #             if strength > 0: # Avoid division by zero
    #                 num_inference_steps = max(num_inference_steps, int(1.0 / strength) + (1 if (1.0 % strength) > 0 else 0) ) # Ensure at least 1 step
    #             else: # if strength is 0, it doesn't make sense for image-to-image, but to prevent errors:
    #                 num_inference_steps = 1 # Default to 1 step, though output might be poor
    #                 strength = 1.0 # Effectively making it 1 step if strength was 0.


    #         image = self.image_to_image_pipe(
    #             prompt=prompt,
    #             image=resized_init_image,
    #             num_inference_steps=num_inference_steps,
    #             strength=strength,
    #             guidance_scale=0.0
    #         ).images[0]
    #         print("Image-to-image generation successful.")
    #         return image
    #     except Exception as e:
    #         print(f"Error during image-to-image generation: {e}")
    #         return None

if __name__ == '__main__':
    # Example Usage (requires PyTorch, diffusers, Pillow, accelerate, transformers)
    # Ensure you have CUDA or a capable CPU.
    
    # This example part will not run directly without a proper environment
    # and downloading the model weights, which can take time and bandwidth.
    # It's here for illustrative purposes.

    print("Attempting to initialize ImageGeneratorService...")
    generator = ImageGeneratorService()

    if generator.text_to_image_pipe:
        print("Service initialized. Attempting generations...")
        
        # 1. Text-to-image example
        text_prompt = "A cinematic shot of a baby racoon wearing an intricate italian priest robe."
        generated_image_text = generator.generate_text_to_image(text_prompt)
        if generated_image_text:
            print(f"Text-to-image generated a {generated_image_text.size} image.")
            # generated_image_text.save("generated_text_to_image_example.png")
            # print("Saved text-to-image example as generated_text_to_image_example.png")
        else:
            print("Failed to generate text-to-image.")

        # # 2. Image-to-image example
        # # Create a dummy initial image for testing if you don't have one
        # try:
        #     # Attempt to load an image if one exists, or create a dummy one.
        #     # For a real test, replace "path_to_your_initial_image.png" with an actual image path.
        #     # init_img = Image.open("path_to_your_initial_image.png").convert("RGB")
        #     # Fallback to a dummy image for this example to run without external files:
        #     init_img = Image.new("RGB", (512, 512), color = "red")
        #     print("Created/loaded dummy initial image for image-to-image example.")

        #     image_prompt = "A cat wizard, gandalf, lord of the rings, detailed, fantasy, cute, adorable, Pixar, Disney, 8k"
        #     generated_image_img = generator.generate_image_to_image(image_prompt, init_img)
        #     if generated_image_img:
        #         print(f"Image-to-image generated a {generated_image_img.size} image.")
        #         # generated_image_img.save("generated_image_to_image_example.png")
        #         # print("Saved image-to-image example as generated_image_to_image_example.png")
        #     else:
        #         print("Failed to generate image-to-image.")
        # except FileNotFoundError:
        #     print("Initial image for image-to-image not found, and dummy image creation failed. Skipping image-to-image example.")
        # except Exception as e:
        #     print(f"An error occurred in the image-to-image example setup: {e}")

    else:
        print("ImageGeneratorService could not be initialized properly (text-to-image model might have failed to load). Check logs.")

    print("Example usage finished.") 