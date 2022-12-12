from IPython import get_ipython
_ip = get_ipython()
import glob
import os
import json
import glob
from tqdm import tqdm
from os import path, mkdir
import pytz
import re
import naas

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
    

# Root path
ROOT_PATH = get_root(os.getcwd())

# Setup project folders   
INPUTS_PATH = path.join(ROOT_PATH, 'inputs')
MODELS_PATH = path.join(ROOT_PATH, 'models')
OUTPUTS_PATH = path.join(ROOT_PATH, 'outputs')
TESTS_PATH = path.join(ROOT_PATH, "tests")
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
        
# Schedule pipeline    
def schedule_pipeline(pipeline_path=None, cron=None, files=[]):
    """
    By default, all files in inputs, models, utils will be sent to production.
    """
    if len(files) == 0:
        inputs_files = glob.glob(f"{INPUTS_PATH}/*", recursive=True)
        models_files = glob.glob(f"{MODELS_PATH}/**/*", recursive=True)
        pipeline_files = glob.glob(f"{MODELS_PATH}/pipeline_executions/**/*", recursive=True)
        utils_files = glob.glob(f"{UTILS_PATH}/*", recursive=True)
        files = inputs_files + models_files + utils_files

    for file in tqdm(files):
        if path.isfile(file) and file not in pipeline_files:
            naas.dependency.add(file, print_result=False)
    print("✅ Project published to production successfully.")
    
    if not pipeline_path:
        pipeline_path = path.join(MODELS_PATH, "__pipeline__.ipynb")
    if cron:
        naas.scheduler.add(path=pipeline_path, cron="*/30 8-20 * * 1-5")
    
# Create dir
def create_dir(dir_path):
    if not path.exists(dir_path):
        mkdir(dir_path)
        
def create_dir_from_path(dir_path):
    if not path.exists(dir_path):
        mkdir(dir_path)
        print(f"✅ Directory successfully created '{dir_path}'.")
        
def create_dir_from_path(dir_path):
    dirs_check = []
    directories = dir_path.split("/")
    for directory in directories:
        dirs_check.append(directory)
        dir_check = "/".join(dirs_check)
        if len(dir_check) > 0 and not path.exists(dir_check) and not "." in directory:
            create_dir(dir_check)


utils_files = sorted(glob.glob(f"{UTILS_PATH}/*.ipynb"))
for file in utils_files:
    if not re.match(".+[0-9]{20}.+.ipynb", file) and not file.endswith("__utils__.ipynb"):
        _ip.run_line_magic('run', file)
        print(f"✅ utils file '{file}' successfully loaded.")

