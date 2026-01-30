from PIL import Image, ImageChops, ImageDraw

def trim_and_circle(img_path, output_path):
    img = Image.open(img_path).convert("RGBA")
    
    # 1. Trim white/transparent padding
    # Create white background and find difference to find content
    white = Image.new("RGBA", img.size, (255, 255, 255, 255))
    diff = ImageChops.difference(img, white)
    # Also find non-transparent area
    bbox = img.getbbox()
    
    # Let's be aggressive: find first non-white-ish pixel
    # For a red logo on white, we can look for anything not near (255,255,255)
    width, height = img.size
    data = img.getdata()
    
    left, top, right, bottom = width, height, 0, 0
    
    # Threshold for "non-white"
    threshold = 240 
    
    for y in range(height):
        for x in range(width):
            r, g, b, a = data[y * width + x]
            if r < threshold or g < threshold or b < threshold:
                left = min(left, x)
                top = min(top, y)
                right = max(right, x)
                bottom = max(bottom, y)
    
    if left >= right or top >= bottom:
        # Fallback to whole image if detection fails
        left, top, right, bottom = 0, 0, width, height
    else:
        # Make it square based on the larger dimension to keep it centered
        w = right - left
        h = bottom - top
        size = max(w, h)
        cx, cy = (left + right) // 2, (top + bottom) // 2
        left = max(0, cx - size // 2)
        top = max(0, cy - size // 2)
        right = min(width, left + size)
        bottom = min(height, top + size)

    img = img.crop((left, top, right, bottom))
    width, height = img.size
    
    # 2. Apply circular mask
    mask = Image.new('L', (width, height), 0)
    draw = ImageDraw.Draw(mask)
    # Draw a slightly smaller circle to ensure no edge bleed
    draw.ellipse((1, 1, width-2, height-2), fill=255)
    
    result = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    result.paste(img, (0, 0), mask=mask)
    
    # 3. Resize to standard favicon size if needed (e.g. 512x512)
    result = result.resize((512, 512), Image.Resampling.LANCZOS)
    
    result.save(output_path)

if __name__ == "__main__":
    trim_and_circle("favicon.png", "favicon.png")
