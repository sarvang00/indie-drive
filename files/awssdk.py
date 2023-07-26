import boto3

class S3ClientObject:
    def __init__(self):
        # Dev
        # self.s3_client = boto3.client('s3', aws_access_key_id='#', aws_secret_access_key='#', aws_session_token="#")
        # Deploy
        self.s3_client = boto3.client('s3')
        self.defaultBucketName = "myawsbucketdalhousietest1"

    def upload_file_to_s3(self, file_path, s3_key, bucket_name=None, public_access=True):
        bucket_name = bucket_name or self.defaultBucketName
        extra_args = {}
        if public_access:
            extra_args['ACL'] = 'public-read'

        try:
            self.s3_client.upload_file(file_path, bucket_name, s3_key, ExtraArgs=extra_args)
            print(f"File uploaded successfully to S3 with public access: {s3_key}")

            object_url = f"https://{bucket_name}.s3.{self.s3_client.meta.region_name}.amazonaws.com/{s3_key}"
            print(object_url)
            return object_url
        except Exception as e:
            print(f"Error uploading file to S3: {e}")
            return False

    def set_public_access_to_false(self, s3_key, bucket_name=None):
        bucket_name = bucket_name or self.defaultBucketName
        try:
            # Remove the public-read permission from the object's ACL
            response = self.s3_client.put_object_acl(
                Bucket=bucket_name,
                Key=s3_key,
                ACL='private'  # Set ACL to private to remove public-read permission
            )

            print(f"Public access of object '{s3_key}' in bucket '{bucket_name}' set to False.")
            return True
        except Exception as e:
            print(f"Error setting public access to False: {e}")
            return False

    def set_public_access_to_true(self, s3_key, bucket_name=None):
        bucket_name = bucket_name or self.defaultBucketName
        try:
            # Set the public-read permission for the object's ACL
            response = self.s3_client.put_object_acl(
                Bucket=bucket_name,
                Key=s3_key,
                ACL='public-read'
            )

            print(f"Public access of object '{s3_key}' in bucket '{bucket_name}' set to True.")
            return True
        except Exception as e:
            print(f"Error setting public access to True: {e}")
            return False
        
    def delete_file_from_s3(self, s3_key, bucket_name=None):
        bucket_name = bucket_name or self.defaultBucketName
        try:
            # Delete the object from the S3 bucket
            response = self.s3_client.delete_object(
                Bucket=bucket_name,
                Key=s3_key
            )

            print(f"File '{s3_key}' deleted from bucket '{bucket_name}'.")
            return True
        except Exception as e:
            print(f"Error deleting file from S3: {e}")
            return False
