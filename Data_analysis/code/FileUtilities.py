import os
import json
from tkinter import messagebox
from enum import Enum
from datetime import datetime

project_directory = ''
experiment = ''
mouse_pair = ''
session = ''
mouse_id = ['', '']
file_timestamp = ''
date_str = ''

def set_project_directory(path):
    global project_directory
    if os.path.exists(path) and os.path.isdir(path):
        project_directory = path
        with open("./ProjectDirectory.txt", 'w') as file:
            file.write(f'{project_directory}')
        return True
    else:
        return False


def get_project_directory():
    try:
        with open("./ProjectDirectory.txt", 'r') as file:
            path = file.read()
    except FileNotFoundError:
        path = ""
    return path


def set_experiment_directory(experiment_name):
    global experiment, project_directory

    experiment_path = project_directory + "/" + experiment_name
    if os.path.exists(experiment_path) and os.path.isdir(experiment_path):
        experiment = experiment_name
        return True
    else:
        result = messagebox.askquestion("Directory Warning", "Experiment directory does not exist. Create?", icon='warning')
        if result == "yes":
            experiment = experiment_name
            os.makedirs(experiment_path)
            return True
        else:
            return False


def _ensure_subdirectory(directory_name):
    subdirectory = project_directory + '/' + experiment + '/' + directory_name
    if os.path.exists(subdirectory) and os.path.isdir(subdirectory):
        return True
    else:
        result = messagebox.askquestion('Directory Warning', f'{directory_name} directory does not exist. Create?', icon='warning')
        if result == "yes":
            os.makedirs(subdirectory)
            return True
        else:
            return False


def set_mouse_directory(mouse):
    global experiment, mouse_pair, mouse_id, project_directory

    if mouse == 'Computer1':
        mouse_id[0] = mouse
    else:
        mouse_id[0] = f'm{mouse}'

    mouse_id[1] = ''
    mouse_pair = mouse_id[0]
    return _ensure_subdirectory(mouse_pair)


def set_mouse_pair_directory(mouse1, mouse2):
    global experiment, mouse_pair, mouse_id, project_directory

    if mouse2 == 'Computer2':
        mouse_id[1] = mouse2
    else:
        mouse_id[1] = f'm{mouse2}'

    if mouse1 == 'Computer1':
        mouse_id[0] = mouse1
        mouse_pair = f'{mouse_id[1]}_{mouse_id[0]}'
    else:
        mouse_id[0] = f'm{mouse1}'
        mouse_pair = f'{mouse_id[0]}_{mouse_id[1]}'

    return _ensure_subdirectory(mouse_pair)


def configure_mouse_directory(mouse1, mouse2=None):
    try:
        import ModuleConfiguration as config
        use_mouse_pair = getattr(config, '__USE_MOUSE_PAIR', True)
    except ImportError:
        use_mouse_pair = True

    if use_mouse_pair:
        if mouse2 is None:
            messagebox.showerror('Configuration Error', 'Mouse pair project requires two mouse ids')
            return False
        return set_mouse_pair_directory(mouse1, mouse2)
    else:
        return set_mouse_directory(mouse1)


def set_session_directory(session_type, session_num):
    global project_directory, experiment, mouse_pair, session, file_timestamp, date_str

    current_datetime = datetime.now()
    date_str = current_datetime.strftime("%Y%m%d")
    file_timestamp = current_datetime.strftime("%Y%m%d-%H%M%S")
    session = session_type + session_num
    session_directory = project_directory + '/' + experiment + '/' + mouse_pair + '/' + date_str + '_' + session

    if os.path.exists(session_directory) and os.path.isdir(session_directory):
        result = messagebox.askquestion('Directory Warning', f'{date_str}_{session} directory already exists. Add Files?',
                                        icon='warning')
        if result == "yes":
            return True
        else:
            return False
    else:
        os.makedirs(session_directory)
        os.makedirs(session_directory + "/behavior")
        os.makedirs(session_directory + "/miniscope")
        os.makedirs(session_directory + "/DAQ")
        return True


def get_file_path(mouse):
    global project_directory, experiment, mouse_pair, session, file_timestamp

    if mouse == 0:      # create a non mouse specific file name
        mouse_str = mouse_pair
    else:               # create a mouse specific file name
        mouse_str = mouse_id[mouse - 1]

    file_directory = (project_directory + '/' + experiment + '/' + mouse_pair + '/' +
                     date_str + '_' + session + '/behavior')
    return f'{file_directory}/{file_timestamp}_{experiment}_{mouse_str}_{session}'


def load_detection_regions():
    global project_directory

    filepath = project_directory + '/DetectionRegions.json'
    try:
        with open(filepath, 'r') as file:
            regions = json.load(file)
    except FileNotFoundError:
        regions = None
    return regions

def save_detection_regions(regions):
    global project_directory

    filepath = project_directory + '/DetectionRegions.json'
    with open(filepath, 'w') as file:
        json.dump(regions, file, indent=4)

