import numpy as np
import tensorflow as tf
from PIL import Image


def load_model(model_path):
    interpreter = tf.lite.Interpreter(model_path=model_path)
    interpreter.allocate_tensors()
    return interpreter


def run_inference_for_single_image(model, image_path):
    input_details = model.get_input_details()
    # print("Model input details", input_details)
    # print("Model output details", model.get_output_details())

    # Check the type of the input tensor
    floating_model = input_details[0]["dtype"] == np.float32

    # NxHxWxC, H:1, W:2
    height = input_details[0]["shape"][1]
    width = input_details[0]["shape"][2]
    img = Image.open(image_path).resize((width, height))

    # add N dim
    input_data = np.expand_dims(img, axis=0)

    if floating_model:
        input_data = (np.float32(input_data) - 127.5) / 127.5

    model.set_tensor(input_details[0]["index"], input_data)

    model.invoke()

    boxes = model.get_tensor(337)[0]  # StatefulPartitionedCall:3 with index 337 - 3D tensor, bounding box coordinates of detected objects
    classes = model.get_tensor(338)[0]  # StatefulPartitionedCall:2 with index 338 - 2D tensor, class index of detected objects
    scores = model.get_tensor(339)[0]  # StatefulPartitionedCall:1 with index 339 - 2D tensor, confidence of detected objects

    return boxes, classes, scores


if __name__ == "__main__":
    model_path = "inference_graph/exporting/model.tflite"
    # model_path = "inference_graph/exporting/conesandcubes_b1.tflite" # uses edgetup-custom-op
    image_path = "./images/test/90189f4a-db35b31a-IMG_6588.JPG"

    detection_model = load_model(model_path)
    boxes, classes, scores = run_inference_for_single_image(detection_model, image_path)

    print("Boxes:", boxes)
    print("Classes:", classes)
    print("Scores:", scores)

# Command to run:
# python predict_image_tflite.py
