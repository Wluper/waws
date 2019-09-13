# coding=utf-8


##########################
# Import
##########################
import os
import subprocess
import boto3
import time

# local imports
from . import utils


##########################
# Code
##########################
class InstanceManager(object):
    """ Main EC2 Instance Manager. """
    _instance_mapping = {
        'flower-power-1' : 'sunshine-1',
        'flower-power-2' : 'sunshine-2',
    }

    def __init__(self):
        self.config_dict = utils.get_config()

        if not self.config_dict:
            raise Exception("Could not load the configuration file.\nPlease configure: 'waws --configure'. If there are other issues please report on Github.")

        self.__session = boto3.Session(
            aws_access_key_id=self.config_dict["AWS_KEY_ID"],
            aws_secret_access_key=self.config_dict["AWS_KEY"],
        )
        self.__ec2 = self.__session.resource(
            "ec2",
            region_name=self.config_dict["AWS_REGION"]
        )

    def upload_to_EC2( self, folder_file_name,  local_path="", optional_remote_path="", instance='flower-power-1' ):
        """ Uploads a file or folder from local_path to home(~) or optional_remote_path on instance. """
        # setting up authentication
        self._set_key_and_user()
        instance = self.get_instance_name(instance)
        instance_host = self.get_dns(instance)

        #local full path
        file = os.path.join( local_path, folder_file_name )

        #uploading the files
        self.scp(mode='put', remote_host=instance_host, remote_file=optional_remote_path, local_file=file )

    def download_from_EC2( self, folder_file_name, local_path=None, optional_remote_path="", instance='flower-power-1' ):
        """
        Downloads a file or folder from optional_remote_path on instance to local_path on local machine
        """
        if not local_path:
            local_path = os.getcwd()

        # setting up authentication
        self._set_key_and_user()
        instance = self.get_instance_name(instance)
        instance_host = self.get_dns(instance)

        #remote full path
        target_folder_file = folder_file_name
        if optional_remote_path:
            if optional_remote_path.endswith('/'):
                target_folder_file = optional_remote_path + target_folder_file
            else:
                target_folder_file = optional_remote_path + '/' + target_folder_file

        #getting the files
        self.scp(mode='get', remote_host=instance_host, remote_file=target_folder_file, local_file=local_path )

    def connect_to_EC2( self, instance='flower-power-1' ):
        """
        connects to instances
        """
        self._set_key_and_user()
        instance = self.get_instance_name(instance)
        self.start_instance(instance)
        instance_dns = self.get_dns(instance)

        command =  'ssh -i "' + os.path.expanduser(self.KEY_PATH) + '" ' + self.USER + '@' + instance_dns
        print(command)

        subprocess.run(command,shell=True)
        print('Exited Instance: Awesome')

    def scp(self,remote_file,remote_host,local_file='',mode='put'):
        """
        invoces rsync command in command line.

        The way it works is that, the destination parameters (i.e. either remote or local) is the folder in which to copy. One depth of folders is ok to not exists rsync will create. More will fail. But also that's the reason for creating things like: dir_for_upload/dir_for_upload -> therefore the destination should only contain the path to where the rest should live.

        if questions read the man page of rsync
        """
        self._set_key_and_user()

        if mode=='put':
            command = 'rsync -e "ssh -i '+self.KEY_PATH+'" -avz "'+local_file+'" "'+self.USER+'@'+remote_host+':'+remote_file+'"'
            print(command)
            subprocess.run(command,shell=True)

        else:
            command = 'rsync -e "ssh -i '+self.KEY_PATH+'" -avz "'+self.USER+'@'+remote_host+':'+remote_file+'" "'+local_file+'"'
            print(command)
            subprocess.run(command,shell=True)

    def get_instance_name(self,maybe_instance_name):
        """ Retrieves instance name. """
        temp = self._instance_mapping.get(maybe_instance_name)
        if temp:
            instance_name = temp
        else:
            instance_name = maybe_instance_name
        return instance_name

    def get_dns(self,instance_name):
        """ Gets the dns of a running instance. """
        instances = self.get_instances()
        for instance in instances:
            if instance['name']==instance_name:
                return instance['dns']
        return False

    def get_instances(self):
        """
        Gets all available instances.

        Input: None
        Output:
            instanceList[
                internalDict = {
                    'id'    : type(string),
                    'name'  : type(string),
                    'dns'   : type(string),
                    'state' : type(string), #running, stopped
                    }
                ]
        """
        out_list  = []
        temp_dict = {
            'name'  : '',
            'dns'   : '',
            'state' : ''
        }

        for instance in self.__ec2.instances.all():
            # filling up dict
            temp_dict['id']    = instance.id
            temp_dict['name']  = self.get_tag(instance.tags,'Name')
            temp_dict['dns']   = instance.public_dns_name
            temp_dict['state'] = instance.state['Name']
            out_dict = temp_dict.copy()
            # appending to list
            out_list.append(out_dict)

        return out_list

    def get_tag(self,tags,key):
        """ Get's the correct Tag Value from the instance.tag dict. """
        for pair in tags:
            if pair['Key']==key:
                return pair['Value']
        return None

    def _set_key_and_user(self):
        """ Sets the users key and name from config dict. """
        self.KEY_PATH  = self.config_dict['KEY_PATH']
        self.USER      = self.config_dict['USER']

    def start_instance(self,name='flower-power-1'):
        """ Activates given instance. Returns True or False. """
        name = self.get_instance_name(name)
        instances = self.get_instances()

        for instance in instances:
            if instance['name']==name:
                temp = self.__ec2.Instance(instance['id'])

                # if not running
                if temp.state['Name']=='running':
                    return instance['dns']

                # if not running
                temp.start()
                idx = 0
                while temp.state['Name'] != 'running':
                    print ('...instance is %s' % temp.state['Name'] )
                    time.sleep(10)
                    idx += 1
                    temp.reload()
                    if idx == 10:
                        temp.stop()
                        return False
                # instance started exiting
                print ('...instance is finally:%s' % temp.state['Name'] )
                return self.get_dns(name)

        return False

    def stop_instance(self,name='flower-power-1'):
        """ Shuts down given instance. Returns True or False. """
        name = self.get_instance_name(name)
        instances = self.get_instances()

        for instance in instances:
            if instance['name']==name:
                temp = self.__ec2.Instance(instance['id'])
                temp.stop()
                # for the instance to stop
                while temp.state['Name'] != 'stopped':
                    time.sleep(10)
                    print('...instance is %s' % temp.state['Name'])
                    temp.reload()
                # instance stopped exiting
                print ('...instance is finally: %s' % temp.state['Name'] )
                return True

        return False
