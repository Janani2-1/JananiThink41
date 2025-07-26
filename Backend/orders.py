from fastapi import APIRouter, HTTPException
from typing import List, Optional
from datetime import datetime, timedelta
import uuid

from app.models.order import Order, OrderCreateRequest, OrderUpdateRequest, OrderStatus, PaymentStatus, ShippingMethod

router = APIRouter()

# Mock order data - in real implementation, this would come from database
MOCK_ORDERS = [
    Order(
        id="ORD-001",
        user_id="user123",
        items=[
            {
                "product_id": "1",
                "product_name": "Classic White T-Shirt",
                "quantity": 2,
                "unit_price": 29.99,
                "total_price": 59.98,
                "size": "M",
                "color": "white"
            }
        ],
        total_amount=59.98,
        shipping_address={
            "first_name": "John",
            "last_name": "Doe",
            "address_line1": "123 Main St",
            "city": "New York",
            "state": "NY",
            "postal_code": "10001",
            "country": "US"
        },
        shipping_method=ShippingMethod.STANDARD,
        shipping_cost=0.0,
        tax_amount=5.99,
        discount_amount=0.0,
        final_amount=65.97,
        status=OrderStatus.SHIPPED,
        payment_status=PaymentStatus.PAID,
        tracking_number="1Z999AA1234567890",
        estimated_delivery=datetime.utcnow() + timedelta(days=3),
        created_at=datetime.utcnow() - timedelta(days=5),
        updated_at=datetime.utcnow() - timedelta(days=2)
    ),
    Order(
        id="ORD-002",
        user_id="user123",
        items=[
            {
                "product_id": "2",
                "product_name": "Slim Fit Jeans",
                "quantity": 1,
                "unit_price": 79.99,
                "total_price": 79.99,
                "size": "L",
                "color": "blue"
            }
        ],
        total_amount=79.99,
        shipping_address={
            "first_name": "John",
            "last_name": "Doe",
            "address_line1": "123 Main St",
            "city": "New York",
            "state": "NY",
            "postal_code": "10001",
            "country": "US"
        },
        shipping_method=ShippingMethod.EXPRESS,
        shipping_cost=15.99,
        tax_amount=7.99,
        discount_amount=10.0,
        final_amount=93.97,
        status=OrderStatus.PROCESSING,
        payment_status=PaymentStatus.PAID,
        tracking_number=None,
        estimated_delivery=datetime.utcnow() + timedelta(days=1),
        created_at=datetime.utcnow() - timedelta(days=1),
        updated_at=datetime.utcnow()
    )
]

@router.get("/orders", response_model=List[Order])
async def get_orders(user_id: Optional[str] = None, status: Optional[OrderStatus] = None):
    """
    Get orders with optional filtering by user ID and status
    """
    try:
        filtered_orders = MOCK_ORDERS.copy()
        
        if user_id:
            filtered_orders = [o for o in filtered_orders if o.user_id == user_id]
        
        if status:
            filtered_orders = [o for o in filtered_orders if o.status == status]
        
        return filtered_orders
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching orders: {str(e)}")

@router.get("/orders/{order_id}", response_model=Order)
async def get_order(order_id: str):
    """
    Get a specific order by ID
    """
    try:
        order = next((o for o in MOCK_ORDERS if o.id == order_id), None)
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")
        return order
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching order: {str(e)}")

@router.post("/orders", response_model=Order)
async def create_order(request: OrderCreateRequest):
    """
    Create a new order
    """
    try:
        # Calculate totals
        total_amount = sum(item["total_price"] for item in request.items)
        
        # Calculate shipping cost based on method
        shipping_costs = {
            ShippingMethod.STANDARD: 0.0 if total_amount >= 50 else 5.99,
            ShippingMethod.EXPRESS: 15.99,
            ShippingMethod.NEXT_DAY: 25.99
        }
        shipping_cost = shipping_costs.get(request.shipping_method, 0.0)
        
        # Calculate tax (simplified)
        tax_amount = total_amount * 0.08  # 8% tax
        
        # Calculate final amount
        final_amount = total_amount + shipping_cost + tax_amount - request.discount_amount if hasattr(request, 'discount_amount') else 0.0
        
        # Create order
        order = Order(
            id=f"ORD-{uuid.uuid4().hex[:8].upper()}",
            user_id=request.user_id,
            items=request.items,
            total_amount=total_amount,
            shipping_address=request.shipping_address,
            shipping_method=request.shipping_method,
            shipping_cost=shipping_cost,
            tax_amount=tax_amount,
            discount_amount=getattr(request, 'discount_amount', 0.0),
            final_amount=final_amount,
            status=OrderStatus.PENDING,
            payment_status=PaymentStatus.PENDING,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
            notes=request.notes
        )
        
        # In real implementation, save to database
        MOCK_ORDERS.append(order)
        
        return order
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating order: {str(e)}")

@router.put("/orders/{order_id}", response_model=Order)
async def update_order(order_id: str, request: OrderUpdateRequest):
    """
    Update an existing order
    """
    try:
        order = next((o for o in MOCK_ORDERS if o.id == order_id), None)
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")
        
        # Update fields if provided
        if request.status is not None:
            order.status = request.status
        if request.payment_status is not None:
            order.payment_status = request.payment_status
        if request.tracking_number is not None:
            order.tracking_number = request.tracking_number
        if request.estimated_delivery is not None:
            order.estimated_delivery = request.estimated_delivery
        if request.notes is not None:
            order.notes = request.notes
        
        order.updated_at = datetime.utcnow()
        
        return order
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating order: {str(e)}")

@router.delete("/orders/{order_id}")
async def cancel_order(order_id: str):
    """
    Cancel an order
    """
    try:
        order = next((o for o in MOCK_ORDERS if o.id == order_id), None)
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")
        
        if order.status in [OrderStatus.SHIPPED, OrderStatus.DELIVERED]:
            raise HTTPException(status_code=400, detail="Cannot cancel shipped or delivered orders")
        
        order.status = OrderStatus.CANCELLED
        order.updated_at = datetime.utcnow()
        
        return {"message": "Order cancelled successfully", "order_id": order_id}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error cancelling order: {str(e)}")

@router.get("/orders/{order_id}/tracking")
async def get_order_tracking(order_id: str):
    """
    Get tracking information for an order
    """
    try:
        order = next((o for o in MOCK_ORDERS if o.id == order_id), None)
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")
        
        if not order.tracking_number:
            return {
                "order_id": order_id,
                "status": order.status,
                "tracking_number": None,
                "message": "Tracking information not available yet"
            }
        
        # Mock tracking information
        tracking_info = {
            "order_id": order_id,
            "tracking_number": order.tracking_number,
            "status": order.status,
            "estimated_delivery": order.estimated_delivery,
            "shipping_method": order.shipping_method,
            "tracking_events": [
                {
                    "timestamp": order.created_at,
                    "status": "Order placed",
                    "location": "Online"
                },
                {
                    "timestamp": order.created_at + timedelta(hours=2),
                    "status": "Order confirmed",
                    "location": "Warehouse"
                },
                {
                    "timestamp": order.updated_at,
                    "status": "Shipped",
                    "location": "Distribution Center"
                }
            ]
        }
        
        return tracking_info
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching tracking info: {str(e)}") 