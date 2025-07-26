from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, Any, List
import logging

from app.services.chatbot_service import ChatbotService

router = APIRouter()
logger = logging.getLogger(__name__)

# Global chatbot service instance
chatbot_service = None

def get_chatbot_service():
    global chatbot_service
    if chatbot_service is None:
        chatbot_service = ChatbotService()
    return chatbot_service

@router.get("/training/status")
async def get_training_status():
    """
    Get the current training status and summary
    """
    try:
        service = get_chatbot_service()
        summary = service.get_training_summary()
        
        return {
            "status": "trained",
            "summary": summary,
            "message": "Chatbot has been trained on the dataset"
        }
    except Exception as e:
        logger.error(f"Error getting training status: {e}")
        raise HTTPException(status_code=500, detail=f"Error getting training status: {str(e)}")

@router.post("/training/retrain")
async def retrain_chatbot():
    """
    Retrain the chatbot with current data
    """
    try:
        service = get_chatbot_service()
        service._train_chatbot()
        
        summary = service.get_training_summary()
        
        return {
            "status": "success",
            "message": "Chatbot retraining completed successfully",
            "summary": summary
        }
    except Exception as e:
        logger.error(f"Error during retraining: {e}")
        raise HTTPException(status_code=500, detail=f"Error during retraining: {str(e)}")

@router.get("/training/knowledge")
async def get_training_knowledge():
    """
    Get the knowledge base built during training
    """
    try:
        service = get_chatbot_service()
        training_service = service.training_service
        
        return {
            "product_knowledge": training_service.product_knowledge,
            "order_patterns": training_service.order_patterns,
            "inventory_patterns": training_service.inventory_patterns,
            "user_preferences": training_service.user_preferences,
            "response_patterns": training_service.response_patterns
        }
    except Exception as e:
        logger.error(f"Error getting training knowledge: {e}")
        raise HTTPException(status_code=500, detail=f"Error getting training knowledge: {str(e)}")

@router.get("/training/scenarios")
async def get_training_scenarios():
    """
    Get the training scenarios generated from the data
    """
    try:
        service = get_chatbot_service()
        scenarios = service.training_service.training_data.get('scenarios', [])
        
        return {
            "scenarios": scenarios,
            "count": len(scenarios)
        }
    except Exception as e:
        logger.error(f"Error getting training scenarios: {e}")
        raise HTTPException(status_code=500, detail=f"Error getting training scenarios: {str(e)}")

@router.get("/training/analytics")
async def get_training_analytics():
    """
    Get detailed analytics from the training data
    """
    try:
        service = get_chatbot_service()
        training_service = service.training_service
        
        analytics = {
            "product_analytics": {
                "total_categories": len(training_service.product_knowledge.get('categories', {})),
                "total_brands": len(training_service.product_knowledge.get('brands', {})),
                "price_range": training_service.product_knowledge.get('pricing', {}),
                "department_breakdown": training_service.product_knowledge.get('departments', {})
            },
            "order_analytics": {
                "status_distribution": training_service.order_patterns.get('status_distribution', {}),
                "order_sizes": training_service.order_patterns.get('order_sizes', {}),
                "popular_products": training_service.order_patterns.get('popular_products', {}),
                "gender_patterns": training_service.order_patterns.get('gender_patterns', {})
            },
            "inventory_analytics": {
                "stock_analysis": training_service.inventory_patterns.get('stock_analysis', {}),
                "category_availability": training_service.inventory_patterns.get('category_availability', {}),
                "distribution_centers": training_service.inventory_patterns.get('dc_availability', {}),
                "price_availability": training_service.inventory_patterns.get('price_availability', {})
            },
            "user_analytics": {
                "demographics": training_service.user_preferences.get('demographics', {}),
                "geographic": training_service.user_preferences.get('geographic', {}),
                "traffic_sources": training_service.user_preferences.get('traffic_sources', {}),
                "order_patterns": training_service.user_preferences.get('order_patterns', {})
            }
        }
        
        return analytics
    except Exception as e:
        logger.error(f"Error getting training analytics: {e}")
        raise HTTPException(status_code=500, detail=f"Error getting training analytics: {str(e)}")

@router.post("/training/test")
async def test_training_response(message: str):
    """
    Test the trained chatbot with a specific message
    """
    try:
        service = get_chatbot_service()
        
        # Create a test session
        test_session_id = "test_session_123"
        
        # Get response using training service
        enhanced_response = service.training_service.get_enhanced_response(message)
        
        # Get regular response
        regular_response = service.process_message(message, test_session_id)
        
        return {
            "input_message": message,
            "enhanced_response": enhanced_response,
            "regular_response": {
                "message": regular_response.message,
                "response_type": regular_response.metadata.get("response_type"),
                "confidence": regular_response.metadata.get("confidence"),
                "training_used": regular_response.metadata.get("training_used", False)
            },
            "comparison": {
                "enhanced_confidence": enhanced_response.get('confidence', 0),
                "regular_confidence": regular_response.metadata.get("confidence", 0),
                "improvement": enhanced_response.get('confidence', 0) - regular_response.metadata.get("confidence", 0)
            }
        }
    except Exception as e:
        logger.error(f"Error testing training response: {e}")
        raise HTTPException(status_code=500, detail=f"Error testing training response: {str(e)}") 