import os
import gnupg
import boto3
from botocore.exceptions import (
    ClientError
)
import botocore

ssm = boto3.client("ssm")
session = boto3.Session( aws_access_key_id='AKIAQJZNGEWMWYXNQ3GX', aws_secret_access_key='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')
s3 = session.resource('s3')
KEY_NAME = ssm.get_parameter(Name="keyname")["Parameter"]["Value"]
EMAIL = ssm.get_parameter(Name="encryptemail")["Parameter"]["Value"]
 
def handler(event, context):
    my_bucket = s3.Bucket('merchantkey')
    lst = os.listdir("/tmp")
    print(lst) 
    my_bucket.download_file(KEY_NAME, f"/tmp/{KEY_NAME}")
    items = []

    file = my_bucket.download_file("texto.txt", "/tmp/texto.txt") 
    lst = os.listdir("/tmp")
    print(lst) 
    result = encrypt_file("/tmp/texto.txt") 
        
  
    
    return f'Gpg encrypt ok'       


def encrypt_file(file_name):
    gpg_homeshort = "/tmp"
    gpg = gnupg.GPG(gnupghome=gpg_homeshort, verbose=True)
    key = open(f"/tmp/{KEY_NAME}", "rb").read()
    gpg.import_keys(key)
    gpg.list_keys() 
    with open(file_name, "rb") as f:
        status = gpg.encrypt_file(
            f,
            recipients=[EMAIL],
            output=f"/tmp/{file_name}.gpg",
            always_trust=True,
            extra_args=["--yes"],
        )
        print(status) 
    lst = os.listdir("/tmp")
    
    return lst


 

 