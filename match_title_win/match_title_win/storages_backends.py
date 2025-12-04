# storages_backends.py
from storages.backends.s3boto3 import S3Boto3Storage

class R2PublicStorage(S3Boto3Storage):
    bucket_name = 'match-and-win'
    default_acl = 'public-read'
    querystring_auth = False
    endpoint_url='https://32432ff29e7ac0529269717c7263c317.r2.cloudflarestorage.com'


# class R2PublicStorage(S3Boto3Storage):
#     bucket_name = 'cashplus'
#     default_acl = 'public-read'
#     querystring_auth = False
#     endpoint_url='https://32432ff29e7ac0529269717c7263c317.r2.cloudflarestorage.com'