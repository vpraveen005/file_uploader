import pytest
from file_uploader.uploader import FileUploader
from file_uploader.config import Config

@pytest.fixture
def config():
    return Config()

@pytest.fixture
def uploader(config):
    return FileUploader(config)

def test_upload_to_s3(uploader, mocker):
    mocker.patch.object(uploader.s3_client, 'upload_file', return_value=None)
    uploader.upload_to_s3('test.jpg', 'test_bucket')
    uploader.s3_client.upload_file.assert_called_once_with('test.jpg', 'test_bucket', 'test.jpg')

def test_upload_to_gcs(uploader, mocker):
    mocker.patch.object(uploader.gcs_client.bucket('test_bucket').blob('test.doc'), 'upload_from_filename', return_value=None)
    uploader.upload_to_gcs('test.doc', 'test_bucket')
    uploader.gcs_client.bucket('test_bucket').blob('test.doc').upload_from_filename.assert_called_once_with('test.doc')
