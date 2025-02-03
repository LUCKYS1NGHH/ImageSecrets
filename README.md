# ImageSecrets
A Python script for embedding and extracting secret messages and files inside images. This script offers multiple features for hiding and revealing messages and files within image files, making it useful for steganography and data concealment.

# Features
1. Inject Message: Embed a secret message into an image file.
2. Read Message: Extract and read the secret message hidden within the image.
3. Inject An Image Into Another Image: Hide one image inside another, creating a steganographic file.
4. Extract The Image: Extract the hidden image from the combined image file.
5. Zip Inject Into Image: Inject a zip archive into an image for secure file storage.
6. Extract Zip From Image: Extract and retrieve the zip archive from the image.
7. Grab The Image Binary: Retrieve the raw binary data of an image.
8. Restore The Image Binary: Restore the binary data of an image from hidden data.

# Requirements
Python 3.x
Pillow (for image manipulation)
Zipfile (for handling zip files)

# 1. Usage
Clone the repository:
```bash
git clone https://github.com/LUCKYS1NGHH/ImageSecrets.git
cd imagesecrets
```
# 2. Install Dependencies
```bash
pip install -r requirements.txt
```
# 3. Run The Script
```bash
python image_secrets.py
```



