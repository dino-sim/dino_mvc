from fastapi import File, UploadFile, APIRouter

router = APIRouter()


@router.post("/files/")
async def create_file(file: bytes = File()):
    return {"file_size": len(file)}


@router.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    return {"filename": file.filename,
            "content_type": file.content_type}
