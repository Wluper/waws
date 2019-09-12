# coding=utf-8


##########################
# Import
##########################
import json
import os
from enum import Enum

##########################
# DEFAULTS
##########################
CONFIG_TEMPLATE = {
    "KEY_PATH": os.path.expanduser("~/.ssh/wluper"),
    "USER": "Firstname",
    "AWS_REGION": "eu-west-2",
    "AWS_ENCODING": "json",
    "AWS_KEY_ID": "",
    "AWS_KEY": ""
}

HOME_DIRECTORY = os.path.expanduser("~")
CONFIG_DIRECTORY_NAME = ".waws"
CONFIG_DIRECTORY_PATH = os.path.join(HOME_DIRECTORY, CONFIG_DIRECTORY_NAME)
CONFIG_FILE_NAME = "config"
CONFIG_FILE_PATH = os.path.join(CONFIG_DIRECTORY_PATH, CONFIG_FILE_NAME)

##########################
# Code
##########################


def configure():
    """ Configures the package. """
    create_config_directory()
    configured_data = get_config()

    if not configured_data:
        configured_data = CONFIG_TEMPLATE

    for key, value in configured_data.items():
        temp_string = "Please Enter Your %s [CURRENT:%s]:  "%(key,value)
        temp_ans = input(temp_string)
        # verifying input wasn't empty
        if temp_ans:
            configured_data[key] = temp_ans

    # DUMPING TO FILE
    with open(CONFIG_FILE_PATH,'w') as file:
            json.dump(configured_data,file,indent=4, sort_keys=True)


def create_config_directory():
    """ Creates the config directory and returns true once it exists. """
    try:
        if not os.path.isdir( CONFIG_DIRECTORY_PATH ):
            os.mkdir(CONFIG_DIRECTORY_PATH)
        return True

    except Exception as e:
        return False


def get_config():
    """ Loads the config file if it exists, otherwise returns False. """
    if os.path.isfile(CONFIG_FILE_PATH):
        with open(CONFIG_FILE_PATH, "r") as file:
            file_data = json.load(file)
        return file_data

    else:
        return False
