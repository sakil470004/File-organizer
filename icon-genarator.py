
from PIL import Image, ImageDraw, ImageFont

def create_icon(size):
    # Create a new image with white background
    image = Image.new('RGB', (size, size), 'white')
    draw = ImageDraw.Draw(image)
    
    # Draw a rounded rectangle for folder
    margin = size // 8
    folder_height = size - 2 * margin
    folder_width = size - 2 * margin
    
    # Draw folder (light blue)
    draw.rectangle(
        [margin, margin + folder_height//4, 
         margin + folder_width, margin + folder_height],
        fill='#4d94ff'
    )
    
    # Draw folder tab
    draw.rectangle(
        [margin, margin, 
         margin + folder_width//2, margin + folder_height//4],
        fill='#4d94ff'
    )
    
    # Draw sorting arrows
    arrow_color = 'white'
    arrow_size = size // 4
    
    # Down arrow
    points_down = [
        (size//2 - arrow_size//2, size//2),
        (size//2 + arrow_size//2, size//2),
        (size//2, size//2 + arrow_size//2)
    ]
    draw.polygon(points_down, fill=arrow_color)
    
    # Up arrow
    points_up = [
        (size//2 - arrow_size//2, size//2 + arrow_size//2),
        (size//2 + arrow_size//2, size//2 + arrow_size//2),
        (size//2, size//2)
    ]
    draw.polygon(points_up, fill=arrow_color)
    
    return image

# Create icons of different sizes
sizes = {
    '16x16': 16,
    '32x32': 32,
    '64x64': 64,
    '128x128': 128,
    '256x256': 256,
    '512x512': 512,
    '1024x1024': 1024
}

for name, size in sizes.items():
    icon = create_icon(size)
    icon.save(f'app.iconset/icon_{name}.png')
    if size <= 512:  # Create @2x version for Retina displays
        icon = create_icon(size * 2)
        icon.save(f'app.iconset/icon_{name}@2x.png')

print("Icon files generated in app.iconset directory")