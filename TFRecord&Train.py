import os
import subprocess
import wget

CUSTOM_MODEL_NAME = 'S.LANG'
PRETRAINED_MODEL_NAME = 'ssd_mobilenet_v2_fpnlite_320x320_coco17_tpu-8'
PRETRAINED_MODEL_URL = 'http://download.tensorflow.org/models/object_detection/tf2/20200711/ssd_mobilenet_v2_fpnlite_320x320_coco17_tpu-8.tar.gz'
TF_RECORD_SCRIPT_NAME = 'generate_tfrecord.py'
LABEL_MAP_NAME = 'label_map.pbtxt'

path_for_paths = 'C:/Users/luigi/sign_lang_ai/paths'
paths = {
    'WORKSPACE_PATH': os.path.join(path_for_paths, 'Tensorflow', 'workspace'),
    'SCRIPTS_PATH': os.path.join(path_for_paths, 'Tensorflow','scripts'),
    'APIMODEL_PATH': os.path.join(path_for_paths,'Tensorflow','models'),
    'ANNOTATION_PATH': os.path.join(path_for_paths,'Tensorflow', 'workspace','annotations'),
    'IMAGE_PATH': os.path.join(path_for_paths,'Tensorflow', 'workspace','images'),
    'MODEL_PATH': os.path.join(path_for_paths,'Tensorflow', 'workspace','models'),
    'PRETRAINED_MODEL_PATH': os.path.join(path_for_paths,'Tensorflow', 'workspace','pre-trained-models'),
    'CHECKPOINT_PATH': os.path.join(path_for_paths,'Tensorflow', 'workspace','models',CUSTOM_MODEL_NAME), 
    'OUTPUT_PATH': os.path.join(path_for_paths,'Tensorflow', 'workspace','models',CUSTOM_MODEL_NAME, 'export'), 
    'TFJS_PATH':os.path.join(path_for_paths,'Tensorflow', 'workspace','models',CUSTOM_MODEL_NAME, 'tfjsexport'), 
    'TFLITE_PATH':os.path.join(path_for_paths,'Tensorflow', 'workspace','models',CUSTOM_MODEL_NAME, 'tfliteexport'), 
    'PROTOC_PATH':os.path.join(path_for_paths,'Tensorflow','protoc')
 }


files = {
    'PIPELINE_CONFIG':os.path.join(path_for_paths,'Tensorflow', 'workspace','models', CUSTOM_MODEL_NAME, 'pipeline.config'),
    'TF_RECORD_SCRIPT': os.path.join(path_for_paths,paths['SCRIPTS_PATH'], TF_RECORD_SCRIPT_NAME), 
    'LABELMAP': os.path.join(path_for_paths,paths['ANNOTATION_PATH'], LABEL_MAP_NAME)
}


for path in paths.values():
    if not os.path.exists(path):
        if os.name == 'nt':
            os.makedirs(path)


if not os.path.exists(os.path.join(paths['APIMODEL_PATH'], 'research', 'object_detection')):
    subprocess.run(['git', 'clone', 'https://github.com/tensorflow/models', paths['APIMODEL_PATH']], shell=True, check=True)

if os.name=='nt':
    url="https://github.com/protocolbuffers/protobuf/releases/download/v3.15.6/protoc-3.15.6-win64.zip"
    wget.download(url)
    subprocess.run(f'move protoc-3.15.6-win64.zip {paths["PROTOC_PATH"]}', shell=True, check=True)
    subprocess.run(['tar', '-xf', f"{paths['PROTOC_PATH']}/protoc-3.15.6-win64.zip"],check=True, cwd=paths['PROTOC_PATH'])
    os.environ['PATH'] += os.pathsep + os.path.abspath(os.path.join(paths['PROTOC_PATH'], 'bin'))   
    subprocess.run('cd Tensorflow/models/research && protoc object_detection/protos/*.proto --python_out=. && copy object_detection\\packages\\tf2\\setup.py setup.py && python setup.py build && python setup.py install', shell=True, check=True)
    subprocess.run('cd Tensorflow/models/research/slim && pip install -e .',shell=True, check=True, executable="/bin/bash")
