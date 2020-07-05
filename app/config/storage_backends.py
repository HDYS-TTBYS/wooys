from storages.backends.s3boto3 import S3Boto3Storage

# 画像は同ファイル名での上書きを許さない


class StaticStorage(S3Boto3Storage):
    location = "static"
    file_overwrite = False

    def _normalize_name(self, name):
        name = self.location + "/" + name
        name = name.replace("static//", "static/")
        return name


class MediaStorage(S3Boto3Storage):
    location = "media"
    file_overwrite = False

    def _normalize_name(self, name):
        name = self.location + "/" + name
        name = name.replace("static//", "static/")
        return name
