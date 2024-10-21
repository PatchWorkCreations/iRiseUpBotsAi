from PIL import Image
import os

# Define the folder containing your images
image_folder = '/Users/Julia/Downloads/braine-package/myapp/static/myapp/images/iriseup'

# Create an output folder for compressed images
compressed_folder = '/Users/Julia/Downloads/braine-package/myapp/static/myapp/images/compressed_images/iriseup'

# Ensure the compressed folder exists
if not os.path.exists(compressed_folder):
    os.makedirs(compressed_folder)

# Loop through all files in the image folder
for filename in os.listdir(image_folder):
    if filename.endswith(('.png', '.jpg', '.jpeg')):
        image_path = os.path.join(image_folder, filename)

        # Open an image file
        with Image.open(image_path) as img:
            # Compress and save the image
            compressed_image_path = os.path.join(compressed_folder, filename)
            
            # Save with reduced quality (quality=85 is a good balance)
            img.save(compressed_image_path, optimize=True, quality=85)

            print(f"Compressed {filename} and saved as {compressed_image_path}")

print("Image compression complete!")
