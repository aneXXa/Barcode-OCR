from barcodeDetection import detection as det

import cv2
import numpy as np
import pytesseract
import os

_candidate_tess_paths = [
    r"C:\\Program Files\\Tesseract-OCR\\tesseract.exe",
    r"C:\\Program Files (x86)\\Tesseract-OCR\\tesseract.exe",
]
for _p in _candidate_tess_paths:
    if os.path.exists(_p):
        pytesseract.pytesseract.tesseract_cmd = _p
        break


def ocr_digits_from_rects(image_path: str, rects: list[tuple[int, int, int, int]]) -> str:
    """
    Run OCR on detected barcode rectangles. First tries full area, then lower half if no results.
    """
    img = cv2.imread(image_path)
    if img is None or rects is None or (isinstance(rects, (list, tuple)) and len(rects) == 0):
        return ""

    digits_all = []
    for (x1, y1, x2, y2) in rects:
        roi_full = img[y1:y2, x1:x2]
        if roi_full.size == 0:
            continue
            
        result_full = perform_ocr_on_roi(roi_full)
        
        if not result_full:
            height = y2 - y1
            lower_half_y1 = y1 + (height // 2)
            lower_half_y2 = y2
            
            roi_lower = img[lower_half_y1:lower_half_y2, x1:x2]
            if roi_lower.size > 0:
                result_lower = perform_ocr_on_roi(roi_lower)
                if result_lower:
                    digits_all.append(result_lower)
        else:
            digits_all.append(result_full)

    return " ".join(digits_all)


def perform_ocr_on_roi(roi):
    """
    Perform OCR on a given ROI and return the best result.
    """
    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    scale = 2.0
    gray = cv2.resize(gray, (int(gray.shape[1] * scale), int(gray.shape[0] * scale)), interpolation=cv2.INTER_CUBIC)
    thr = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 51, 4)
    if np.mean(thr) < 127:
        thr = cv2.bitwise_not(thr)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
    thr = cv2.morphologyEx(thr, cv2.MORPH_CLOSE, kernel)

    configs = [
        "--oem 3 --psm 7 -c tessedit_char_whitelist=0123456789",
        "--oem 3 --psm 6 -c tessedit_char_whitelist=0123456789",
        "--oem 3 --psm 8 -c tessedit_char_whitelist=0123456789",
    ]
    candidates = []
    for cfg in configs:
        try:
            txt = pytesseract.image_to_string(thr, config=cfg)
            digits = "".join(ch for ch in txt if ch.isdigit())
            if digits:
                candidates.append(digits)
        except Exception:
            continue
    
    if candidates:
        def score(s: str) -> tuple:
            return (0 if len(s) in (8, 12, 13) else 1, -len(s))
        best = sorted(candidates, key=score)[0]
        return best
    
    return ""




def extract_barcodes_with_ocr(image_path, output_path="barcode_detected.jpg"):
    """
    Detect barcodes and print OCR digits to console from expanded ROIs.
    Also adds text labels to the output image.
    Uses submodule functions for detection.
    """
    success = det.extract_barcodes(image_path, output_path)
    if not success:
        return False

    rects = det.get_expanded_barcode_rects(image_path)
    if not rects:
        return False
    
    digits = ocr_digits_from_rects(image_path, rects)
    
    img = cv2.imread(image_path)
    if img is not None:
        for rect in rects:
            x1, y1, x2, y2 = rect
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 3)
        
        if digits:
            digit_tokens = digits.split()
            text_x = 10
            text_y = 30
            line_height = 35
            
            for i, token in enumerate(digit_tokens):
                text = f"Barcode: {token}"
                y_pos = text_y + (i * line_height)
                
                cv2.putText(img, text, (text_x, y_pos), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)
                cv2.putText(img, text, (text_x, y_pos), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 4) 
        else:
            cv2.putText(img, "Barcode: not recognized", (10, 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)
            cv2.putText(img, "Barcode: not recognized", (10, 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
        
        cv2.imwrite(output_path, img)
    
    if digits:
        for token in digits.split():
            print(f"Barcode: {token}")
    else:
        print("Barcode: not recognized")

    return True


def main():
    """
    Detect barcodes and save outlined images with OCR digits.
    """
    print("=== Barcode Detection with OCR ===")

    test_images = [
        "./test/barcode1.jpg",
        "./test/barcode2.png",
        "./test/barcode3.jpg",
        "./test/barcode4.png",
        "./test/barcode5.png",
    ]

    for i, image_path in enumerate(test_images):
        print(f"\n--- Processing image {i+1}: {image_path} ---")
        output_path = f"barcode_detected_{i+1}.jpg"
        extract_barcodes_with_ocr(image_path, output_path)


if __name__ == "__main__":
    main()