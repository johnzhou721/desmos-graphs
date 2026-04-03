from PIL import Image
import numpy as np

INPUT_FILE = "icepalace.png"
OUTPUT_FILE = "icepalace-transparent.png"

# Load image as RGBA
img = Image.open(INPUT_FILE).convert("RGBA")
data = np.array(img, dtype=float)

# Separate channels
r, g, b, a = data[:,:,0], data[:,:,1], data[:,:,2], data[:,:,3]

# Normalize RGB to 0-1
r /= 255.0
g /= 255.0
b /= 255.0
a /= 255.0

# Unpremultiply: calculate alpha based on how much black was blended
# Formula: alpha = max(R,G,B)
new_alpha = np.max([r, g, b], axis=0)

# Prevent division by zero
factor = np.where(new_alpha > 0, 1 / new_alpha, 0)

# Recover original colors before black blending
r_new = r * factor
g_new = g * factor
b_new = b * factor

# Clip values
r_new = np.clip(r_new, 0, 1)
g_new = np.clip(g_new, 0, 1)
b_new = np.clip(b_new, 0, 1)
a_new = np.clip(new_alpha, 0, 1)

# Convert back to 0-255
out_data = np.stack([r_new, g_new, b_new, a_new], axis=2) * 255
out_data = out_data.astype(np.uint8)

# Save transparent image
out_img = Image.fromarray(out_data, 'RGBA')
out_img.save(OUTPUT_FILE)

print(f"Saved {OUTPUT_FILE} — black fully transparent, semi-transparent preserved!")
