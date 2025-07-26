from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from app.models.base import Base

class ProductCategory(str, Enum):
    SHIRTS = "shirts"
    PANTS = "pants"
    DRESSES = "dresses"
    SHOES = "shoes"
    ACCESSORIES = "accessories"
    OUTERWEAR = "outerwear"

class ProductSize(str, Enum):
    XS = "XS"
    S = "S"
    M = "M"
    L = "L"
    XL = "XL"
    XXL = "XXL"

class ProductColor(str, Enum):
    BLACK = "black"
    WHITE = "white"
    RED = "red"
    BLUE = "blue"
    GREEN = "green"
    YELLOW = "yellow"
    PINK = "pink"
    PURPLE = "purple"
    BROWN = "brown"
    GRAY = "gray"

class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True, index=True)
    cost = Column(Float)
    category = Column(String)
    name = Column(String, nullable=False)
    brand = Column(String)
    retail_price = Column(Float)
    department = Column(String)
    sku = Column(String)
    distribution_center_id = Column(Integer, ForeignKey('distribution_centers.id'))

class ProductSearchRequest(BaseModel):
    query: Optional[str] = None
    category: Optional[ProductCategory] = None
    min_price: Optional[float] = None
    max_price: Optional[float] = None
    colors: Optional[List[ProductColor]] = None
    sizes: Optional[List[ProductSize]] = None
    in_stock_only: bool = False
    page: int = 1
    limit: int = 20

class ProductSearchResponse(BaseModel):
    products: List[Product]
    total: int
    page: int
    limit: int
    total_pages: int 