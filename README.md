# WAWS

This is a minimal library for handling EC2 instances and uploading and downloading files to S3.

## Installation

```bash
pip3 install waws
```

### CONFIGURATION

After the installation you need to configure:

```bash
w_aws --configure
```


## Running within Python

### S3

#### Uploading and Downloading
```python
import waws

s3 = waws.BucketManager()

# Upload files
s3.upload_file(
    file_name="test.txt",
    local_path="some/local/path",
    remote_path="SOME/S3/PATH",
    bucket_name="some_bucket_name"
)

# Download files
s3.download_file(
    file_name="test.txt",
    local_path="some/local/path",
    remote_path="SOME/S3/PATH",
    bucket_name="some_bucket_name"
)
```


### EC2

#### Uploading and Downloading
```python
import waws

inst = waws.InstanceManager()

inst.upload_to_EC2(folder_file_name="CODE_FOLDER", local_path="./training", optionalRemotePath="EXPERIMENT2", instance="flower-power-1")

inst.download_from_EC2(folder_file_name="CODE_FOLDER", local_path="./training", optional_remote_path="EXPERIMENT2", instance="flower-power-1")
```

## Running as CLI

### Useful Help:
```bash
w_aws --help
```

### Useful functions:
```bash
w_aws --start -i flower-power-1

w_aws --connect -i flower-power-1

w_aws --list

w_aws --docker_uploadEC2 -i flower-power-1 -f FOLDER -l LOCALPATH

w_aws --docker_downloadEC2 -i flower-power-1 -f FOLDER -l LOCALPATH

w_aws --docker_attach

w_aws --docker_list
```

### General parameters:
```bash
w_aws -i INSTANCE_NAME -f FILE_NAME  -l LOCAL_PATH  -r REMOTE_PATH  -b BUCKET_NAME
```

<!-- EOF -->
