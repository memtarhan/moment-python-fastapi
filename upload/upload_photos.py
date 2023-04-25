import cloudinary
from cloudinary.uploader import upload
from fastapi import UploadFile
import api.config as config

cloudinary.config(
    cloud_name=config.CLOUDINARY_CLOUD_NAME,
    api_key=config.CLOUDINARY_API_KEY,
    api_secret=config.CLOUDINARY_API_SECRET,
    secure=True
)


async def upload_photo(folder_name: str,
                       public_id: str,
                       fileobject: UploadFile) -> str:
    file = fileobject.file._file
    response = upload(file, folder=f"photos/{folder_name}/", public_id=f"{public_id}")
    url = response['url']
    return url
