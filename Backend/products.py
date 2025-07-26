from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from datetime import datetime
import uuid

from app.models.product import Product, ProductSearchRequest, ProductSearchResponse, ProductCategory, ProductColor, ProductSize

router = APIRouter()

# Mock product data - in real implementation, this would come from database
MOCK_PRODUCTS = [
    Product(
        id="1",
        name="Classic White T-Shirt",
        description="Premium cotton t-shirt perfect for everyday wear",
        price=29.99,
        category=ProductCategory.SHIRTS,
        colors=[ProductColor.WHITE, ProductColor.BLACK, ProductColor.GRAY],
        sizes=[ProductSize.S, ProductSize.M, ProductSize.L, ProductSize.XL],
        images=["https://example.com/white-tshirt.jpg"],
        in_stock=True,
        stock_quantity=100,
        rating=4.5,
        review_count=127,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    ),
    Product(
        id="2",
        name="Slim Fit Jeans",
        description="Modern slim fit jeans with stretch comfort",
        price=79.99,
        category=ProductCategory.PANTS,
        colors=[ProductColor.BLUE, ProductColor.BLACK],
        sizes=[ProductSize.S, ProductSize.M, ProductSize.L, ProductSize.XL, ProductSize.XXL],
        images=["https://example.com/slim-jeans.jpg"],
        in_stock=True,
        stock_quantity=75,
        rating=4.2,
        review_count=89,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    ),
    Product(
        id="3",
        name="Summer Dress",
        description="Lightweight summer dress perfect for warm weather",
        price=59.99,
        category=ProductCategory.DRESSES,
        colors=[ProductColor.RED, ProductColor.BLUE, ProductColor.GREEN],
        sizes=[ProductSize.XS, ProductSize.S, ProductSize.M, ProductSize.L],
        images=["https://example.com/summer-dress.jpg"],
        in_stock=True,
        stock_quantity=50,
        rating=4.7,
        review_count=203,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    ),
    Product(
        id="4",
        name="Running Shoes",
        description="Comfortable running shoes with excellent support",
        price=129.99,
        category=ProductCategory.SHOES,
        colors=[ProductColor.BLACK, ProductColor.WHITE, ProductColor.RED],
        sizes=[ProductSize.S, ProductSize.M, ProductSize.L, ProductSize.XL],
        images=["https://example.com/running-shoes.jpg"],
        in_stock=True,
        stock_quantity=60,
        rating=4.6,
        review_count=156,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    ),
    Product(
        id="5",
        name="Leather Wallet",
        description="Genuine leather wallet with multiple card slots",
        price=39.99,
        category=ProductCategory.ACCESSORIES,
        colors=[ProductColor.BROWN, ProductColor.BLACK],
        sizes=[ProductSize.M],
        images=["https://example.com/leather-wallet.jpg"],
        in_stock=True,
        stock_quantity=200,
        rating=4.3,
        review_count=78,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
]

@router.get("/products", response_model=ProductSearchResponse)
async def get_products(
    query: Optional[str] = Query(None, description="Search query"),
    category: Optional[ProductCategory] = Query(None, description="Product category"),
    min_price: Optional[float] = Query(None, description="Minimum price"),
    max_price: Optional[float] = Query(None, description="Maximum price"),
    colors: Optional[List[ProductColor]] = Query(None, description="Filter by colors"),
    sizes: Optional[List[ProductSize]] = Query(None, description="Filter by sizes"),
    in_stock_only: bool = Query(False, description="Show only in-stock items"),
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(20, ge=1, le=100, description="Items per page")
):
    """
    Get products with optional filtering and pagination
    """
    try:
        # Filter products based on parameters
        filtered_products = MOCK_PRODUCTS.copy()
        
        # Apply filters
        if query:
            query_lower = query.lower()
            filtered_products = [
                p for p in filtered_products 
                if query_lower in p.name.lower() or query_lower in p.description.lower()
            ]
        
        if category:
            filtered_products = [p for p in filtered_products if p.category == category]
        
        if min_price is not None:
            filtered_products = [p for p in filtered_products if p.price >= min_price]
        
        if max_price is not None:
            filtered_products = [p for p in filtered_products if p.price <= max_price]
        
        if colors:
            filtered_products = [
                p for p in filtered_products 
                if any(color in p.colors for color in colors)
            ]
        
        if sizes:
            filtered_products = [
                p for p in filtered_products 
                if any(size in p.sizes for size in sizes)
            ]
        
        if in_stock_only:
            filtered_products = [p for p in filtered_products if p.in_stock]
        
        # Apply pagination
        total = len(filtered_products)
        start_idx = (page - 1) * limit
        end_idx = start_idx + limit
        paginated_products = filtered_products[start_idx:end_idx]
        
        total_pages = (total + limit - 1) // limit
        
        return ProductSearchResponse(
            products=paginated_products,
            total=total,
            page=page,
            limit=limit,
            total_pages=total_pages
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching products: {str(e)}")

@router.get("/products/{product_id}", response_model=Product)
async def get_product(product_id: str):
    """
    Get a specific product by ID
    """
    try:
        product = next((p for p in MOCK_PRODUCTS if p.id == product_id), None)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        return product
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching product: {str(e)}")

@router.get("/products/categories", response_model=List[str])
async def get_categories():
    """
    Get all available product categories
    """
    try:
        return [category.value for category in ProductCategory]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching categories: {str(e)}")

@router.get("/products/colors", response_model=List[str])
async def get_colors():
    """
    Get all available product colors
    """
    try:
        return [color.value for color in ProductColor]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching colors: {str(e)}")

@router.get("/products/sizes", response_model=List[str])
async def get_sizes():
    """
    Get all available product sizes
    """
    try:
        return [size.value for size in ProductSize]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching sizes: {str(e)}") 