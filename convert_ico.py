from PIL import Image

def convert_to_ico(png_path, ico_path):
    img = Image.open(png_path)
    # mod compatibility
    if img.mode != 'RGBA':
        img = img.convert('RGBA')
    
    # Save as ICO (can contain multiple sizes, but we'll specific 256, 128, 64, 48, 32, 16)
    img.save(ico_path, format='ICO', sizes=[(256, 256), (128, 128), (64, 64), (48, 48), (32, 32), (16, 16)])

if __name__ == "__main__":
    convert_to_ico("favicon.png", "favicon.ico")
