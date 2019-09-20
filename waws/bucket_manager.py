# coding=utf-8


##########################
# Import
##########################
import os
import subprocess
import boto3

# local imports
from . import utils


##########################
# Constants
##########################
DEFAULT_BUCKET = "wluper-retrograph"


##########################
# Code
##########################
class BucketManager(object):
    """ Main S3 Bucket Manager. """


    def __init__(self):
        self.config_dict = utils.get_config()

        if not self.config_dict:
            raise Exception("Could not load the configuration file.\nPlease configure: 'waws --configure'. If there are other issues please report on Github.")

        self.__session = boto3.Session(
            aws_access_key_id=self.config_dict["AWS_KEY_ID"],
            aws_secret_access_key=self.config_dict["AWS_KEY"],
        )
        self.__s3  = self.__session.resource(
            "s3",
            region_name=self.config_dict["AWS_REGION"]
        )

    def upload_file(
        self,
        file_name,
        local_path,
        remote_path,
        bucket_name=DEFAULT_BUCKET
        ):
        """ Uploads object to S3. """
        bucket = self.__s3.Bucket(bucket_name)
        final_local_path = os.path.join(local_path,file_name)
        final_remote_path = remote_path + '/' + file_name

        if final_remote_path.startswith('/'):
            final_remote_path = final_remote_path.replace('/','',1)

        bucket.upload_file( final_local_path, final_remote_path )
        print( "Uploaded: {}".format(file_name) )

    def download_file(
        self,
        file_name,
        local_path,
        remote_path,
        bucket_name=DEFAULT_BUCKET
        ):
        """ Downloads object from S3. """
        bucket = self.__s3.Bucket(bucket_name)
        final_local_path = os.path.join(local_path,file_name)
        final_remote_path = remote_path + '/' + file_name

        if final_remote_path.startswith('/'):
            final_remote_path = final_remote_path.replace('/','',1)

        bucket.download_file( final_remote_path, final_local_path )
        print( "Downloaded: {}".format(file_name) )

    def list_files(
        self,
        bucket_name=DEFAULT_BUCKET
        ):
        """ Downloads object from S3. """
        bucket = self.__s3.Bucket(bucket_name)
        objects = bucket.objects.filter(Prefix="")
        for obj in objects:
            print( "Path: {}".format(obj.key) )

# EOF
