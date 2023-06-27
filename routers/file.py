from botocore.exceptions import ClientError
from fastapi import UploadFile, APIRouter, HTTPException, Path
from starlette import status

from db.session import client_s3, s3_bucket_name
import os
import time

from models.fileinfo import FileInfos
from routers.deps import db_dependency, user_dependency
from util.genrateUploadFilename import generate_filename_for_s3
from util.errors import no_user, error_msg

router = APIRouter()


@router.get("/download/{file_id}", status_code=status.HTTP_200_OK)
def download(user: user_dependency, db: db_dependency, file_id: int = Path(gt=0)):
    no_user(user)
    file_model = db.query(FileInfos).filter(FileInfos.id == file_id).first()

    if file_model is not None:
        res = file_model.src
        return res

    raise HTTPException(status_code=404, detail=error_msg('file_id'))


@router.post("/uploadfile/", status_code=status.HTTP_200_OK)
async def create_upload_file(file: UploadFile, user: user_dependency, db: db_dependency):
    location = os.getcwd() + '/upload/' + file.filename
    no_user(user)
    filename = generate_filename_for_s3(file.filename)
    try:
        client_s3.upload_file(
            location, s3_bucket_name, filename
        )
        # download 정책 추가 -> s3 자체에서 가능
        title = filename
        size = file.size
        src = f"https://{s3_bucket_name}.s3.ap-northeast-2.amazonaws.com/{filename}"
        created_at = time.strftime('%Y-%m-%d %H:%M:%S')

        fileinfo_model = FileInfos(title=title, size=size, src=src, created_at=created_at, owner_id=user.get('id'))
        db.add(fileinfo_model)
        db.commit()
    except ClientError as e:
        print(f'Credential error => {e}')
    except Exception as e:
        print(f"Another error => {e}")


@router.post("/delete/{file_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_file(user: user_dependency, db: db_dependency, file_id: int = Path(gt=0)):
    no_user(user)
    try:

        file_info = db.query(FileInfos).filter(FileInfos.id == file_id).filter(FileInfos.owner_id == user.get('id')).first()
        if file_info is None:
            raise HTTPException(status_code=404, detail=error_msg('file'))

        client_s3.delete_object(Bucket=s3_bucket_name, Key=file_info.title)
        db.query(FileInfos).filter(FileInfos.id == file_id).delete()
        db.commit()
    except ClientError as e:
        print(f'Credential error => {e}')
    except Exception as e:
        print(f"Another error => {e}")

