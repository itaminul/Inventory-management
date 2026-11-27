
from datetime import datetime

from sqlalchemy.util import await_

from app.core.uploader import upload_single_image
from app.database.dependencies import get_db
from fastapi import (
    APIRouter,
    Depends,
    status,
    File,
    UploadFile,
    Form
)
from sqlalchemy.orm import Session

from app.modules.product import service
from app.modules.product.models import Product
from app.modules.product.schemas import ProductResponse, ProductCreate, UpdateProduct
from app.modules.product.service import ProductService

router = APIRouter()

@router.get("/", response_model=list[ProductResponse])
def get_all_products(db: Session = Depends(get_db)):
    service = ProductService(db)
    products = service.get_all_products()
    return products
@router.post("/", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)

async def create_product(
    product_name: str = Form(...),
    manufacturer_date: datetime = Form(...),
    product_code: str | None = Form(None),
    product_price: float | None = Form(None),
    product_description: str | None = Form(None),
    product_image: UploadFile | None = File(None),
    customer_id: int = None,
    db: Session = Depends(get_db),
):
    uploaded_image = None
    if product_image and product_image.filename:
        uploaded_image = await upload_single_image(
            file= product_image,
            subfolder="products",
            max_size_mb=5
        )

    product_data = ProductCreate(
        product_code=product_code,
        product_price= product_price,
        product_name=product_name,
        product_description=product_description,
        manufacturer_date=manufacturer_date,
        product_image=uploaded_image,
        customer_id= customer_id,

    )

    service = ProductService(db)
    return service.create_product(product_data)
@router.patch("/{id}", response_model=ProductResponse)
def update_product(id: int, product: UpdateProduct, db: Session = Depends(get_db)):
    service =  ProductService(db)
    update_product = service.update_product(id, product)
    return update_product
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(id: int, db: Session = Depends(get_db)):
    service = ProductService(db)
    delete_product = service.delete_product(id)
    return delete_product