import os
import subprocess

dir_path = 'C:/Users/luigi/sign_lang_ai'
Labeling_path = os.path.join(dir_path, 'labeled_imgs')

if not os.path.exists(Labeling_path):
    os.makedirs(Labeling_path)
    subprocess.run(['git', 'clone', 'https://github.com/tzutalin/labelImg', Labeling_path], check=True)

if os.name == 'nt':
    if os.path.exists(os.path.join(Labeling_path, 'resources.qrc')):
        subprocess.run(['cd', Labeling_path, '&&', 'pyrcc5', '-o', 'libs/resources.py', 'resources.qrc'], shell=True)
        subprocess.run(['cd', Labeling_path, '&&', 'python', 'labelImg.py'], shell=True)
    else:
        print('resources.qrc file not found in specified directory.')