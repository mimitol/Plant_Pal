import tensorflow as tf
import PIL
from PIL import Image
import numpy as np
from DB import DB_access
import json

class_labels = None
model = None
from exceptions import InvalidInputError


def get_config_details():
    global class_labels, model
    with open(r'C:\Users\user\PycharmProjects\pythonProject3\Configuration\configuration.json', 'r') as config_file:
        config_data = json.load(config_file)
    class_labels = config_data["model_categories"]
    model = tf.keras.models.load_model(config_data["model_address"])


# פונקציה שמשקללת את תוצאות שלוש הפרדיקציות ומחזירה את שלוש הקטגוריות שקיבלו הכי הרבה אחוזים
def getTopThree(combined_prediction):
    # קריאת קובץ הקונפיגורציה
    global class_labels
    # class_labels = ['0', '1', '10', '11', '12', '13', '2', '3', '4', '5', '6', '7', '8', '9']
    count_arr = [0] * len(class_labels)  # Assuming class_labels is the list of class names
    for i in range(len(combined_prediction)):  # Iterate over the length of combined_prediction
        for j in range(
                len(combined_prediction[i])):  # Iterate over the length of each inner list in combined_prediction
            index = int(combined_prediction[i][j])
            if index < len(count_arr):
                count_arr[index] += (3 - j)

    indexed_values = list(enumerate(count_arr))
    sorted_values = sorted(indexed_values, key=lambda x: x[1], reverse=True)
    top_three_indexes = [index for index, _ in sorted_values[:3]]
    return top_three_indexes


# פונקציית הפרדיקציה
async def predictionFunc(images):
    print(images)
    global class_labels, model
    if not class_labels or not model:
        get_config_details()
    combined_prediction = []
    # model = tf.keras.models.load_model("C:/Users/user/Desktop/my_first_project/saved_model_bh.keras")
    # class_labels = ['0', '1', '10', '11', '12', '13', '2', '3', '4', '5', '6', '7', '8', '9']
    for image in images:
        image = Image.open(str(image))
        if image is not None:
            image = image.resize((180, 180))
            image = np.expand_dims(image, axis=0)
            predictions = model.predict(image)
            top_predicted_indices = np.argsort(predictions[0])[::-1][:3]
            top_predicted_labels = [class_labels[i] for i in top_predicted_indices]
            combined_prediction += [top_predicted_labels]
        else:
            raise InvalidInputError
    predicted_categories = getTopThree(combined_prediction)
    predicted_plants = []
    for category in predicted_categories:
        predicted_plants += await DB_access.execute_query(
            "SELECT plant_id,id_in_model,plant_name,picture FROM Plants WHERE id_in_model= ?;", category)
    return predicted_plants
