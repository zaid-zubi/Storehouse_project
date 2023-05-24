import os
import shutil
from fastapi import HTTPException, UploadFile, status
from fastapi.encoders import jsonable_encoder
from app.api.v1.models.user import User

URL_USER_IMAGE_FOLDER = "app/api/v1/images_users"


async def upload_user_photo(username: str, file: UploadFile):
    try:
        file.filename = username
        image_url = f"{URL_USER_IMAGE_FOLDER}/{file.filename}.JPG"
        async with open(image_url, "wb") as buffer:
            await shutil.copyfileobj(file.file, buffer)
            print(file.filename)
    except:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error Occurred when upload file ",
        )
    return image_url


UPLOAD_FOLDER = "app/api/v1/images"


def upload_file(user_id: int, file: UploadFile, db):
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User Id not found"
        )

    file.filename = str(user_id)
    file_location = f"{UPLOAD_FOLDER}/{file.filename}.jpg"
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        print("---------")
    image_data = {"user_id": user_id, "path": file_location}
    image = UserImage(**image_data)
    db.add(image)
    db.commit()
    db.refresh(image)
    return jsonable_encoder(image)


def delete_file(user_id: int, db):
    file_location = f"{UPLOAD_FOLDER}/{user_id}.jpg"
    image = db.query(UserImage).filter_by(user_id=user_id).first()
    if os.path.exists(file_location):
        os.remove(file_location)
        db.delete(image)
        db.commit()
        return jsonable_encoder("Photo is deleted")
    else:
        return jsonable_encoder("Photo not found!")
