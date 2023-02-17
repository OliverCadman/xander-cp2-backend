import boto3
import uuid

from django.conf import settings

def generate_uuid():
    return uuid.uuid4()


class S3Client:

    def __init__(self, access_key, secret_key, region):
        self.access_key = access_key
        self.secret_key = secret_key
        self.bucket_name = settings.AWS_BUCKET_NAME

        self.region = region
    
    def create_s3_session(self):
        return boto3.Session(
            aws_access_key_id=self.access_key,
            aws_secret_access_key=self.secret_key
        )
    
    def create_s3_resource(self):
        session = self.create_s3_session()
        return session.resource('s3')
    
    def write_object(self, txt_data):
        s3 = self.create_s3_resource()
        file_id = generate_uuid()

        key = f'{file_id}.txt'

        print('BUCKET NAME:', self.bucket_name)

        res = s3.meta.client.put_object(
            Body=txt_data,
            Bucket=self.bucket_name,
            Key=key
        )

        meta_data = res.get('ResponseMetadata')
        
        status = meta_data.get('HTTPStatusCode')

        if status == 200:
            return file_id
        else:
            return None

    def read_object(self, key):
        s3 = self.create_s3_resource()
        obj = s3.meta.client.get_object(
            Bucket=self.bucket_name,
            Key=key
        )

        return obj['Body'].read().decode('utf-8')
