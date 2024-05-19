# Import necessary libraries
import numpy as np
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
import cv2
import pandas as pd
from tensorflow.keras.models import load_model

IMAGE_SIZE = (224, 224, 3)
CATEGORIES = ['Autistic', 'Normal']

model = load_model("Model\AutismDetection_resnet_101_v2_model.h5")

def detect_Autism(imgpath):
    img = cv2.imread(imgpath)
    img = cv2.resize(img, (IMAGE_SIZE[0], IMAGE_SIZE[1]))
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    img_rotated_90 = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
    img_rotated_180 = cv2.rotate(img, cv2.ROTATE_180)
    img_rotated_270 = cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)
    img_flip_ver = cv2.flip(img, 0)
    img_flip_hor = cv2.flip(img, 1)

    images = []
    images.append(img)
    images.append(img_rotated_90)
    images.append(img_rotated_180)
    images.append(img_rotated_270)
    images.append(img_flip_ver)
    images.append(img_flip_hor)

    images = np.array(images)
    images = images.astype(np.float32)
    images /= 255

    op = []
    # make predictions on the input image
    for im in images:
        image = np.array(im)
        image = np.expand_dims(image, axis=0)
        pred = model.predict(image)
        pred = pred.argmax(axis=1)[0]
        op.append(pred)
        # print("Pred:", pred, CATEGORIES[pred])

    op = np.array(op)

    print("Final Output:", CATEGORIES[np.bincount(np.array(op)).argmax()])
    return  CATEGORIES[np.bincount(np.array(op)).argmax()]

def model_prediction(image, input_data):

    # Detect autism from the image
    dl_output = detect_Autism(image)

    # Load the data
    data = pd.read_csv("files/final-data.csv")
    X = data.drop(columns=["Qchat-10-Score"])
    y = data["Qchat-10-Score"]

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
    
    # Create and train the model
    rf_model = DecisionTreeClassifier()
    rf_model.fit(X_train, y_train)
    
    # Predict using the input data
    prediction = rf_model.predict([input_data])
    
    # Define output and therapy default values
    Output, Therapy = "Very begining level of autism","Extra Love & Care will subside the symptoms"

    # Define output mapping
    output_mapping = {
        ("Autistic", (7, 11)): ("Level 3 - Requiring Very Substantial Support", "Intensive interventions, Individualized education plans, and Support for daily living skills."),
        ("Autistic", (4, 7)): ("Level 2 - Requiring Substantial Support", "Applied behavior analysis (ABA), Speech therapy, and Specialized education programs."),
        ("Autistic", (0, 4)): ("Level 1 - Requiring Support", "Social skills training, Speech therapy, and Occupational therapy."),
        ("Normal", None): ("Normal Child", "NO ASD Traits")
    }

    # Check if the DL output and prediction range match any entry in the dictionary
    for key, (output, therapy) in output_mapping.items():
        dl_output_match = key[0] == dl_output
        prediction_match = isinstance(key[1], tuple) and (key[1][0] < prediction <= key[1][1]) if key[1] else True
        if dl_output_match and prediction_match:
            Output, Therapy = output, therapy
            break

    return dl_output, Output, Therapy

if __name__ =="__main__":

    print(model_prediction("files/test data/0065.jpg",(0,0,0,0,0,0,0,0,0,0)))