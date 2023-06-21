import os
import gnupg
import boto3
from botocore.exceptions import (
    ClientError
)
import botocore


session = boto3.Session( aws_access_key_id='AKIAQJZNGEWMWYXNQ3GX', aws_secret_access_key='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')
s3 = session.resource('s3')
KEY_NAME = "XX_AP_UPL_MERCHANT_DOCS_NPRD_.key"
def handler(event, context):
    my_bucket = s3.Bucket('merchantkey')
    lst = os.listdir("/tmp")
    print(lst)
    try:
        my_bucket.download_file(KEY_NAME, f"/tmp/{KEY_NAME}")
        items = []
    
        for my_bucket_object in my_bucket.objects.all():
            file = my_bucket_object.key
            items.append(file)
            my_bucket.download_file(f"{file}", f"/tmp/{file}") 
        
        for file in items:
            result = encrypt_file(f"/tmp/{file}") 
            print(result) 
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
            print("The object does not exist.",str(e))
        else:
            print("The object have error.",str(e))
  
    
    return f'Gpg encrypt ok'       


def encrypt_file(file_name):
    print("start lsitado temporal")
    lst = os.listdir("/tmp")
    print(lst)
    print("end listado temporal")
    gpg_homeshort = "/tmp"
    gpg = gnupg.GPG(gnupghome=gpg_homeshort, verbose=True)
    key = open(f"/tmp/{KEY_NAME}", "rb").read()
    gpg.import_keys(key)
    gpg.list_keys() 
    with open(file_name, "rb") as f:
        status = gpg.encrypt_file(
            f,
            recipients=["Luis.Salazar@Millicom.com"],
            output=f"/tmp/{file_name}.gpg",
            always_trust=True,
            extra_args=["--yes"],
        )
        print(status) 
    lst = os.listdir("/tmp")
    
    return lst


 

 