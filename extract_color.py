from PIL import Image
from collections import Counter

try:
    img = Image.open('frontend/assets/logos/logo.png')
    img = img.convert('RGBA')
    
    pixels = img.getdata()
    valid_pixels = []
    
    for r, g, b, a in pixels:
        if a > 0: # not transparent
            # not white/black
            if not (r > 240 and g > 240 and b > 240) and not (r < 20 and g < 20 and b < 20):
                # We are looking for BLUE, so let's specifically filter for colors where B is prominent
                if b > r and b > g:
                    valid_pixels.append((r, g, b))
                
    if valid_pixels:
        counter = Counter(valid_pixels)
        most_common = counter.most_common(5)
        for color, count in most_common:
            print(f"Blueish Color: #{color[0]:02x}{color[1]:02x}{color[2]:02x} - Count: {count}")
    else:
        print("No blueish colors found")
except Exception as e:
    print(e)
