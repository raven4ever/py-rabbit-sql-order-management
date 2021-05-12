from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Product(Base):
    __tablename__ = 'PRODUCTS'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    quantity = Column(Integer)
    orders = relationship("Order", back_populates="product")

    def __repr__(self):
        return f'Product(name={self.name}, quantity={self.quantity})'


class Order(Base):
    __tablename__ = 'ORDERS'

    id = Column(Integer, primary_key=True)
    client_name = Column(String(50))
    status = Column(String(50))
    product_id = Column(Integer, ForeignKey('PRODUCTS.id'))
    product = relationship("Product", back_populates="orders")

    def __repr__(self):
        return f'Order'
