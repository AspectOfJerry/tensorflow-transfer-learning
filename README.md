# Installation

- Recommended Python version: 3.9

### Clone Tensorflow Models repository

```bash
git clone https://github.com/tensorflow/models.git
```

### Install Protobuf

<https://github.com/protocolbuffers/protobuf/releases>

Download the corresponding version of protobuf for your system and extract it to a folder (`C:\Users\<user>\AppData\Local\Programs\Python\`). Then, add the bin
folder to your PATH environment variable (`C:\Users\<user>\AppData\Local\Programs\Python\protoc-25.1-win64\bin`).

Restart your IDE/terminal and follow the next steps.

### Run protoc

Copy the `use_protobuf.py` file to the `models/research` folder and run the following command:

```bash
cd models/research  (if not already in the folder)
python use_protobuf.py object_detection/protos protoc
```

### Copying files

Copy the `setup.py` file from `models/research/object_detection/packages/tf2` to `models/research/` and run the following command:

```bash
cd models/research  (if not already in the folder)
python -m pip install .
```

Reinstall `numpy` because the included version is somehow broken:

```bash
pip install numpy==1.24.3 --force-reinstall
```

### Fix protobuf error

If you test the installation now, you will get the following error:

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

Here's a fix from [Stack Overflow](https://stackoverflow.com/questions/71759248/importerror-cannot-import-name-builder-from-google-protobuf-internal)

1. Install the latest protobuf version:

```bash
pip install --upgrade protobuf
```

2. Copy the `builder.py` file from `...\Lib\site-packages\google\protobuf\internal` to another folder (e.g. your desktop).
3. Re-install protobuf:

```bash
pip install protobuf==3.19.6 --force-reinstall
```

4. Copy the `builder.py` file back to `...\Lib\site-packages\google\protobuf\internal` and replace the existing file.

### Test the installation

```
cd models/research/object_detection/builders  (if not already in the folder)
python model_builder_tf2_test.py
```

You should get the following output:

```
[...]
----------------------------------------------------------------------
Ran 24 tests in 13.296s

OK (skipped=1)
```

And you're done 🎉!

# Setup

Create a folder called `images` in the `models/research/object_detection` folder. Then, copy the custom dataset's `test` and `train` folders into the `images`
folder.

### Convert XML to CSV

Copy the `xml_to_csv.py` file to the `models/research/object_detection` folder and run the following command:

```
cd models/research/object_detection  (if not already in the folder)
python xml_to_csv.py
```

