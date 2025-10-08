# Barcode OCR

A Python application for detecting barcodes in images and extracting their numeric content using computer vision and optical character recognition (OCR) techniques. This project demonstrates advanced image processing, barcode detection algorithms, and text recognition using OpenCV and Tesseract OCR.

## Requirements

### Python Dependencies

The following Python packages are required to run this application:

```
opencv-python>=4.5.5
numpy>=1.21.0
matplotlib>=3.4.3
pytesseract>=0.3.10
Pillow>=8.3.0
```

### System Requirements

- Python 3.7 or higher
- Operating System: Windows, macOS, or Linux
- Minimum 4GB RAM (recommended for image processing)
- Tesseract OCR engine installed on the system

### Tesseract OCR Installation

#### Windows

1. Download Tesseract from: https://github.com/UB-Mannheim/tesseract/wiki
2. Install to default location: `C:\Program Files\Tesseract-OCR\`
3. Add to PATH or the application will auto-detect common installation paths

#### macOS

```bash
brew install tesseract
```

#### Linux (Ubuntu/Debian)

```bash
sudo apt-get install tesseract-ocr
```

## Installation

### Method 1: Using pip (Recommended)

1. Clone or download this repository:

   ```bash
   git clone <repository-url>
   cd Barcode-OCR
   ```

2. Install the required dependencies:
   ```bash
   pip install opencv-python numpy matplotlib pytesseract Pillow
   ```

### Method 2: Using requirements.txt

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Method 3: Using conda

```bash
conda install opencv numpy matplotlib pytesseract pillow
```

## Usage

### Basic Usage

1. Run the main barcode detection script:

   ```bash
   python CV-3-12.py
   ```

2. The application will automatically process test images and display results:

   ```
   === Barcode Detection with OCR ===

   --- Processing image 1: ./test/barcode1.jpg ---
   Barcode: 1234567890123

   --- Processing image 2: ./test/barcode2.png ---
   Barcode: 9876543210987
   ```

3. Output images with detected barcodes will be saved as `barcode_detected_1.jpg`, `barcode_detected_2.jpg`, etc.

### Custom Image Processing

To process your own images, modify the `test_images` list in the `main()` function:

```python
test_images = [
    "path/to/your/image1.jpg",
    "path/to/your/image2.png",
]
```

### Supported Image Formats

The application supports all image formats that OpenCV can read, including:

- JPEG (.jpg, .jpeg)
- PNG (.png)
- BMP (.bmp)
- TIFF (.tiff, .tif)
- WebP (.webp)

## Implementation Details

### Core Components

- **`CV-3-12.py`**: Main application script

  - `extract_barcodes_with_ocr()`: Main function for barcode detection and OCR
  - `ocr_digits_from_rects()`: OCR processing on detected barcode regions
  - `perform_ocr_on_roi()`: Advanced OCR with multiple configurations and preprocessing

- **`barcodeDetection/detection.py`**: Barcode detection module
  - `extract_barcodes()`: Core barcode detection algorithm
  - `get_expanded_barcode_rects()`: Returns bounding rectangles for detected barcodes

### OCR Processing Pipeline

1. **Image Preprocessing**: Grayscale conversion, scaling, adaptive thresholding
2. **Morphological Operations**: Noise reduction and character enhancement
3. **Multiple OCR Configurations**: Different PSM (Page Segmentation Mode) settings
4. **Result Scoring**: Prioritizes common barcode lengths (8, 12, 13 digits)
5. **Fallback Strategy**: Tries full region, then lower half if initial OCR fails

### Detection Algorithm

- Uses OpenCV's barcode detection capabilities
- Expands detected regions for better OCR accuracy
- Implements robust error handling and fallback mechanisms

## Examples

### Sample Output

The application processes test images and generates:

- Console output with detected barcode numbers
- Annotated images with green rectangles around detected barcodes
- Text labels showing the recognized barcode numbers

### Expected Output Format

```
=== Barcode Detection with OCR ===

--- Processing image 1: ./test/barcode1.jpg ---
Barcode: 1234567890123

--- Processing image 2: ./test/barcode2.png ---
Barcode: 9876543210987
```

## Educational Context

**Novosibirsk State University (NSU)**  
**Bachelor's Program**: 15.03.06 - Mechatronics and Robotics (AI Profile)

_Project Activity Course - Task 3_  
_Computer Vision Algorithms in Python_

## Features

- **Automatic Barcode Detection**: Uses OpenCV's built-in barcode detection algorithms
- **Advanced OCR Processing**: Multiple OCR configurations with intelligent result scoring
- **Robust Preprocessing**: Image enhancement techniques for better recognition accuracy
- **Fallback Mechanisms**: Multiple strategies for difficult-to-read barcodes
- **Visual Output**: Annotated images showing detection results
- **Cross-Platform**: Works on Windows, macOS, and Linux

## Troubleshooting

### Common Issues

1. **Tesseract Not Found**: Ensure Tesseract OCR is installed and accessible
2. **No Barcodes Detected**: Check image quality and barcode visibility
3. **Poor OCR Results**: Try different image preprocessing or higher resolution images
4. **Memory Issues**: Process smaller images or reduce batch size

### Performance Tips

- Use high-resolution images for better OCR accuracy
- Ensure good lighting and contrast in source images
- For batch processing, consider processing images individually

## Contributing

Feel free to submit issues, feature requests, or pull requests to improve this project.

## License

This project is part of an educational curriculum at Novosibirsk State University.
