from pydantic import BaseModel, validator, Field
from fastapi import UploadFile, Form
import shutil
import os
from core.settings.cloudinary import *
from utils.generate_random_code import RandomNumBillion


class ProductIn(BaseModel):
    product_name: str
    description: str
    quantity: int
    price: float
    image: UploadFile | str
    currency: str
    product_creator: int | None
    category_id: int

    @validator("product_name")
    def validate_name(cls, v: str):
        if len(v) > 50:
            raise ValueError("Product Name is More Than 50 letters")
        return v

    @validator("quantity")
    def validate_quantity(cls, v: int):
        if v < 0:
            raise ValueError("Qunaitity Is Less Than Zero")
        return v

    @validator("price")
    def validate_price(cls, v):
        if v < 0:
            raise ValueError("Price Less Than Zero")
        return v

    @classmethod
    async def as_form(
        cls,
        product_name: str = Form(),
        description: str = Form(),
        quantity: int = Form(1),
        price: float = Form(),
        image: UploadFile = Form(),
        currency: str = Form("JOD"),
        category_id: int = Form(),
    ):
        URL_IMAGE_FOLDER = "app/api/v1/images_products"
        image.filename = RandomNumBillion.generate()
        image_url = f"{URL_IMAGE_FOLDER}/{image.filename}.JPG"
        print(image_url)
        if os.path.isdir(URL_IMAGE_FOLDER):
            with open(image_url, "wb") as buffer:
                shutil.copyfileobj(image.file, buffer)
        else:
            print("folder not exist")
        cloudinary.uploader.upload(image_url, public_id=f"{image.filename}")
        url, options = cloudinary_url(
            f"{image_url}", width=100, height=150, crop="fill"
        )
        x_url = f"https://res.cloudinary.com/dgqc75jdf/image/upload/{image.filename}"
        print(x_url)

        return cls(
            product_name=product_name,
            description=description,
            quantity=quantity,
            price=price,
            image=x_url,
            currency=currency,
            category_id=category_id,
        )


class UpdateProductPart(BaseModel):
    description: str | None
    quantity: int | None
    price: float | None
    currency: str | None
    product_creator: int | None
    category_id: int | None

    @classmethod
    async def as_form(
        cls,
        product_name: str = Form(),
        description: str = Form(),
        quantity: int = Form(1),
        price: float = Form(),
        image: UploadFile = Form(),
        currency: str = Form("JOD"),
        category_id: int = Form(),
    ):
        URL_IMAGE_FOLDER = "app/api/v1/images_products"
        image.filename = RandomNumBillion.generate()
        image_url = f"{URL_IMAGE_FOLDER}/{image.filename}.JPG"
        print(image_url)
        if os.path.isdir(URL_IMAGE_FOLDER):
            with open(image_url, "wb") as buffer:
                shutil.copyfileobj(image.file, buffer)
        else:
            print("folder not exist")
        return cls(
            product_name=product_name,
            description=description,
            quantity=quantity,
            price=price,
            image=image_url,
            currency=currency,
            category_id=category_id,
        )
