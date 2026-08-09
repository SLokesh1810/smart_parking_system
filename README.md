# Smart Parking System — Computer Vision Prototype

A lightweight Computer Vision prototype for a research-oriented Smart Parking System. The current implementation focuses on **vehicle detection, license plate detection, and license plate recognition (OCR)** from road/parking-lot images.

> **Current status:** Version 1 — End-to-end ALPR prototype  
> Vehicle Detection → Vehicle Cropping → License Plate Detection → Plate Cropping → OCR

## Overview

The goal of this repository is to provide a small, working implementation of the Computer Vision component of a Smart Parking System.

Instead of attempting to build the complete parking-management platform, this prototype demonstrates the core AI pipeline that can later be integrated into a larger system.

The current pipeline:

1. Detects vehicles using YOLO.
2. Filters detections to relevant vehicle classes.
3. Crops each detected vehicle.
4. Detects the license plate inside the vehicle crop using a specialized YOLO license-plate detector.
5. Crops the detected license plate.
6. Uses EasyOCR to recognize the plate text.
7. Displays the detected vehicles and recognized plate numbers.

## System Architecture

```text
                 Input Image
                     │
                     ▼
          ┌─────────────────────┐
          │  YOLOv8 Vehicle     │
          │     Detection       │
          └──────────┬──────────┘
                     │
                     ▼
               Vehicle Crop
                     │
                     ▼
          ┌─────────────────────┐
          │ YOLOv11 License     │
          │ Plate Detection     │
          └──────────┬──────────┘
                     │
                     ▼
                Plate Crop
                     │
                     ▼
          ┌─────────────────────┐
          │      EasyOCR        │
          │ Text Recognition    │
          └──────────┬──────────┘
                     │
                     ▼
             License Plate Text
```

### Why two detection stages?

The vehicle detector and license-plate detector have different responsibilities.

The first YOLO model identifies vehicles in the complete image. Each vehicle is then cropped before running the second model, giving the license-plate detector a smaller and more focused image.

The plate detector returns coordinates relative to the vehicle crop, so the implementation also performs coordinate translation when drawing the plate location on the original image.

## Current Features

- Vehicle detection using YOLOv8
- Detection filtering for car, bus, truck, and motorcycle
- License plate detection using a pretrained YOLOv11-based model
- Vehicle and license-plate image cropping
- Coordinate transformation from vehicle-crop coordinates to original-image coordinates
- License plate text recognition using EasyOCR
- Confidence-based filtering
- OpenCV visualization of detections
- Separate model files

## Tech Stack

| Component | Technology |
|---|---|
| Programming Language | Python |
| Computer Vision | OpenCV |
| Vehicle Detection | Ultralytics YOLOv8n |
| License Plate Detection | YOLOv11-based pretrained detector |
| OCR | EasyOCR |
| Deep Learning Backend | PyTorch |
| Numerical Processing | NumPy |

## Models

### Vehicle Detector

The vehicle detector uses:

```text
YOLOv8n
```

The pretrained model detects general object classes, after which the application filters the results to vehicle-related classes.

### License Plate Detector

The license plate detector uses:

```text
license-plate-finetune-v1s.pt
```

This is a pretrained YOLOv11-based license-plate detection model selected because it provides a downloadable PyTorch checkpoint compatible with the Ultralytics inference workflow and performed well during initial testing.

**Important:** The license plate model is an external pretrained model. Review its original model card, dataset information, and license before redistribution or commercial use.

## Project Structure

A typical layout is:

```text
smart_parking_system/
│
├── models/
│   ├── yolov8n.pt
│   └── license-plate-finetune-v1s.pt
│
├── plate_detector.py
├── requirements.txt
├── road_image(1).jpg
└── README.md
```

The exact layout may evolve as the project is refactored into separate modules.

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/SLokesh1810/smart_parking_system.git
cd smart_parking_system
```

### 2. Create a virtual environment

Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Add the model weights

Place the required model files inside:

```text
models/
```

Expected files:

```text
models/yolov8n.pt
models/license-plate-finetune-v1s.pt
```

## Running the Prototype

Place a road or parking-lot image in the project directory and update the image path in the Python script if required.

Then run:

```bash
python plate_detector.py
```

The application performs:

```text
Load Image
    ↓
Detect Vehicles
    ↓
Crop Vehicles
    ↓
Detect License Plates
    ↓
Crop Plates
    ↓
Run EasyOCR
    ↓
Display Results
```

## Example Output

The current prototype can produce results similar to:

```text
Car
 └── License Plate
       └── WB22U7778
```

The system also reports OCR confidence values during inference.

Because this is a first-stage prototype, OCR can occasionally confuse visually similar characters, especially with small, angled, blurred, reflective, or low-resolution plates.

## Current Limitations

Version 1 is intentionally small and is **not intended to be a production-ready parking system**.

Current limitations include:

- OCR accuracy depends heavily on image quality.
- Small or highly angled license plates can be difficult to read.
- Lighting, reflections, blur, and occlusion can reduce OCR accuracy.
- The current implementation processes an image rather than providing a complete real-time parking deployment.
- No vehicle tracking is currently implemented.
- No parking-slot occupancy calculation is currently implemented.
- No database or persistent event logging is currently implemented.
- No dedicated Indian-license-plate fine-tuning has been performed yet.
- OCR preprocessing is currently limited and can be improved.

## Publication

### Smart Parking Safety and Surveillance System Using Computer Vision

**Intelligent Transportation and Smart Systems, IGI Global (2026)**

Proposed a multi-view smart parking pipeline integrating computer vision, IoT, and blockchain, with YOLO and OpenCV for real-time pedestrian and vehicle monitoring.

**DOI:** [10.4018/979-8-3373-4277-1.ch003](https://doi.org/10.4018/979-8-3373-4277-1.ch003)

## Responsible Use

License plate recognition can involve potentially sensitive vehicle-identification data.

Any real deployment should consider:

- Local privacy and data-protection requirements
- Appropriate data retention policies
- Access control
- Secure storage
- Purpose limitation
- Proper authorization for camera deployment

This repository is currently a research/educational prototype.

## Author

**Lokesh**

GitHub: https://github.com/SLokesh1810

## License

This project is licensed under the [MIT License](LICENSE).

> **Note:** The pretrained models used in this project may have separate licenses. Refer to their respective model repositories and licenses before redistributing or using them commercially.
