import re
import random
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime
import uuid

from app.models.chat import ChatMessage, MessageType, ChatResponse
from app.core.config import settings
from app.services.data_service import DataService
from app.services.training_service import TrainingService

class ChatbotService:
    def __init__(self):
        self.name = settings.CHATBOT_NAME
        self.welcome_message = settings.CHATBOT_WELCOME_MESSAGE
        self.data_service = DataService()
        self.training_service = TrainingService(self.data_service)
        
        # Train the chatbot on startup
        self._train_chatbot()
        
        # Define response patterns and templates
        self.response_patterns = {
            # Greetings
            r'\b(hi|hello|hey|good morning|good afternoon|good evening)\b': self._handle_greeting,
            
            # Product analytics
            r'\b(top\s+\d+\s+most\s+sold|best\s+sellers|popular\s+products|trending)\b': self._handle_top_products_inquiry,
            r'\b(most\s+sold|best\s+selling|top\s+products)\b': self._handle_top_products_inquiry,
            
            # Product inquiries
            r'\b(product|item|clothing|shirt|pants|dress|shoes|accessories)\b': self._handle_product_inquiry,
            r'\b(price|cost|how much|expensive|cheap)\b': self._handle_price_inquiry,
            r'\b(size|fit|measurement|small|medium|large)\b': self._handle_size_inquiry,
            r'\b(color|colour|red|blue|green|black|white)\b': self._handle_color_inquiry,
            
            # Order inquiries
            r'\b(order\s+id\s+\d+|order\s+#\d+|status\s+of\s+order)\b': self._handle_order_status_inquiry,
            r'\b(order|purchase|buy|shopping cart|checkout)\b': self._handle_order_inquiry,
            r'\b(track|tracking|where is|delivery|shipping)\b': self._handle_tracking_inquiry,
            r'\b(return|refund|exchange|cancel)\b': self._handle_return_inquiry,
            
            # Inventory inquiries
            r'\b(stock|inventory|available|left\s+in\s+stock|how\s+many)\b': self._handle_inventory_inquiry,
            
            # General support
            r'\b(help|support|assist|problem|issue)\b': self._handle_help_request,
            r'\b(contact|phone|email|customer service)\b': self._handle_contact_inquiry,
            r'\b(policy|terms|conditions|warranty)\b': self._handle_policy_inquiry,
            
            # Payment
            r'\b(payment|pay|credit card|debit|paypal)\b': self._handle_payment_inquiry,
            
            # Shipping
            r'\b(shipping|delivery|free shipping|express|standard)\b': self._handle_shipping_inquiry,
        }
        
        # Response templates
        self.templates = {
            'greeting': [
                "Hello! I'm {name}, your fashion assistant. How can I help you today?",
                "Hi there! I'm {name}, ready to help you with all your fashion needs!",
                "Welcome! I'm {name}, your personal shopping assistant. What can I do for you?"
            ],
            'product_info': [
                "I'd be happy to help you find the perfect {category}! What specific style or features are you looking for?",
                "Great choice! We have a wide selection of {category}. Would you like me to show you our best sellers?",
                "Our {category} collection is amazing! What size and color are you interested in?"
            ],
            'price_info': [
                "Our prices range from ${min_price} to ${max_price} for {category}. Is there a specific budget you have in mind?",
                "We offer competitive pricing on all our {category}. Plus, we have regular sales and discounts!",
                "Prices vary by style and material. Would you like me to show you our most popular {category} options?"
            ],
            'size_help': [
                "We offer sizes XS to XXL for most items. You can find our size guide on each product page, or I can help you find the right fit!",
                "Not sure about your size? Our detailed size charts are available on every product page. Would you like me to explain how to measure?",
                "We have a comprehensive size guide to help you find the perfect fit. What's your usual size in other brands?"
            ],
            'order_help': [
                "I can help you with your order! Do you need help placing a new order or checking an existing one?",
                "For orders, you can browse our catalog and add items to your cart. Would you like me to show you our featured products?",
                "Placing an order is easy! Just add items to your cart and proceed to checkout. Need help finding something specific?"
            ],
            'tracking_help': [
                "To track your order, you'll need your order number. You can find it in your order confirmation email or account dashboard.",
                "Once your order ships, you'll receive a tracking number via email. You can also check your order status in your account.",
                "Track your order by logging into your account or using the tracking number from your shipping confirmation email."
            ],
            'return_help': [
                "We have a 30-day return policy for most items. Items must be unworn and in original packaging. Would you like me to explain the process?",
                "Returns are easy! You can initiate a return through your account or contact our customer service team.",
                "Our return policy allows returns within 30 days of delivery. Just make sure items are in original condition!"
            ],
            'contact_help': [
                "You can reach our customer service team at support@fashionstore.com or call us at 1-800-FASHION. We're here to help!",
                "Need to speak with someone? Our customer service team is available Monday-Friday, 9 AM to 6 PM EST.",
                "For immediate assistance, you can email us at support@fashionstore.com or use our live chat feature."
            ],
            'payment_help': [
                "We accept all major credit cards, PayPal, and Apple Pay. All payments are secure and encrypted.",
                "Payment options include Visa, MasterCard, American Express, PayPal, and Apple Pay. Your payment information is always secure.",
                "We offer multiple secure payment methods including credit cards, PayPal, and digital wallets."
            ],
            'shipping_help': [
                "We offer free standard shipping on orders over $50! Express shipping is available for faster delivery.",
                "Standard shipping takes 3-5 business days and is free on orders over $50. Express shipping (1-2 days) is available for an additional fee.",
                "Free shipping on orders over $50! Standard delivery takes 3-5 days, or upgrade to express for 1-2 day delivery."
            ],
            'fallback': [
                "I'm not sure I understood that. Could you rephrase your question? I'm here to help with products, orders, returns, and general support!",
                "I didn't quite catch that. Are you asking about our products, orders, returns, or something else?",
                "Let me help you better. Are you looking for product information, order help, or customer support?"
            ]
        }
        
        # Quick reply suggestions
        self.quick_replies = {
            'greeting': ["Show me products", "Track my order", "Return policy", "Contact support"],
            'product': ["Men's clothing", "Women's clothing", "Accessories", "Sale items"],
            'order': ["Place order", "Track order", "Order history", "Cancel order"],
            'support': ["Returns", "Shipping", "Payment", "Contact us"]
        }

    def _train_chatbot(self):
        """Train the chatbot with the dataset"""
        try:
            success = self.training_service.train_chatbot()
            if success:
                print("✅ Chatbot training completed successfully!")
                summary = self.training_service.get_training_summary()
                print(f"📊 Training Summary: {summary}")
            else:
                print("❌ Chatbot training failed!")
        except Exception as e:
            print(f"⚠️ Training error: {e}")

    def process_message(self, message: str, session_id: str, context: Optional[Dict[str, Any]] = None) -> ChatResponse:
        """Process user message and generate appropriate response"""
        message_lower = message.lower().strip()
        
        # First, try to get enhanced response from training service
        enhanced_response = self.training_service.get_enhanced_response(message_lower, context)
        
        if enhanced_response['confidence'] > 0.7:
            # Use enhanced response from training
            response_text = enhanced_response['template']
            response_type = enhanced_response['response_type']
        else:
            # Fall back to pattern matching
            response_text, response_type = self._match_patterns(message_lower, context)
        
        # Generate quick replies based on response type
        quick_replies = self.quick_replies.get(response_type, [])
        
        # Generate suggestions based on context
        suggestions = self._generate_suggestions(message_lower, context)
        
        return ChatResponse(
            message=response_text,
            session_id=session_id,
            timestamp=datetime.utcnow(),
            suggestions=suggestions,
            quick_replies=quick_replies,
            metadata={
                "response_type": response_type,
                "confidence": enhanced_response.get('confidence', 0.9),
                "context": context,
                "training_used": enhanced_response['confidence'] > 0.7
            }
        )

    def _match_patterns(self, message: str, context: Optional[Dict[str, Any]] = None) -> Tuple[str, str]:
        """Match message against patterns and return appropriate response"""
        for pattern, handler in self.response_patterns.items():
            if re.search(pattern, message, re.IGNORECASE):
                return handler(message, context)
        
        # Fallback response
        return self._handle_fallback(message, context)

    def _handle_greeting(self, message: str, context: Optional[Dict[str, Any]] = None) -> Tuple[str, str]:
        """Handle greeting messages"""
        template = random.choice(self.templates['greeting'])
        return template.format(name=self.name), 'greeting'

    def _handle_product_inquiry(self, message: str, context: Optional[Dict[str, Any]] = None) -> Tuple[str, str]:
        """Handle product-related inquiries"""
        # Extract category from message
        categories = ['shirt', 'pants', 'dress', 'shoes', 'accessories', 'clothing']
        category = 'clothing'
        
        for cat in categories:
            if cat in message:
                category = cat
                break
        
        template = random.choice(self.templates['product_info'])
        return template.format(category=category), 'product'

    def _handle_price_inquiry(self, message: str, context: Optional[Dict[str, Any]] = None) -> Tuple[str, str]:
        """Handle price-related inquiries"""
        template = random.choice(self.templates['price_info'])
        return template.format(category='clothing', min_price=25, max_price=200), 'product'

    def _handle_size_inquiry(self, message: str, context: Optional[Dict[str, Any]] = None) -> Tuple[str, str]:
        """Handle size-related inquiries"""
        template = random.choice(self.templates['size_help'])
        return template, 'product'

    def _handle_color_inquiry(self, message: str, context: Optional[Dict[str, Any]] = None) -> Tuple[str, str]:
        """Handle color-related inquiries"""
        return "We offer a wide range of colors including black, white, red, blue, green, and many more! What's your favorite color?", 'product'

    def _handle_order_inquiry(self, message: str, context: Optional[Dict[str, Any]] = None) -> Tuple[str, str]:
        """Handle order-related inquiries"""
        template = random.choice(self.templates['order_help'])
        return template, 'order'

    def _handle_tracking_inquiry(self, message: str, context: Optional[Dict[str, Any]] = None) -> Tuple[str, str]:
        """Handle tracking-related inquiries"""
        template = random.choice(self.templates['tracking_help'])
        return template, 'order'

    def _handle_return_inquiry(self, message: str, context: Optional[Dict[str, Any]] = None) -> Tuple[str, str]:
        """Handle return-related inquiries"""
        template = random.choice(self.templates['return_help'])
        return template, 'support'

    def _handle_help_request(self, message: str, context: Optional[Dict[str, Any]] = None) -> Tuple[str, str]:
        """Handle general help requests"""
        return "I'm here to help! I can assist with product information, orders, returns, shipping, and more. What do you need help with?", 'support'

    def _handle_contact_inquiry(self, message: str, context: Optional[Dict[str, Any]] = None) -> Tuple[str, str]:
        """Handle contact-related inquiries"""
        template = random.choice(self.templates['contact_help'])
        return template, 'support'

    def _handle_policy_inquiry(self, message: str, context: Optional[Dict[str, Any]] = None) -> Tuple[str, str]:
        """Handle policy-related inquiries"""
        return "Our policies include a 30-day return policy, secure payment processing, and free shipping on orders over $50. Which policy would you like to know more about?", 'support'

    def _handle_payment_inquiry(self, message: str, context: Optional[Dict[str, Any]] = None) -> Tuple[str, str]:
        """Handle payment-related inquiries"""
        template = random.choice(self.templates['payment_help'])
        return template, 'support'

    def _handle_shipping_inquiry(self, message: str, context: Optional[Dict[str, Any]] = None) -> Tuple[str, str]:
        """Handle shipping-related inquiries"""
        template = random.choice(self.templates['shipping_help'])
        return template, 'support'

    def _handle_top_products_inquiry(self, message: str, context: Optional[Dict[str, Any]] = None) -> Tuple[str, str]:
        """Handle top products inquiries"""
        try:
            # Extract number from message (default to 5)
            import re
            number_match = re.search(r'top\s+(\d+)', message.lower())
            limit = int(number_match.group(1)) if number_match else 5
            
            top_products = self.data_service.get_top_products(limit)
            
            if not top_products:
                return "I don't have sales data available right now. Would you like me to show you our featured products instead?", 'product'
            
            response = f"Based on our sales data, here are the top {limit} most sold products:\n\n"
            
            for i, product in enumerate(top_products, 1):
                response += f"{i}. {product['name']} - {product['units_sold']} units sold (${product['unit_price']:.2f})\n"
            
            response += "\nWould you like me to show you similar products or help you find something specific?"
            
            return response, 'product'
            
        except Exception as e:
            return "I'm having trouble accessing the sales data right now. Would you like me to show you our featured products instead?", 'product'

    def _handle_order_status_inquiry(self, message: str, context: Optional[Dict[str, Any]] = None) -> Tuple[str, str]:
        """Handle order status inquiries"""
        try:
            # Extract order ID from message
            import re
            order_match = re.search(r'order\s+(?:id\s+)?#?(\d+)', message.lower())
            if not order_match:
                return "I need an order ID to check the status. Could you please provide your order number?", 'order'
            
            order_id = order_match.group(1)
            order_status = self.data_service.get_order_status(order_id)
            
            if not order_status:
                return f"I couldn't find order #{order_id}. Please check the order number and try again.", 'order'
            
            response = f"I found your order #{order_id}. Here's the current status:\n\n"
            response += f"📦 Order Status: {order_status['status'].title()}\n"
            response += f"📅 Order Date: {order_status['created_at']}\n"
            response += f"👤 Customer: {order_status['user_name']}\n"
            
            if order_status['shipped_at']:
                response += f"🚚 Shipped: {order_status['shipped_at']}\n"
            if order_status['delivered_at']:
                response += f"📦 Delivered: {order_status['delivered_at']}\n"
            
            response += f"\nOrder Details:\n"
            for item in order_status['items']:
                response += f"- {item['name']} - ${item['retail_price']:.2f} ({item['status']})\n"
            
            response += f"\nTotal: ${order_status['total_amount']:.2f}\n\n"
            response += "Would you like me to help you track this package or answer any questions about your order?"
            
            return response, 'order'
            
        except Exception as e:
            return "I'm having trouble accessing the order information right now. Please try again or contact our support team.", 'order'

    def _handle_inventory_inquiry(self, message: str, context: Optional[Dict[str, Any]] = None) -> Tuple[str, str]:
        """Handle inventory inquiries"""
        try:
            # Extract product name from message
            import re
            
            # Look for specific product mentions
            product_keywords = ['t-shirt', 'shirt', 'jeans', 'dress', 'shoes', 'wallet']
            found_product = None
            
            for keyword in product_keywords:
                if keyword in message.lower():
                    found_product = keyword
                    break
            
            if not found_product:
                return "I can help you check inventory for specific products. What item would you like to check?", 'product'
            
            inventory_status = self.data_service.get_inventory_status(product_name=found_product)
            
            if not inventory_status:
                return f"I don't have inventory data for {found_product} right now. Would you like me to show you similar products?", 'product'
            
            response = f"I checked our inventory for {found_product.title()}. Here's what's available:\n\n"
            
            for item in inventory_status:
                response += f"📦 {item['product_name']}:\n"
                response += f"   - Available: {item['available_quantity']} units\n"
                response += f"   - Price: ${item['product_retail_price']:.2f}\n"
                if 'name' in item:  # distribution center name
                    response += f"   - Location: {item['name']}\n"
                response += "\n"
            
            response += "Would you like me to help you place an order or check other products?"
            
            return response, 'product'
            
        except Exception as e:
            return "I'm having trouble accessing the inventory data right now. Would you like me to show you our product catalog instead?", 'product'

    def _handle_fallback(self, message: str, context: Optional[Dict[str, Any]] = None) -> Tuple[str, str]:
        """Handle unrecognized messages"""
        template = random.choice(self.templates['fallback'])
        return template, 'support'

    def _generate_suggestions(self, message: str, context: Optional[Dict[str, Any]] = None) -> List[str]:
        """Generate contextual suggestions based on message and context"""
        suggestions = []
        
        if any(word in message for word in ['product', 'item', 'clothing']):
            suggestions.extend(["Show me men's clothing", "Show me women's clothing", "What's on sale?"])
        elif any(word in message for word in ['order', 'track', 'delivery']):
            suggestions.extend(["Track my order", "Order history", "Shipping info"])
        elif any(word in message for word in ['return', 'refund', 'exchange']):
            suggestions.extend(["Return policy", "Start return", "Contact support"])
        else:
            suggestions.extend(["Browse products", "Track order", "Get help"])
        
        return suggestions[:3]  # Limit to 3 suggestions

    def get_welcome_message(self, session_id: str) -> ChatResponse:
        """Get welcome message for new chat session"""
        return ChatResponse(
            message=self.welcome_message,
            session_id=session_id,
            timestamp=datetime.utcnow(),
            quick_replies=self.quick_replies['greeting'],
            metadata={
                "response_type": "welcome",
                "confidence": 1.0
            }
        )

    def get_training_summary(self) -> Dict[str, Any]:
        """Get training summary for monitoring"""
        return self.training_service.get_training_summary() 