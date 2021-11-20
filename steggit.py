import os, sys
from PIL import Image


# Short term plans:
#   Encode messages in randomly chosen (or created) images
#   Decode messages from images

# Discord integration:
#   Listen for encode command
#   Generate or get random image and encode message
#   Replace the original command with encoded image


# each letter (8-bit binary) = requires 3 pixels (9-bits)
def copy_to_new_image(original_image):
    encoded_image = original_image.copy()
    og_photo_filename = os.path.splitext(original_image.filename)[0]
    og_photo_extension = os.path.splitext(original_image.filename)[1]
    new_image_name = og_photo_filename + "_enc" + og_photo_extension
    encoded_image.save(new_image_name)
    return Image.open(new_image_name)


def string_to_ascii(message):
    ascii_message = []
    for character in message:
        ascii_message.append(ord(character))
    return ascii_message


def ascii_to_binary(ascii_message):
    binary_message = []
    for character in ascii_message:
        binary_message.append(int(bin(character)[2:]))
    return binary_message


def calculate_pixels_needed(binary_message):
    binary_characters = len(binary_message)
    pixels_needed = binary_characters * 3
    return pixels_needed


def pixel_check(pixel_requirement, image):
    pixels = len(image.getdata())
    if pixels < pixel_requirement:
        return False
    return True


def adjust_pixel(pixel_value):
    if pixel_value == 0:
        new_pixel_value = pixel_value + 1
    else:
        new_pixel_value = pixel_value - 1
    return new_pixel_value


def encode_message(binary_message, new_image):
    pixel_data = iter(new_image.getdata())
    message_length = len(binary_message)
    for binary_letter in binary_message:
        # 1101000
        pixel_set = [
            value
            for value in pixel_data.__next__()[:3]
            + pixel_data.__next__()[:3]
            + pixel_data.__next__()[:3]
        ]
        for index, binary_character in enumerate(str(binary_letter)):
            binary_value = int(binary_character)
            pixel_value = pixel_set[index]
            if (binary_value == 1) and (pixel_value % 2 == 0):
                # Handle switching the pixel value
                new_pixel_value = adjust_pixel(pixel_value)
                pixel_set[index] = new_pixel_value
            if (binary_value == 0) and (pixel_value % 2 == 1):
                # Handle switching the pixel value
                new_pixel_value = adjust_pixel(pixel_value)
                pixel_set[index] = new_pixel_value

        import pdb

        pdb.set_trace()
        # Change the first item in pixel tuple to even or odd
        # Change the second item in pixel tuple to even or odd
        # Change the third item in pixel tuple to even or odd
        # Move to next pixel
        # Repeat
        # Move to third pixel
        # Repeat for first item in pixel tuple
        # ---- moving to the next binary letter
        # Change the second item in pixel tuple to even or odd
        # etc.

    return encoded_image


# Main Function
def main():
    message = input("Input a string: ")
    original_image = Image.open("random_fish.jpg")
    new_image = copy_to_new_image(original_image)
    # small_image = Image.new("RGB", (5, 5))
    ascii_message = string_to_ascii(message)
    binary_message = ascii_to_binary(ascii_message)
    pixels_needed = calculate_pixels_needed(binary_message)
    message_can_fit = pixel_check(pixels_needed, original_image)
    if message_can_fit:
        encode_message(binary_message, new_image)


# Driver Code
if __name__ == "__main__":

    # Calling main function
    main()
