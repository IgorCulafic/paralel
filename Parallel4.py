from PIL import Image
import numpy as np
from multiprocessing import Pool, current_process
import os
import time


def process_image(image_part, shift_value, color_channel):
    # Record start time
    start_time = time.time()

    # Convert PIL Image to numpy array
    img_shift = np.array(image_part)

    # Shift the colour channel
    img_shift[..., color_channel] = (img_shift[..., color_channel] + shift_value).clip(
        0, 255
    )

    # Convert numpy array to PIL Image
    processed_img = Image.fromarray(img_shift.astype("uint8"))

    # Record end time
    end_time = time.time()

    # Calculate process time
    process_time = end_time - start_time

    # Get process name
    process_name = current_process().name

    return processed_img, process_name, process_time


def main():
    img = Image.open("C:/Users/pitch/OneDrive/Desktop/paralel/big_pic.jpg")

    width, height = img.size
    part_height = height // 2
    part_width = width // 3
    image_parts = []

    for i in range(2):
        for j in range(3):
            left = j * part_width
            upper = i * part_height
            right = (j + 1) * part_width if j + 1 != 3 else width
            lower = (i + 1) * part_height if i + 1 != 2 else height
            part = img.crop((left, upper, right, lower))
            image_parts.append(part)

    shift_RGB_value = [50, 75, 100, -50, -75, -100]
    color_channels = [0, 1, 2, 2, 1, 0]  # 0: Red, 1: Green, 2: Blue

    # Create a multiprocessing Pool
    with Pool() as p:
        results = p.starmap(
            process_image, zip(image_parts, shift_RGB_value, color_channels)
        )

    processed_parts = [result[0] for result in results]
    process_info = [(result[1], result[2]) for result in results]

    final_img = Image.new("RGB", img.size)
    for i in range(2):
        for j in range(3):
            final_img.paste(
                processed_parts[i * 3 + j], (j * part_width, i * part_height)
            )

    directory = "C:/Users/pitch/OneDrive/Desktop/paralel"
    if not os.path.exists(directory):
        os.mkdir(directory)

    image_path = os.path.join(directory, "final18.jpg")
    final_img.save(image_path)

    # Write process information to a .txt file
    with open(os.path.join(directory, "process_info4.txt"), "w") as f:
        for info in process_info:
            f.write(f"Process {info[0]} took {info[1]} seconds\n")


if __name__ == "__main__":
    main()
