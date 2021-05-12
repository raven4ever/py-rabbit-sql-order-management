import enum

from sqlalchemy import Column, Integer, String, ForeignKey, Enum
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


class OrderStatus(enum.Enum):
    ACCEPTED = 0
    INSUFFICIENT_STOCK = 1
    NA = 999


class Order(Base):
    __tablename__ = 'ORDERS'

    id = Column(Integer, primary_key=True)
    client_name = Column(String(50))
    status = Column(Enum(OrderStatus), default=OrderStatus.NA)
    product_id = Column(Integer, ForeignKey('PRODUCTS.id'))
    product = relationship("Product", back_populates="orders")

    def __repr__(self):
        return f'Order(client={self.client_name}, status={self.status})'
