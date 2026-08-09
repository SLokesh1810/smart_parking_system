import cv2
from ultralytics import YOLO
import easyocr

# Load models
vehicle_model = YOLO("models/yolov8n.pt")
plate_model = YOLO("models/license-plate-finetune-v1s.pt")
reader = easyocr.Reader(['en'])

# Read image
frame = cv2.imread("road_image(1).jpg")

allowed = {"car", "bus", "truck", "motorcycle"}

# Detect vehicles
vehicle_results = vehicle_model(frame)

for vehicle_box in vehicle_results[0].boxes:
    confidence = float(vehicle_box.conf[0])
    if confidence < 0.5:
        continue

    class_id = int(vehicle_box.cls[0])
    label = vehicle_results[0].names[class_id]

    if label not in allowed:
        continue

    x1, y1, x2, y2 = map(int, vehicle_box.xyxy[0])

    # Draw vehicle box
    cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)
    cv2.putText(frame, label, (x1, y1 - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)

    # Crop vehicle
    vehicle_crop = frame[y1:y2, x1:x2]
    if vehicle_crop.size == 0:
        continue

    # Detect license plates
    plate_results = plate_model(vehicle_crop)
    for plate_box in plate_results[0].boxes:
        plate_conf = float(plate_box.conf[0])
        if plate_conf < 0.5:
            continue

        px1, py1, px2, py2 = map(int, plate_box.xyxy[0])

        # Crop plate from vehicle image
        plate_crop = vehicle_crop[py1:py2, px1:px2]
        if plate_crop.size == 0:
            continue

        results = reader.readtext(plate_crop)

        for result in results:
            text = result[1]
            confidence = result[2]
            print(f"{text} ({confidence:.2f})")

        if results:
            plate_text = results[0][1]
        else:
            plate_text = "Unknown"

        # Convert coordinates back to original image
        fx1 = x1 + px1
        fy1 = y1 + py1
        fx2 = x1 + px2
        fy2 = y1 + py2

        plate_label = f"{plate_text} ({plate_conf:.2f})"

        cv2.putText(
            frame,
            plate_label,
            (fx1, fy1 - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (0,255,0),
            2
        )

# Display final result
cv2.imshow("Smart Parking Detection", frame)

cv2.waitKey(0)
cv2.destroyAllWindows()