from IPython import get_ipython
_ip = get_ipython()
import glob
import os
<<<<<<< HEAD
import json
import glob
from tqdm import tqdm
from os import path, mkdir
import pytz
=======
from os import path
>>>>>>> 4d4a6cc710fa580f928c98ca3ab63cd07eb5c63a

ndp_loaded = False

def in_sub_folder(path):
    path = path.split('/')
    for folder in ['inputs', 'models', 'outputs', 'utils', 'tests']:
        if folder in path:
            return True
    return False

def get_root(path):
    if in_sub_folder(path) is False:
        return path
    else:
        return get_root('/'.join(path.split('/')[:-1]))
<<<<<<< HEAD

# Root path
ROOT_PATH = get_root(os.getcwd())

# Setup project folders   
INPUTS_PATH = path.join(ROOT_PATH, 'inputs')
MODELS_PATH = path.join(ROOT_PATH, 'models')
OUTPUTS_PATH = path.join(ROOT_PATH, 'outputs')
TESTS_PATH = path.join(ROOT_PATH, "tests")
=======
    
ROOT_PATH = get_root(os.getcwd())
>>>>>>> 4d4a6cc710fa580f928c98ca3ab63cd07eb5c63a
UTILS_PATH = path.join(ROOT_PATH, "utils")

# Params
PARAMS_NAME = 'params.json'
PARAMS_PATH = path.join(INPUTS_PATH, PARAMS_NAME)

# Get params
if path.exists(PARAMS_PATH):
    with open(PARAMS_PATH) as f:
        PARAMS = json.load(f)

# Save parameters
def save_parameters(data):
    with open(PARAMS_PATH, 'w') as f:
        json.dump(data, f, indent=4)
        print(f"✅ Parameters saved successfully.")
        
# Publish all to production     
def publish_all():
    files = f"{ROOT_PATH}/**/*"

    for file in tqdm(glob.glob(files)):
        if path.isfile(file):
            naas.dependency.add(file, print_result=False)
    print("✅ Project published to production successfully.")
    
# Create dir
def create_dir(dir_path):
    if not path.exists(dir_path):
        mkdir(dir_path)


utils_files = sorted(glob.glob(f"{UTILS_PATH}/*.ipynb"))
for file in utils_files:
    if not file.endswith("__utils__.ipynb"):
        _ip.run_line_magic('run', file)

