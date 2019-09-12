# WAWS

This is a minimal library for handling EC2 instances and uploading and downloading files to S3.

## Installation

```bash
pip3 install waws
```

### CONFIGURATION

After the installation you need to configure:

```bash
waws --configure
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

inst.upload_to_EC2(folder_file_name="CODE_FOLDER", local_path="./training", optionalRemotePath="EXPERIMENT2", instance="sunshine-1")

inst.download_from_EC2(folder_file_name="CODE_FOLDER", local_path="./training", optional_remote_path="EXPERIMENT2", instance="sunshine-1")
```

## Running as CLI

### Useful Help:
```bash
waws --help
```

### Useful functions:
```bash
# Todo with S3
waws --uploadS3 -b wluper-retrograph -f FILE -l LOCALPATH

waws --downloadS3 -b wluper-retrograph -f FILE -l LOCALPATH

#Todo with EC2
waws --start -i sunshine-1

waws --connect -i sunshine-1

waws --list

waws --docker_uploadEC2 -i sunshine-1 -f FOLDER -l LOCALPATH

waws --docker_downloadEC2 -i sunshine-1 -f FOLDER -l LOCALPATH


waws --docker_attach

waws --docker_list
```

### General parameters:
```bash
waws -i INSTANCE_NAME -f FILE_NAME  -l LOCAL_PATH  -r REMOTE_PATH  -b BUCKET_NAME
```

<!-- EOF -->
