from PIL import Image
import numpy as np
from multiprocessing import Pool
import os


def process_image(image_part, shift_value, color_channel):
    # Convert PIL Image to numpy array
    img_shift = np.array(image_part)

    # Shift the colour channel
    img_shift[..., color_channel] = (img_shift[..., color_channel] + shift_value).clip(
        0, 255
    )

    # Convert numpy array to PIL Image
    return Image.fromarray(img_shift.astype("uint8"))


def main():
    # CHANGE DIR PATH ON DIFFERENT PC!!!
    # 00000.png doesn't work at all
    img = Image.open("C:/Users/pitch/OneDrive/Desktop/paralel/logo.png")

    # Img dimesnions
    width, height = img.size

    # Calculate the size of each part
    part_height = height // 2
    part_width = width // 3

    # store image parts
    image_parts = []

    # Split the image into six equal parts!!!
    # Fucking UNEQUAL PARTS was causing the black bar!!!!
    # The parts were Random before
    for i in range(2):
        for j in range(3):
            left = j * part_width
            upper = i * part_height
            right = (j + 1) * part_width if j + 1 != 3 else width
            lower = (i + 1) * part_height if i + 1 != 2 else height
            part = img.crop((left, upper, right, lower))
            image_parts.append(part)

    # Define the shift values and color channels
    # negative values work, but need to subtract from the curent RGB value
    # NEGATIVE DOESN'T WORK WITH JUST 0-255 SETTING!!!
    shift_RGB_value = [50, 75, 100, -50, -75, -100]
    color_channels = [0, 1, 2, 2, 1, 0]  # 0: Red, 1: Green, 2: Blue

    # Create a multiprocessing Pool
    with Pool() as p:
        # Process each part in parallel
        processed_parts = p.starmap(
            process_image, zip(image_parts, shift_RGB_value, color_channels)
        )

    # Merge to single image
    final_img = Image.new("RGB", img.size)
    for i in range(2):
        for j in range(3):
            final_img.paste(
                processed_parts[i * 3 + j], (j * part_width, i * part_height)
            )

    # Save dir
    # Be carefull with typos! Fallback was a bad idea!
    # CHANGE DIR PATH ON DIFFERENT PC!!!
    directory = "C:/Users/pitch/OneDrive/Desktop/paralel"

    # mistake fallback
    # Create new dir if it doesn't exist
    if not os.path.exists(directory):
        os.mkdir(directory)

    # New image save name
    image_path = os.path.join(directory, "final14.jpg")

    # save img
    final_img.save(image_path)


if __name__ == "__main__":
    main()
