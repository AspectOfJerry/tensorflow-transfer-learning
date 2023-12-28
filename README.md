# Installation

- Python version: 3.9
- Resources:
    - [Youtube Tutorial 1/4](https://youtu.be/rRwflsS67ow?list=PLAs-3cqyNbIjqaTLHNSu2g4kpaw6TGCud)
    - [Youtube Tutorial 2/4](https://youtu.be/O6BsjQat4aE?list=PLAs-3cqyNbIjqaTLHNSu2g4kpaw6TGCud)
    - [Youtube Tutorial 3/4](https://youtu.be/8ktcGQ-XreQ?list=PLAs-3cqyNbIjqaTLHNSu2g4kpaw6TGCud)
    - [Tensorflow Model Zoo](https://github.com/tensorflow/models/blob/master/research/object_detection/g3doc/tf2_detection_zoo.md)

To train on an NVIDIA GPU, you will need to install CUDA and cuDNN. I won't cover this in this guide (maybe later).
You can also use Google Colab to train your model (I won't cover this either).

### Clone Tensorflow Models repository

```bash
git clone https://github.com/tensorflow/models.git
```

As you will notice in this guide, most of the action happens in the `models/research/object_detection` folder.
DO NOT commit the `models/` folder to the repository (it should be ignored).

Unless you are fixing a script, please make your modifications in its copy to avoid committing your changes to the repository.

Because the Tensorflow Models repository is huge, make sure to modify/move the right scripts to the right place. It's easy to get lost in the files...

### Install Protobuf

<https://github.com/protocolbuffers/protobuf/releases>

Download the corresponding version of protobuf for your system and extract it to a folder (`C:\Users\<user>\AppData\Local\Programs\Python\`). Then, add the bin
folder to your PATH environment variable (`C:\Users\<user>\AppData\Local\Programs\Python\protoc-25.1-win64\bin`).

Restart your IDE/terminal and follow the next steps.

### Run protoc

Copy the `use_protobuf.py` file to the `models/research` folder and run the following command:

```bash
cd models/research
python use_protobuf.py object_detection/protos protoc
```

### Copying files

Copy the `setup.py` file from `models/research/object_detection/packages/tf2` to `models/research/` and run the following command:

```bash
cd models/research
python -m pip install .
```

Reinstall `numpy` because the included version is somehow broken:

```bash
pip install numpy==1.24.3 --force-reinstall
```

### Fix protobuf error

If you test the installation now, you should get the following error:

```bash
Traceback (most recent call last):
  File "C:<...>\tensorflow-transfer-learning\models\research\object_detection\builders\model_builder_tf2_test.py", line 24, in <module>
    from object_detection.builders import model_builder
  File "C:<...>\tensorflow-transfer-learning\venv\lib\site-packages\object_detection\builders\model_builder.py", line 23, in <module>
    from object_detection.builders import anchor_generator_builder
  File "C:<...>\tensorflow-transfer-learning\venv\lib\site-packages\object_detection\builders\anchor_generator_builder.py", line 26, in <module>
    from object_detection.protos import anchor_generator_pb2
  File "C:<...>\tensorflow-transfer-learning\venv\lib\site-packages\object_detection\protos\anchor_generator_pb2.py", line 9, in <module>
    from google.protobuf.internal import builder as _builder
ImportError: cannot import name 'builder' from 'google.protobuf.internal' (C:<...>\tensorflow-transfer-learning\venv\lib\site-packages\google\protobuf\internal\__init__.py)
```

Here's a clever fix from [Stack Overflow](https://stackoverflow.com/questions/71759248/importerror-cannot-import-name-builder-from-google-protobuf-internal):

1. Install the latest protobuf version and ignore dependency conflicts:

```bash
pip install --upgrade protobuf
```

2. Copy the `builder.py` file from `...\Lib\site-packages\google\protobuf\internal` to another folder (e.g. your desktop). If you are using PyCharm, you
   might need to reload the folder from disk to see the new files.
3. Re-install a compatible version of protobuf for this project (`3.19.6`):

```bash
pip install protobuf==3.19.6 --force-reinstall
```

4. Copy the `builder.py` file back to `...\Lib\site-packages\google\protobuf\internal` and replace the existing one.

### Test the installation

```bash
cd models/research/object_detection/builders
python model_builder_tf2_test.py
```

You should get the following output:

```
[...]
----------------------------------------------------------------------
Ran 24 tests in 13.296s

OK (skipped=1)
```

And you're done (for this part) 🎉!

# Setup

### Download the model

Install dependencies:

```bash
pip install wget
```

Copy the `model_downloader.py` file to the `models/research/object_detection` folder and run the following command:

```bash
cd models/research/object_detection
python model_downloader.py
```

You should see a folder with the model's name in the `models/research/object_detection` folder.

### (Optional) Choose a different model

Visit the [Tensorflow Model Zoo](https://github.com/tensorflow/models/blob/master/research/object_detection/g3doc/tf2_detection_zoo.md)

Change the `MODEL_FILE` variable in the `model_downloader.py` file to the model you want to use. Make sure to double-check the URL.

## (Optional) Test the setup

### Install dependencies

```bash
pip install opencv-contrib-python
```

If not already installed (`pip list`), install the following dependencies:

```bash
pip install opencv-python
pip install opencv-python-headless
```

For all the following commands, after copying the files, replace:

- the `-m` parameter with the name of the model you downloaded if you chose a different model.
- the `-l` parameter with the path to the label map file of the model you downloaded if you chose a different model.

### Predict on the included test images

Create a folder called `output` in the `models/research/object_detection` folder.
Copy the `predict_image.py` file to the `models/research/object_detection` folder and run the following command:

```bash
cd models/research/object_detection
python .\predict_image.py -m ssd_mobilenet_v2_fpnlite_320x320_coco17_tpu-8\saved_model -l .\data\mscoco_label_map.pbtxt -i .\test_images
```

The output should be in the `models/research/object_detection/output` folder (make sure you created the `output` folder).

### Predict on webcam

Copy the `predict_webcam.py` file to the `models/research/object_detection` folder and run the following command:

```bash
cd models/research/object_detection
python .\predict_webcam.py -m ssd_mobilenet_v2_fpnlite_320x320_coco17_tpu-8\saved_model -l .\data\mscoco_label_map.pbtxt
```

### Predict on a video

Copy the `predict_video.py` file to the `models/research/object_detection` folder and run the following command:
Replace `video.mp4` with the name of the video you want to use.
Move your video to the `models/research/object_detection` folder.

```bash
cd models/research/object_detection
python .\predict_video.py -m ssd_mobilenet_v2_fpnlite_320x320_coco17_tpu-8\saved_model -l .\data\mscoco_label_map.pbtxt -v .\video.mp4
```

And you're done (for this part) 🎉!

# Custom model/transfer learning!!!

Make sure the annotations are in Pascal VOC format.

### Prepare the dataset

Create a folder called `images` in the `models/research/object_detection` folder. Then, copy the custom dataset's `test` and `train` folders into the `images`
folder. The custom dataset is provided by me for private projects.

### Convert XML to CSV

Copy the `xml_to_csv.py` file to the `models/research/object_detection` folder and run the following command:

```bash
cd models/research/object_detection
python xml_to_csv.py
```

### Generate TFRecords

Copy the `generate_tfrecord.py` file to the `models/research/object_detection`.
Make sure to take a look at the `generate_tfrecord.py` file and apply the necessary changes (e.g. change the label map).

Run the following commands (you might need to change the paths):

```bash
cd models/research/object_detection
python generate_tfrecord.py --csv_input=images/train_labels.csv --image_dir=images/train --output_path=train.record
python generate_tfrecord.py --csv_input=images/test_labels.csv --image_dir=images/test --output_path=test.record
```

The `test.record` and `train.record` files should be in the `models/research/object_detection` folder.

### Create your label map

Copy the `label_map.pbtxt` file to the `models/research/object_detection` folder and adjust the following template to your needs:

```
item {
    id: 1
    name: "cone"
}

item {
    id: 2
    name: "cube"
}
add more if you need, make sure the names and ids are the same as the ones in generate_tfrecord.py
```

## Edit model config

Make sure to change the model name if you chose a different model.

Copy the `models/research/object_detection/configs/tf2/ssd_mobilenet_v2_fpnlite_320x320_coco17_tpu-8.config` file to the `models/research/object_detection`
folder.

Open the file and change the following values (in this case, I'm using the `ssd_mobilenet_v2_fpnlite_320x320_coco17_tpu-8` model)

| Line | Property                                               | To                                                                                                                                                  | Tested |
|------|--------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------|--------|
| 13   | `model.ssd.num_classes`                                | Number of classes in your dataset                                                                                                                   | 2      |
| 142  | `train_config.fine_tune_checkpoint`                    | Path to the model's checkpoint (e.g. `ssd_mobilenet_v2_fpnlite_320x320_coco17_tpu-8/checkpoint/ckpt-0`). remove `.index`, use forward slashes (`/`) | -      |
| 143  | `train_config.fine_tune_checkpoint_type`               | `detection`                                                                                                                                         | 16     |
| 144  | `train_config.batch_size`                              | Your batch size (depending on your specs). (e.g. `8`)                                                                                               | 3600   |
| 149  | `train_config.num_steps`                               | Number of steps to train the model (you can decrease it a bit) (e.g. `5000`)                                                                        | -      |
| 182  | `train_input_reader.label_map_path`                    | The label map file (e.g. `label_map.pbtxt`)                                                                                                         | -      |
| 184  | `train_input_reader.tf_record_input_reader.input_path` | Train TFRecord file (e.g. `train.record`)                                                                                                           | -      |
| 194  | `eval_input_reader.label_map_path`                     | The label map file (e.g. `label_map.pbtxt`)                                                                                                         | -      |
| 198  | `eval_input_reader.tf_record_input_reader.input_path`  | Test TFRecord file (e.g. `test.record`)                                                                                                             | -      |

### (Optional) Tensorboard

To monitor the training process, run the following command in a new terminal in the same environment:

```bash
cd models/research/object_detection
tensorboard --logdir=training --bind_all
```

- `--logdir` is the path to the folder where the model and checkpoints are saved.
- `--bind_all` is optional, it will allow you to access Tensorboard from other devices in your network.

Then, open your browser and go to <http://localhost:6006/>

You are now ready to train your model!

### Train the model

To start training, run the following command:

```bash
cd models/research/object_detection
python model_main_tf2.py --model_dir=training --pipeline_config_path=ssd_mobilenet_v2_fpnlite_320x320_coco17_tpu-8.config --alsologtostderr
```

- `--model_dir` is the path to the folder where the model and checkpoints will be saved.
- `--pipeline_config_path` is the path to the model's config file (e.g. `ssd_mobilenet_v2_fpnlite_320x320_coco17_tpu-8.config`)
- `--alsologtostderr` is optional, it will print the logs to the console.

### (Optional) Resume training

Need a break during training? No problem! To resume training, modify the following value in your configuration file (in this case, I'm using the
`ssd_mobilenet_v2_fpnlite_320x320_coco17_tpu-8` model)

| Line | Property                            | To                                                                                                                                                         |
|------|-------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 142  | `train_config.fine_tune_checkpoint` | Path to the model's latest checkpoint (e.g. `ssd_mobilenet_v2_fpnlite_320x320_coco17_tpu-8/checkpoint/ckpt-1`). remove `.index`, use forward slashes (`/`) |

### Export the model

To export the inference graph, run the following command:

```bash
python exporter_main_v2.py --trained_checkpoint_dir=training  --pipeline_config_path=ssd_mobilenet_v2_fpnlite_320x320_coco17_tpu-8.config --output_directory inference_graph
```

- `--trained_checkpoint_dir` is the path to the folder where the model and checkpoints are saved.
- `--pipeline_config_path` is the path to the model's config file (e.g. `ssd_mobilenet_v2_fpnlite_320x320_coco17_tpu-8.config`)
- `--output_directory` is the path to the folder where the inference graph will be saved.

### Test the model

- Change the `-m` parameter with the name of the model you downloaded if you chose a different model.

### Predict on images

Create a folder called `output` in the `models/research/object_detection` folder.
Copy the `predict_image.py` file to the `models/research/object_detection` folder and run the following command:

- `-i` will predict on all the images in the folder. If you don't use it, you will have to specify the image path with the `-p` parameter.

```bash
cd models/research/object_detection
python .\predict_image.py -m inference_graph\saved_model -l label_map.pbtxt -i .\images\test
```

The output should be in the `models/research/object_detection/output` folder (make sure you created the `output` folder).

### Predict on webcam

Copy the `predict_webcam.py` file to the `models/research/object_detection` folder and run the following command:

```bash
cd models/research/object_detection
python .\predict_webcam.py -m inference_graph\saved_model -l label_map.pbtxt
```

### Predict on a video

Copy the `predict_video.py` file to the `models/research/object_detection` folder and run the following command:
Replace `video.mp4` with the name of the video you want to use.
Move your video to the `models/research/object_detection` folder.

```bash
cd models/research/object_detection
python .\predict_video.py -m inference_graph\saved_model -l label_map.pbtxt -v .\video.mp4
```

Congrats, you're done 🎉!
