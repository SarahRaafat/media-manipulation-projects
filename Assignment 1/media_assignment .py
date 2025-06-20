# -*- coding: utf-8 -*-
"""Media Assignment.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1DNylDMt-ZafJRt4_I9Ay9ik2N6tVVL2b
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import ndimage

print("Phase 1: Loading and Revealing the Image")

# Load the image data from CSV
image_data = np.loadtxt('/content/secret_image .csv', delimiter=',')
print(f"Image shape: {image_data.shape}")

# Display the original grayscale image
plt.figure(figsize=(10, 8))
plt.subplot(2, 2, 1)
plt.title('Original Grayscale Image')
plt.imshow(image_data, cmap='gray')
plt.colorbar()

# Display with 'hot' colormap
plt.subplot(2, 2, 2)
plt.title('Hot Colormap')
plt.imshow(image_data, cmap='hot')
plt.colorbar()

# Display with 'cool' colormap
plt.subplot(2, 2, 3)
plt.title('Cool Colormap')
plt.imshow(image_data, cmap='cool')
plt.colorbar()

# Display with 'viridis' colormap
plt.subplot(2, 2, 4)
plt.title('Viridis Colormap')
plt.imshow(image_data, cmap='viridis')
plt.colorbar()

plt.tight_layout()
plt.savefig('phase1_visualizations.png')
plt.show()

# Phase 2: Pattern Detection and Analysis
print("\nPhase 2: Pattern Detection and Analysis")

# Find black pixels (assuming black is 0)
black_pixels = np.where(image_data == 0)
num_black_pixels = len(black_pixels[0])

print(f"Number of black pixels: {num_black_pixels}")

# Extract coordinates of black pixels
black_pixel_coordinates = list(zip(black_pixels[0], black_pixels[1]))
print("Coordinates of all black pixels:")
for i, coord in enumerate(black_pixel_coordinates):
    print(f"  Pixel {i+1}: {coord}")

# Determine the bounding box
if num_black_pixels > 0:
    min_y, max_y = min(black_pixels[0]), max(black_pixels[0])
    min_x, max_x = min(black_pixels[1]), max(black_pixels[1])

    bounding_box = (min_y, min_x, max_y, max_x)
    print(f"Bounding box (min_y, min_x, max_y, max_x): {bounding_box}")

    # Visualize the bounding box
    plt.figure(figsize=(8, 8))
    plt.imshow(image_data, cmap='gray')
    plt.plot([min_x, max_x, max_x, min_x, min_x],
             [min_y, min_y, max_y, max_y, min_y], 'r-', linewidth=2)
    plt.title('Black Pixels and Bounding Box')
    plt.savefig('phase2_bounding_box.png')
    plt.show()

    # Pattern Analysis
    print("\nPattern Analysis:")

    # Check if the black pixels form horizontal line segments (potential mouth)
    rows_with_black = np.unique(black_pixels[0])
    potential_mouth_rows = []

    for row in rows_with_black:
        black_in_row = np.where(image_data[row, :] == 0)[0]
        if len(black_in_row) > 3:  # If multiple consecutive black pixels in a row
            potential_mouth_rows.append(row)

    # Look for symmetry (eyes)
    potential_eyes = []
    for i in range(len(black_pixel_coordinates)):
        for j in range(i+1, len(black_pixel_coordinates)):
            y1, x1 = black_pixel_coordinates[i]
            y2, x2 = black_pixel_coordinates[j]

            # Check if two black pixels are at same height (y-coordinate)
            # and symmetrically positioned horizontally
            if y1 == y2 and abs(x1 - (image_data.shape[1] - x2)) < 5:
                potential_eyes.append(((y1, x1), (y2, x2)))
                break

    if potential_mouth_rows:
        print(f"  Found potential mouth features at rows: {potential_mouth_rows}")

    if potential_eyes:
        print(f"  Found potential eye features: {potential_eyes[:2]}")

    # Determine if there's a face-like structure
    has_face_structure = len(potential_eyes) > 0 and len(potential_mouth_rows) > 0
    if has_face_structure:
        print("  The pattern appears to have a face-like structure with eyes and mouth!")
    else:
        print("  No clear face-like structure detected.")
else:
    print("No black pixels found in the image.")

print("\nPhase 3: Modifying the Image")

# Normalize grayscale to range [0, 1] and convert to RGB
rgb_image = np.stack([image_data] * 3, axis=-1) / 255.0

# Only proceed if black pixels were found
if num_black_pixels > 0:
    mid_y = min_y + (max_y - min_y) // 2

    # Separate pixels into upper (eyes) and lower (mouth) regions
    eye_pixels = [(y, x) for y, x in black_pixel_coordinates if y <= mid_y]
    mouth_pixels = [(y, x) for y, x in black_pixel_coordinates if y > mid_y]

    # === EYES: Cluster and color red ===
    eye_clusters = []
    visited = set()

    for pixel in eye_pixels:
        if pixel in visited:
            continue
        cluster = [pixel]
        visited.add(pixel)
        i = 0
        while i < len(cluster):
            y0, x0 = cluster[i]
            for dy in [-1, 0, 1]:
                for dx in [-1, 0, 1]:
                    neighbor = (y0 + dy, x0 + dx)
                    if neighbor in eye_pixels and neighbor not in visited:
                        cluster.append(neighbor)
                        visited.add(neighbor)
            i += 1
        eye_clusters.append(cluster)

    # Keep top 2 clusters (assumed eyes)
    eye_clusters.sort(key=len, reverse=True)
    for cluster in eye_clusters[:2]:
        for y, x in cluster:
            rgb_image[y, x] = [1.0, 0.0, 0.0]  # Red

    # === MOUTH: Flip to sad face ===
    if mouth_pixels:
        mouth_center_y = int(sum(y for y, _ in mouth_pixels) / len(mouth_pixels))
        bg_gray = np.median(image_data) / 255.0

        # Remove original mouth
        for y, x in mouth_pixels:
            rgb_image[y, x] = [bg_gray] * 3

        # Reflect mouth vertically around center
        for y, x in mouth_pixels:
            flipped_y = 2 * mouth_center_y - y
            if 0 <= flipped_y < rgb_image.shape[0]:
                rgb_image[flipped_y, x] = [0, 0, 0]

# === Add Blue Border ===
border_width = 5
h, w = rgb_image.shape[:2]
bordered_image = np.ones((h + 2 * border_width, w + 2 * border_width, 3))  # default white

# Fill border with blue
bordered_image[:border_width, :, :2] = 0  # top
bordered_image[-border_width:, :, :2] = 0  # bottom
bordered_image[:, :border_width, :2] = 0  # left
bordered_image[:, -border_width:, :2] = 0  # right

# Place RGB image in center
bordered_image[border_width:-border_width, border_width:-border_width] = rgb_image

# === Display and Save ===
plt.figure(figsize=(8, 8))
plt.imshow(bordered_image)
plt.title('Modified Image: Red Eyes, Blue Border, Sad Mouth')
plt.savefig('phase3_modified_image.png')
plt.show()

# Phase 4: Apply a Noise Reduction Filter
print("\nPhase 4: Applying Noise Reduction Filter (Size = 2)")

# Apply mean filter with size 2
filter_size = 2
filtered_image = ndimage.uniform_filter(bordered_image, size=filter_size)

# Display and save the original and filtered image
plt.figure(figsize=(15, 7))

plt.subplot(1, 2, 1)
plt.imshow(bordered_image)
plt.title('Original Modified Image (Noisy)')

plt.subplot(1, 2, 2)
plt.imshow(filtered_image)
plt.title(f'Denoised Image (Mean Filter, Size={filter_size})')

plt.savefig('phase4_denoised_comparison.png')
plt.show()

# Also save individual images for submission
plt.figure(figsize=(8, 8))
plt.imshow(bordered_image)
plt.title('Original Modified Image (Noisy)')
plt.savefig('phase4_original_noisy.png')
plt.close()

plt.figure(figsize=(8, 8))
plt.imshow(filtered_image)
plt.title(f'Denoised Image (Mean Filter, Size={filter_size})')
plt.savefig('phase4_denoised.png')
plt.close()

# Phase 4: Apply a Noise Reduction Filter (Preserving Key Pixels)
print("\nPhase 4: Applying Noise Reduction Filter (Size = 2)")

# Make a copy of the bordered image for filtering
filtered_image = np.copy(bordered_image)

# Coordinates of black pixels in the original grayscale image (before border)
black_pixel_coords = [
    (5, 5), (5, 14), (13, 6), (13, 12),
    (14, 7), (14, 8), (14, 9), (14, 10), (14, 11)
]

# Create a mask to protect specific pixels from filtering
protected_mask = np.zeros_like(bordered_image[:, :, 0], dtype=bool)

# Mark black pixels (adjusted for border offset)
for y, x in black_pixel_coords:
    protected_mask[y + border_width, x + border_width] = True
    print(f"Protected pixel at ({y + border_width}, {x + border_width})")

# Also protect red eye pixels and completely black pixels
for y in range(bordered_image.shape[0]):
    for x in range(bordered_image.shape[1]):
        pixel = bordered_image[y, x]
        is_red = pixel[0] > 0.9 and pixel[1] < 0.1 and pixel[2] < 0.1
        is_black = np.all(pixel < 0.01)
        if is_red or is_black:
            protected_mask[y, x] = True

print(f"Total protected pixels: {np.sum(protected_mask)}")

# Apply mean filter with size 2
filter_size = 2
mean_filtered = ndimage.uniform_filter(bordered_image, size=filter_size)

# Replace only unprotected pixels
filtered_image[~protected_mask] = mean_filtered[~protected_mask]

# Show and save the comparison
plt.figure(figsize=(15, 7))

plt.subplot(1, 2, 1)
plt.imshow(bordered_image)
plt.title('Original Modified Image (Noisy)')

plt.subplot(1, 2, 2)
plt.imshow(filtered_image)
plt.title('Denoised Image (Mean Filter, Size=2, Protected Eyes & Blacks)')

plt.savefig('phase4_denoised_comparisonWithoutEyes.png')
plt.show()

# Also save individual images for submission
plt.figure(figsize=(8, 8))
plt.imshow(bordered_image)
plt.title('Original Modified Image (Noisy)')
plt.savefig('phase4_noisy.png')
plt.close()

plt.figure(figsize=(8, 8))
plt.imshow(filtered_image)
plt.title(f'Denoised Image without eyes and mouth (Mean Filter, Size={filter_size})')
plt.savefig('phase4_denoisedWithoutEyesAndMouth.png')
plt.close()

# Phase 5: Answer the questions
print("\nPhase 5: Answers to Questions")

print(f"1. How many black pixels were found? {num_black_pixels}")

print("2. What are the coordinates of the black pixels?")
print(f"   {black_pixel_coordinates[:5]} ... and {len(black_pixel_coordinates) - 5} more")

if 'bounding_box' in locals():
    print(f"3. What is the bounding box? {bounding_box}")
else:
    print("3. No bounding box found (no black pixels).")

print("4. What features did you detect in the image?")
if 'has_face_structure' in locals() and has_face_structure:
    print("   The image appears to contain a face-like structure with:")
    if 'potential_eyes' in locals() and potential_eyes:
        print(f"   - Eyes at approximately {[pair[0] for pair in potential_eyes[:2]]}")
    if 'potential_mouth_rows' in locals() and potential_mouth_rows:
        print(f"   - Mouth around rows {potential_mouth_rows}")
else:
    print("   No clear structured features detected.")