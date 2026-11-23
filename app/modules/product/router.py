from app.database.dependencies import get_db
from fastapi import (
APIRouter,
Depends,
status
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

def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    service = ProductService(db)
    return service.create_product(product)
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