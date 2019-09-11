# coding=utf-8


##########################
# Import
##########################
from setuptools import setup, find_packages

setup(
    #
    # SETUP
    #
      name          ='waws',
      version       ='0.0.0.1',
      description   ='Minimal AWS EC2/S3 wrapper by Wluper',
      url           ='https://github.com/Wluper/waws',
      author        ='Nikolai Rozanov',
      author_email  ='nikolai.rozanov@gmail.com',
      license       ='GPL 2.0',
    #
    # Actual packages, data and scripts
    #

      packages      =find_packages(),
      scripts       =[
                        'bin/waws',
                    ],
    #
    # Requirements
    #
      install_requires=[
                        'aws-cli',
                        'boto3',
                        'tqdm'
                        ]
      )
