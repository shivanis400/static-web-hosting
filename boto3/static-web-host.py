import logging
import boto3
from botocore.exceptions import ClientError
import json
import os
logging.getLogger().setLevel(logging.INFO)
import mimetypes 

bucket_name = 'edcast-static-webhost'
region = "us-east-2" 


def create_bucket(bucket_name, region=None):
    """
    
    Create an S3 bucket in a specified region if region is not passed, default region 
    N.Virginia will be used
   
    :param bucket_name: Bucket name to be created
    :param region: String region to create bucket in
    :return True: If bucket is Created and False: If Bucket is not created
    """

    try:
        logging.info(f"Creating Bucket {bucket_name}.")
        if region is None:
            s3_client = boto3.client('s3')
            s3_client.create_bucket(Bucket=bucket_name)
        else:
            s3_client = boto3.client('s3', region_name=region)
            location = {'LocationConstraint': region}
            s3_client.create_bucket(Bucket=bucket_name, CreateBucketConfiguration=location)
        logging.info(f"Bucket {bucket_name} Created successfully.")
        
        
    except ClientError as e:
        logging.error(f"Error while creating bucket {bucket_name}, Failed with Error Message {e}.")
        return False
        
    return True   
        
    
def add_bucket_policy(bucket_name):
    """
    
    Setting up the bucket policy, if bucket is created successfully.
    
    :param bucket_name : Name of the bucket to apply policies
    """ 
    
    logging.info(f"Creating Policy Document for bucket {bucket_name}.")
    bucket_policy = {
        'Version': '2012-10-17',
        'Statement': 
                    [{
                'Effect': 'Allow',
                "Sid":"PublicReadObjects",
                'Principal': '*',
                'Action': ['s3:GetObject'],
                'Resource': f'arn:aws:s3:::{bucket_name}/*'
                     }]
                }
                
    # Convert the bucket_policy from JSON dictionary to string format
    bucket_policy = json.dumps(bucket_policy)

    # Set the new policy to the specified bucket, so that it can be 
    # accesbile over the internet
    try:
        s3 = boto3.client('s3')
        s3.put_bucket_policy(Bucket=bucket_name, Policy=bucket_policy)
        logging.info(f"Successfully applied policy to the specified bucket.")
        
    except Exception as e:
        logging.error(f"Failed tp apply policy to the specified bucket, Error Message :- {e}.")
        
        
def set_static_config(bucket_name):
    """
    
    Setting This bucket to be used as static web hosting.
    
    :param bucket_name name of the bucket 
    """

    logging.info("Setting up Website Configuration for s3 bucket.")
    
    website_configuration = {
    'IndexDocument': {'Suffix': 'index.html'}
                            }

    # Set the website configuration
    s3 = boto3.client('s3')
    s3.put_bucket_website(Bucket=bucket_name, WebsiteConfiguration=website_configuration)
                          
    logging.info("Successfully Applied website configuration.")
    
    
def upload_objects(local_directory):
    """
    
    Upload the content to our s3 bucket, to be used by our Website.
    
    :param file content path of our local_directory  
    """

    try:
        
        logging.info(f"Starting Content Upload to the bucket {bucket_name}.")
        root_path = local_directory 
        s3_resource = boto3.resource("s3", region_name=region)
        my_bucket = s3_resource.Bucket(bucket_name)

        for path, subdirs, files in os.walk(root_path):
            path = path.replace("\\","/")
            for file in files: 
                local_path = os.path.join(path, file)
                mimetype, _ = mimetypes.guess_type(local_path)
                relative_path = os.path.relpath(local_path, local_directory).replace("\\","/")
                logging.info(f"Uploading {file} in s3://{relative_path}")
                
                if '/' in relative_path:
                    my_bucket.upload_file(local_path, os.path.dirname(relative_path)+'/'+file,
                                        ExtraArgs={"ContentType": mimetype,'ACL': 'public-read'})
                else:
                    my_bucket.upload_file(local_path,file,ExtraArgs={"ContentType": mimetype,'ACL': 'public-read'})
                logging.info(f"Successfully Uploaded the file  s3://{relative_path}.")
                
    except Exception as e:
        logging.error(f"Error While uploading the website content, Error Message {e}.")
        

def website_url(bucket_name):
    """
    
    Post the website URL will be used for Static web hosting.
    
    :param bucket_name used for static web hosting 
    """ 
    website_url = f"http://{bucket_name}.s3-website.{region}.amazonaws.com" 
    logging.info(f"\n\n\nPlease Use this URL to access the website :- {website_url}\n\n.")
    
    
    
if __name__ == '__main__':
    """
    
    TODO: 27/07/2020
    Version : 2
    
    1:- Create An S3 Bucket.
    2:- Add Bucket Policies.
    3:- Set up the Website Configuration.
    4:- Upload the Website Content.
    5:- Output the Static website URL.    
    """
    logging.info("Started Main Function Excecution")
    
    status = create_bucket(bucket_name,region)
    
    if(status == True):
        content_path ="F:\\website" 
        add_bucket_policy(bucket_name)
        set_static_config(bucket_name)
        upload_objects(content_path)
        website_url(bucket_name)
    else:
        logging.info(f"Failed to Create The bucket {bucket_name}, Exiting the execution")
        exit(0)
      
        
