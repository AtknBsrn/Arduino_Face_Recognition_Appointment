import cv2
import mediapipe as mp

mp_face_detection = mp.solutions.face_detection
face_detection = mp_face_detection.FaceDetection()

def detect_face(frame):
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_detection.process(rgb_frame)

    if results.detections:
        face_coords = []
        for detection in results.detections:
            bboxC = detection.location_data.relative_bounding_box
            face_coords.append(bboxC)
        return face_coords
    return None
