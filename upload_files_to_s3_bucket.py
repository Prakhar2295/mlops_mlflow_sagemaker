import os
import boto3
from from_root import from_root


s3_resource = boto3.resource("s3", region_name="us-east-1")

def upload_objects():
    try:
        bucket_name = "mlops-s3-001"               #s3 bucket name
        root_path =    os.path.join(from_root(),"D:/FSDS/MAchine_Learning/mlflow_aws_sagemaker/artifacts")

        my_bucket = s3_resource.Bucket(bucket_name)

        for path, subdirs, files in os.walk(root_path):
            path = path.replace("\\","/")
            directory_name = path.replace(root_path,"")
            for file in files:
                my_bucket.upload_file(os.path.join(path, file), directory_name+'/'+file)
        print("done")        

    except Exception as err:
        print(err)

if __name__ == '__main__':
    upload_objects()