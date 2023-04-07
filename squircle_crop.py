from PIL import Image, ImageDraw

def draw_superellipse_transparent(size, exponent, color):
    # Create a new image with a transparent background
    image = Image.new("RGBA", size, (0, 0, 0, 0))

    # Create a drawing object
    draw = ImageDraw.Draw(image)

    # Draw the superellipse
    for x in range(size[0]):
        for y in range(size[1]):
            px = abs(x - size[0]//2)**exponent
            py = abs(y - size[1]//2)**exponent
            if (px + py)**(1/exponent) < size[0]//2:
                draw.point((x, y), fill=color)

    return image

def crop_with_superellipse(image_path, exponent = 8):
    # Load the original image
    image = Image.open(image_path)
    assert image.width == image.height, "image should be square"

    # Define parameters for superellipse
    size  = (image.width, image.height)
    
    # Create a new image with a transparent background
    cropped_image = Image.new("RGBA", size, (0, 0, 0, 0))

    # Create a drawing object
    mask = Image.new("L", size, 0)
    draw = ImageDraw.Draw(mask)

    # Draw the superellipse
    for x in range(size[0]):
        for y in range(size[1]):
            px = abs(x - size[0]//2)**exponent
            py = abs(y - size[1]//2)**exponent
            if (px + py)**(1/exponent) < size[0]//2:
                draw.point((x, y), fill=255)
    
    # Apply mask to the new image as alpha channel
    cropped_image.putalpha(mask)

    # Paste the original image onto the new image using the alpha channel
    cropped_image.paste(image, (0, 0), mask=mask)

    # Return the cropped image
    return cropped_image

if __name__ == '__main__':

    # # Draw superellipse
    # squircle = draw_superellipse_transparent((800, 800), 4, 'black')
    # squircle.show()
    # del(squircle)
    
    # Load the original image
    original_image_path = "square_input.jpg"

    # Crop the image with the superellipse as a mask
    cropped_image = crop_with_superellipse(original_image_path, 4)
    cropped_image.show()