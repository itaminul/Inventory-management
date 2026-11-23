from fastapi import HTTPException
from sqlalchemy.orm import Session
from starlette import status
from app.modules.product.repository import ProductRepository
from app.modules.product.schemas import ProductCreate, UpdateProduct


class ProductService:
    def __init__(self, db: Session):
        self.repository = ProductRepository(db)

    def get_all_products(self):
        return self.repository.get_all_products()
    def create_product(self, new_product: ProductCreate):
        return self.repository.create(new_product)
    def update_product(self, product_id: int, update_product: UpdateProduct):
        existing_product = self.repository.get_by_id(product_id)
        if not existing_product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found"
            )
        return self.repository.update(existing_product, update_product)

    def delete_product(self, product_id: int):
        existing_customer = self.repository.get_by_id(product_id)
        if not existing_customer:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found"
            )
        self.repository.delete(existing_customer)