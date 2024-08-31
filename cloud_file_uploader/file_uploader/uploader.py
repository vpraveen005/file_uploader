import os
import boto3
from google.cloud import storage
from config import Config

class FileUploader:
    def __init__(self, config: Config):
        self.config = config
        self.s3_client = boto3.client('s3', aws_access_key_id=config.aws_access_key_id, aws_secret_access_key=config.aws_secret_access_key)
        self.gcs_client = storage.Client.from_service_account_json(config.gcs_service_account_json)

    def upload_to_s3(self, file_path, bucket_name):
        try:
            self.s3_client.upload_file(file_path, bucket_name, os.path.basename(file_path))
            print(f"Uploaded {file_path} to S3 bucket {bucket_name}")
        except Exception as e:
            print(f"Failed to upload {file_path} to S3: {e}")

    def upload_to_gcs(self, file_path, bucket_name):
        try:
            bucket = self.gcs_client.bucket(bucket_name)
            blob = bucket.blob(os.path.basename(file_path))
            blob.upload_from_filename(file_path)
            print(f"Uploaded {file_path} to GCS bucket {bucket_name}")
        except Exception as e:
            print(f"Failed to upload {file_path} to GCS: {e}")

    def process_files(self, directory):
        for root, _, files in os.walk(directory):
            for file in files:
                file_path = os.path.join(root, file)
                if file.split('.')[-1] in self.config.s3_file_types:
                    self.upload_to_s3(file_path, self.config.s3_bucket_name)
                elif file.split('.')[-1] in self.config.gcs_file_types:
                    self.upload_to_gcs(file_path, self.config.gcs_bucket_name)

if __name__ == "__main__":
    config = Config()
    uploader = FileUploader(config)
    uploader.process_files(config.directory)
