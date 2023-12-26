import wget

MODEL_FILE = "ssd_mobilenet_v2_fpnlite_320x320_coco17_tpu-8.tar.gz"

model_link = "http://download.tensorflow.org/models/object_detection/tf2/20200711/" + MODEL_FILE
wget.download(model_link)
import tarfile

tar = tarfile.open(MODEL_FILE)
tar.extractall('.')
tar.close()
