import logging
import base64
import os

logging.basicConfig(
    filename='image_secrets.log',  # Log file name
    level=logging.DEBUG,  # Log all levels of messages (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format='%(asctime)s - %(levelname)s - %(message)s'  # Log format with timestamp, level, and message
)

def Img_tools():
    while True:
        choice = input("""
---------- Image Secrets ------------ 
1. Inject Message
2. Read Message
------------------------------------- 
3. Inject An Image Into Another Image
4. Extract The image
-------------------------------------
5. Zip Inject Into Image
6. Extract Zip From Image 
-------------------------------------
7. Grab The Image Binary
8. Restore The Image Binary
-------------------------------------
9. Exit
-------------------------------------
Choose (1/2/3/4/5/6/7/8/9): """)

        if choice == "1": # message injection
            path =  input("Enter Image Path: ") #location
            texts_to_inject = input("Message To Inject: ") #texts to inject
            format = (".jpg", ".png", ".jpeg")
            if not path.endswith(format):
                print("Image Format Should be: jpg/png/jpeg")
                continue
            try:
                with open(path, "ab") as f:
                    f.write(texts_to_inject.encode())
                print("Message Injecting Successful!")
                logging.info(f"Message injected successfully into '{path}'")
            except Exception as e:
                logging.error(f"injecting message into image failed with error: {e}")
                print(f"Error: {e}")

        elif choice == "2": # Message reading
            image_reading_path = input("Enter Image Path For Reading: ")
            format = (".jpg", ".png", ".jpeg")
            if not image_reading_path.endswith(format):
                print("Image Format Should be: jpg/png/jpeg")
                continue
            try:
                with open(image_reading_path, "rb") as f:
                    content = f.read()
                    ofs = content.index(bytes.fromhex("FFD9"))
                    f.seek(ofs + 2)
                    print("--- The Message ---")
                    print(f.read())
                logging.info(f"Message successfully read from the image '{image_reading_path}'")
            except Exception as e:
                logging.error(f"Message reading from the Image failed with error: {e}")
                print(f"Error: {e}")

        elif choice == "3": # Image injection into an image
            image_inject_path = input("Enter the Base Image Path: ") # Base JPG image
            embed_image_path = input("Enter the Image path to embed: ") # PNG file to embed
            output_image_path = input("Output Image Path: ") # Output JPG with embedded PNG
            format = (".jpg", ".png", ".jpeg")
            if not image_inject_path.endswith(format) and not embed_image_path.endswith(format):
                print("Image Format Should be: jpg/png/jpeg")
                continue
            try:
                # Read the JPG image in binary mode
                with open(image_inject_path, "rb") as jpg_file:
                    jpg_data = jpg_file.read()

                # Read the PNG file in binary mode
                with open(embed_image_path, "rb") as png_file:
                    png_data = png_file.read()

                # Add a unique marker to separate the JPG data and PNG data
                marker = b"EMBEDDED_PNG_MARKER"

                # Combine the JPG data, marker, and PNG data
                combined_data = jpg_data + marker + png_data

                # Save the new image with the embedded PNG
                with open(output_image_path, "wb") as output_file:
                    output_file.write(combined_data)
                print(f"Image embedded successfully into {output_image_path}")
                logging.info(f"Image embedded successfully into '{output_image_path}' | The Base Image Path '{image_inject_path}' The Embed Image Path '{embed_image_path}'")
            except Exception as e:
                logging.error(f"Image embedding failed with error: {e}")
                print(f"Error: {e}")

        elif choice == "4": # image injection extraction
            embedded_image_path = input("Enter the Embedded Image Path: ")  # JPG with embedded PNG
            extracted_image_path = input("Output Image Path: ")  # Output PNG file
            format = (".jpg", ".png", ".jpeg")
            if not embedded_image_path.endswith(format):
                print("Image Format Should be: jpg/png/jpeg")
                continue
            try:
                # Read the combined file in binary mode
                with open(embedded_image_path, "rb") as img_file:
                    combined_data = img_file.read()

                # Define the unique marker
                marker = b"EMBEDDED_PNG_MARKER"

                # Check if the marker exists in the file
                if marker in combined_data:
                    # Split the data using the marker
                    jpg_data, png_data = combined_data.split(marker, 1)
                    
                    # Save the extracted PNG data
                    with open(extracted_image_path, "wb") as png_file:
                        png_file.write(png_data)
                    
                    print(f"PNG extracted successfully and saved to {extracted_image_path}")
                    logging.info(f"PNG extracted successfully and saved to {extracted_image_path}")
                else:
                    print("No embedded PNG found in the image!")
            except Exception as e:
                print(f"Error: {e}")
                logging.error(f"Message reading from the Image failed with error: {e}")

        elif choice == "5": #zip file injection to image
            image_path_for_zip = input("Enter the image file path: ") # Base image file
            zip_path = input("Enter the ZIP file path: ") # ZIP file to inject
            output_image_path = input("Enter the output image file path: ") # Image with injected ZIP
            format = (".jpg", ".png", ".jpeg")
            if not image_path_for_zip.endswith(format) and not output_image_path.endswith(format):
                print("Image Format Should be: jpg/png/jpeg")
                continue
            try:
                # Read the image file in binary mode
                with open(image_path_for_zip, "rb") as img_file:
                    image_data = img_file.read()

                # Read the ZIP file in binary mode
                with open(zip_path, "rb") as zip_file:
                    zip_data = zip_file.read()

                # Combine the image data with the ZIP data
                combined_data = image_data + b"ZIP_MARKER" + zip_data

                # Save the combined file
                with open(output_image_path, "wb") as output_file:
                    output_file.write(combined_data)
                print(f"ZIP file successfully injected into {output_image_path}")
                logging.info(f"ZIP {zip_path} file successfully injected into {output_image_path}")
            except Exception as e:
                print(f"Error: {e}")
                logging.error(f"Zip injecting into an image failed with error: {e}")

        elif choice == "6": #zip file extraction from image
            zip_injected_image_path = input("Enter the image file with injected ZIP path: ")  # Image with embedded ZIP
            output_zip_path = input("Enter the output ZIP file path: ")  # Output ZIP file
            format = (".jpg", ".png", ".jpeg")
            if not zip_injected_image_path.endswith(format):
                print("Image Format Should be: jpg/png/jpeg")
                continue
            try:
                # Read the combined file in binary mode
                with open(zip_injected_image_path, "rb") as injected_file:
                    combined_data = injected_file.read()

                # Define the unique marker
                marker = b"ZIP_MARKER"

                # Check if the marker exists in the file
                if marker in combined_data:
                    # Split the data using the marker
                    image_data, zip_data = combined_data.split(marker, 1)

                    # Save the extracted ZIP data
                    with open(output_zip_path, "wb") as zip_file:
                        zip_file.write(zip_data)

                    print(f"ZIP file successfully extracted to {output_zip_path}")
                    logging.info(f"Zip file sucessfully extracted to {output_zip_path}")
                else:
                    print("No ZIP file found in the image!")
            except Exception as e:
                print(f"Error: {e}")
                logging.error(f"Zip extracting from an image failed with error: {e}")

        elif choice == "7": #grabbing the image binary
            try:
                image_path = input("Enter Image File Path: ")
                text_file_name = input("Txt Filename For Saving the Image Binary (e.g., myimage.txt): ")
                if text_file_name.endswith(".txt"):
                    with open(image_path, "rb") as img_file:
                            binary_data = base64.b64encode(img_file.read()).decode('utf-8')
                    if not os.path.exists("Image_Binaries"):
                        os.mkdir("Image_Binaries")
                        print("A Folder Called 'Image_Binaries' is Created to Save the Txt Files There.")
                    text_file_path = os.path.join("Image_Binaries", f"{text_file_name}")
                    with open(text_file_path, "w") as txt_file:
                            txt_file.write(binary_data)
                            print(f"Txt Saved as {text_file_path}")
                            logging.info(f"Txt Saved as {text_file_path}")
                else:
                    print("The Image Binary File Format Is Not in '.txt'")
                    logging.error("The Image Binary File Format Is Not in '.txt'")

            except FileNotFoundError:
                    print("Error: The file path provided does not exist.")
                    logging.error("Error: The file path provided does not exist.")
            except Exception as e:
                    print(f"An error occurred: {e}")
                    logging.error(f"An error occurred: {e}")
        
        elif choice == "8": #restore the image binary 
            try:
                if os.path.exists(f"Image_Binaries"):
                            text_file_name = input("Enter the Image Binary Txt Filename: ")
                            text_file_path = os.path.join("Image_Binaries", f"{text_file_name}")
                            
                            if os.path.exists(text_file_path):
                                output_image_path = input("Output Image Path: ")
                                with open(text_file_path, "r") as txt_file:
                                    binary_data = txt_file.read()
                                with open(output_image_path, "wb") as img_file:
                                    img_file.write(base64.b64decode(binary_data))
                                    print(f"Image Created and Saved to {output_image_path}")
                                    logging.info(f"Image Created and Saved to {output_image_path}")
                            else:
                                print("Error: The specified file does not exist in 'Image_Binaries'.")
                                logging.info("Error: The specified file does not exist in 'Image_Binaries'.")
                else:
                    print("'Image_Binaries' folder does not exist. Provide another image binary txt location.")
                    other_txt_path = input("Enter the Image Binary Txt Path: ")
                    output_image_path = input("Output Image Path: ")
                    with open(other_txt_path, "r") as txt_file:
                        binary_data = txt_file.read()
                    with open(output_image_path, "wb") as img_file:
                        img_file.write(base64.b64decode(binary_data))
                        print(f"Image Created and Saved to {output_image_path}")
                        logging.info(f"'Image_Binaries' Folder Not Found, Used Custom Txt Location: Image Created and Saved to {output_image_path}")

            except FileNotFoundError:
                print("Error: The file path provided does not exist.")
                logging.error("Error: The file path provided does not exist.")
            except Exception as e:
                print(f"An error occurred: {e}")
                logging.error(f"An error occurred: {e}")

        elif choice == "9": #exiting
            break

        else:
            print("Invalid Choice!")

if __name__ == "__main__":
    Img_tools()
