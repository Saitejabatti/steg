import cv2
import os

# Function to encode a message into the image
def encode_image(image_path, message, password):
    img = cv2.imread(image_path)
    if img is None:
        print(f"Error: Image not found at {image_path}! Please check the file path.")
        return
    
    height, width, _ = img.shape
    message_length = len(message)
    n = 0
    m = 0

    # Append the message length at the beginning of the message for decoding purposes
    encoded_message = f"{message_length}:" + message

    # Check if message is too large for the image
    if len(encoded_message) > (height * width * 3):
        print("Error: Message too large to fit in the image!")
        return

    # Embed the message into the image (LSB technique)
    for char in encoded_message:
        for bit in format(ord(char), '08b'):
            pixel = img[n, m]
            # Modify the LSB of each pixel to encode the message bit by bit
            pixel[0] = (pixel[0] & 0xFE) | int(bit)  # Modify the blue channel (0)
            n += 1
            if n == height:
                n = 0
                m += 1
            if m == width:
                break
        if m == width:
            break

    # Save the encoded image
    encrypted_image_path = "encrypted_image.png"
    cv2.imwrite(encrypted_image_path, img)
    print(f"Encoded image saved as {encrypted_image_path}")
    os.system(f"start {encrypted_image_path}")

# Function to decode a message from the image
def decode_image(image_path, password):
    img = cv2.imread(image_path)
    if img is None:
        print(f"Error: Image not found at {image_path}!")
        return

    # Get image dimensions
    height, width, _ = img.shape

    # Define variables for decoding
    message = ""  # Initialize message variable
    n = 0
    m = 0
    z = 0  # To iterate over the color channels
    extracted_bits = []

    # Loop through the image to extract the secret message
    pas = input("Enter passcode for Decryption: ")
    
    if password == pas:  # Check if the passcode matches
        # Extract bits from the LSB of each pixel
        for i in range(8 * (height * width)):  # Loop over all the bits in the image
            pixel = img[n, m]
            # Extract the LSB from the blue channel (0)
            extracted_bits.append(pixel[0] & 1)
            n += 1
            if n == height:
                n = 0
                m += 1
            if m == width:
                break

        # Reconstruct the message from the extracted bits
        message_bits = ''.join(map(str, extracted_bits))
        message_length = int(message_bits[:16], 2)  # First 16 bits are for the message length
        message_bits = message_bits[16:]  # Skip the first 16 bits for the length

        # Convert the remaining bits back into characters
        decoded_message = ''
        for i in range(0, message_length * 8, 8):
            byte = message_bits[i:i+8]
            decoded_message += chr(int(byte, 2))

        print("Decrypted message:", decoded_message)
    else:
        print("YOU ARE NOT AUTHORIZED TO DECRYPT")

# Main logic
img_path = input("Enter image file path: ")
msg = input("Enter secret message: ")
password = input("Enter a passcode for encryption: ")

# Encoding the message into the image
encode_image(img_path, msg, password)

# Decrypting the message (this part is only for demonstration, so you can adjust how to input passcode)
decryption_password = input("Enter passcode for Decryption: ")

# Check if the password is correct before decrypting
if password == decryption_password:  # Password should match the encryption passcode
    decode_image("encrypted_image.png", decryption_password)
else:
    print("Invalid passcode! Decryption failed.")

