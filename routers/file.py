from botocore.exceptions import ClientError
from fastapi import File, UploadFile, APIRouter
from db.session import client_s3, s3_bucket_name

router = APIRouter()


@router.post("/files/")
async def create_file(file: bytes = File()):
    return {"file_size": len(file)}


@router.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    location = os.getcwd() + '/upload/' + file.filename
    try:
        client_s3.upload_file(
            location, s3_bucket_name, file.filename
        )
    except ClientError as e:
        print(f'Credential error => {e}')
    except Exception as e:
        print(f"Another error => {e}")
