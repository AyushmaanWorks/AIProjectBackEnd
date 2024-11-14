import cv2
from keras.models import model_from_json
import numpy as np

with open("./model/model.json", "r") as json_file:
    model_json = json_file.read()
model = model_from_json(model_json)

model.load_weights("./model/model_weights.h5")
haar_file = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
face_cascade = cv2.CascadeClassifier(haar_file)

labels = {
    0: "angry",
    1: "disgust",
    2: "fear",
    3: "happy",
    4: "neutral",
    5: "sad",
    6: "surprise",
}


def extract_features(image):
    feature = np.array(image)
    feature = feature.reshape(1, 48, 48, 1)
    return feature / 255.0


def process_image(path: str) -> str | None:
    im = cv2.imread(path)
    gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(im, 1.3, 5)

    if len(faces) == 0:
        return "unknown"

    try:
        for p, q, r, s in faces:
            image = gray[q : q + s, p : p + r]
            cv2.rectangle(im, (p, q), (p + r, q + s), (255, 0, 0), 2)
            image = cv2.resize(image, (48, 48))
            img = extract_features(image)
            pred = model.predict(img)
            prediction_label = labels[pred.argmax()]
            return prediction_label
    except cv2.error:
        return "unknown"
