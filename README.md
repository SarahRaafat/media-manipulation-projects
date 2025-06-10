
## 📁 Repository Overview
This repository contains two major assignments from the "Introduction to Media Informatics" course. Both assignments focus on practical manipulation and analysis of media data including images, video, and audio using Python, OpenCV, NumPy, and other libraries.

---

## 📌 Assignment 1 – Secret Image Analysis  
### Location: `assignment_1_secret_image/`

This assignment focuses on raster image processing and pixel-based pattern detection using NumPy and Matplotlib.

### 🧠 Key Tasks:
- Load and visualize a grayscale image stored as a `.csv` file.
- Apply colormaps (`hot`, `cool`, `viridis`) to reveal patterns.
- Detect black pixels and analyze their positions.
- Modify the image:
  - Detect and recolor “eyes”
  - Add blue border
  - Flip the mouth to create a sad face
- Apply mean filtering to reduce noise.

### 📦 Contents:
- `secret_image.ipynb` – the main Jupyter notebook with all steps.
- `secret_image.py` – script version of the notebook.
- `report_assignment_1.pdf` – report answering all phase 5 questions.
- `output_images/` – saved visualizations including colormap images and modified outputs.
- `secret_image.csv` – the input grayscale image.

---

## 📌 Assignment 2 – Video and Audio Processing  
### Location: `assignment_2_media_processing/`

This assignment explores three advanced topics in media informatics: motion detection, audio processing, and video interlacing simulation.

### 🧠 Key Tasks:
**Phase 1 – Hidden Letter Detection**  
- Use motion detection to extract hidden letters from each video frame.

**Phase 2 – Audio Extraction and Denoising**  
- Extract audio from a video and apply a noise reduction filter.

**Phase 3 – Simulating Interlaced Scanning**  
- Create two interlaced videos (odd/even scanlines).
- Compare the first frames side-by-side with a zoom-in effect.


Technologies Used
- Python 3.10+
- NumPy
- OpenCV
- Matplotlib
- SciPy (for audio filtering)
- MoviePy (for video/audio processing)


Authors
- Team of 2 
