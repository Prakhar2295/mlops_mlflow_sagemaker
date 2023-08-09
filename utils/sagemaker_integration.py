import subprocess
import os
from from_root import from_root
import boto3
import mlflow.sagemaker as mfs
import json

class sagemaker_integration:
    def __init__(self, config):
        self.config = config


    def upload(s3_bucket_name = None, mlruns_direc = None):
        try:
            output = subprocess.run(["aws","s3","sync","{}".format(mlruns_direc),"s3://".format(s3_bucket_name)],stdout = subprocess.PIPE,encoding = 'utf-8')
            print("\nSaved to bucket: ",s3_bucket_name)
            return f"Done Uploading: {output.stdout}"
        except Exception as e:
            raise e


    def deploy_model_aws_sagemaker(self):
            try:
                app_name=self.config['params']['app_name']
                execution_role_arn=self.config['params']['execution_role_arn']
                image_ecr_url=self.config['params']['image_ecr_url']
                region_name=self.config['params']['region']
                s3_bucket_name = self.config['params']['s3_bucket_name']
                experiment_id = self.config['params']['experiment_id']
                run_id =  self.config['params']['run_id']
                model_name= self.config['params']['model_name']
                
                model_uri = "s3://{}//{}/{}/artifacts/{}/".format(s3_bucket_name,experiment_id,run_id,model_name)
                print(model_uri)
                                                               
                mfs.deploy(app_name=app_name,
                        model_uri=model_uri,
                        execution_role_arn=execution_role_arn,
                        region_name=region_name,
                        image_url=image_ecr_url,
                        mode=mfs.DEPLOYMENT_MODE_CREATE)
                
                return "Deployment Successfully"
            except Exception as e:
                return f"Error Occurred while Deploying : {e.__str__()} "

    def query(self, input_json):
            try:
                client = boto3.session.Session().client("sagemaker-runtime", self.config['params']['region'])
                response = client.invoke_endpoint(
                    EndpointName=self.config['params']['app_name'],
                    Body=input_json,
                    ContentType='application/json; format=pandas-split')
                return json.loads(response['Body'].read().decode("ascii"))
            except Exception as e:
                return f"Error Occurred While Prediction : {e.__str__()}"
            
            
    def switching_models(self):
            try:
                new_model_uri = "s3://{}//{}/{}/artifacts/{}/".format(self.config['params']['s3_bucket_name'],
                                                                    self.config['params']['experiment_id'],
                                                                    self.config['params']['run_id'],
                                                                    self.config['params']['model_name'])

                mfs.deploy(app_name=self.config['params']['app_name'], model_uri=new_model_uri,
                        execution_role_arn=self.config['params']['execution_role_arn'],
                        region_name=self.config['params']['region'],
                        image_url=self.config['params']['image_ecr_url'],
                        mode=mfs.DEPLOYMENT_MODE_REPLACE)

                return f"Model Successfully switched "

            except Exception as e:
                return f"Error While Changing Model : {e.__str__()}"
            
    def remove_deployed_model(self):
            try:
                mfs.delete(app_name=self.config['params']['app_name'],
                        region_name=self.config['params']['region'])
                return f"Endpoint Successfully Deleted : {self.config['params']['app_name']}"
            except Exception as e:
                return f"Error While Deleting EndPoint : {e.__str__()}"




