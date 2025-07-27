import cv2
import numpy as np
from sort import Sort

net = cv2.dnn.readNet("yolov3.weights", "yolov3.cfg")
layer_names = net.getLayerNames()
output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]
fgbg = cv2.createBackgroundSubtractorMOG2(history=500, varThreshold=150, detectShadows=False)
tracker = Sort()

def detect_and_track(frame):
    mask = fgbg.apply(frame)
    kernel = np.ones((3, 3), np.uint8)
    motion_mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    blob = cv2.dnn.blobFromImage(frame, 1/255.0, (416, 416), swapRB=True, crop=False)
    net.setInput(blob)
    detections = net.forward(output_layers)

    boxes = []
    confidences = []
    for output in detections:
        for detection in output:
            scores = detection[5:]
            confidence = np.max(scores)
            if confidence > 0.5:
                center_x = int(detection[0] * frame.shape[1])
                center_y = int(detection[1] * frame.shape[0])
                w = int(detection[2] * frame.shape[1])
                h = int(detection[3] * frame.shape[0])
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)
                roi = motion_mask[max(y, 0):min(y + h, frame.shape[0]), max(x, 0):min(x + w, frame.shape[1])]
                motion_level = np.sum(roi) / 255
                if motion_level > 50:
                    boxes.append([x, y, w, h])
                    confidences.append(float(confidence))

    indices = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
    dets = []
    if indices is not None and len(indices) > 0:
        for i in indices:
            i = i[0] if isinstance(i, (list, np.ndarray)) else i
            x, y, w, h = boxes[i]
            dets.append([x, y, x + w, y + h, confidences[i]])
    else:
        dets = np.empty((0, 5))

    if len(dets) > 0:
        dets = np.array(dets)
    tracks = tracker.update(dets)

    for track in tracks:
        x1, y1, x2, y2, _ = track.astype(int)
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0,255,255), 2)

    return frame
