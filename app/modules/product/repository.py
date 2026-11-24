from starlette.middleware.sessions import Session
from sqlalchemy.orm import Session, joinedload
from app.modules.product.models import Product
from app.modules.product.schemas import ProductCreate, UpdateProduct


class ProductRepository():

    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, product_id: int):
        return self.db.query(Product).filter(Product.id==product_id).first()

    def get_all_products(self) -> list[Product]:
        return (
            self.db.query(Product)
            .options(joinedload(Product.customer))
            .order_by(Product.id.desc())
            .all()
        )

    def create(self, product_data: ProductCreate):
        new_product = Product(**product_data.model_dump())
        self.db.add(new_product)
        self.db.commit()
        self.db.refresh(new_product)
        return new_product

    def update(self, product: Product, product_data: UpdateProduct):
        update_fields = product_data.model_dump(exclude_unset=True)
        for key, value in update_fields.items():
         setattr(product, key, value)

        self.db.commit()
        self.db.refresh(product)
        return product

    def delete(self, product_id: int):
        self.db.delete(product_id)
        self.db.commit()

