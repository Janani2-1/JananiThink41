import pandas as pd
import numpy as np
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime
import logging
import json
import re
from collections import Counter, defaultdict

logger = logging.getLogger(__name__)

class TrainingService:
    def __init__(self, data_service):
        self.data_service = data_service
        self.training_data = {}
        self.response_patterns = {}
        self.product_knowledge = {}
        self.order_patterns = {}
        self.inventory_patterns = {}
        self.user_preferences = {}
        
    def train_chatbot(self):
        """Main training function that processes all data and builds knowledge base"""
        logger.info("Starting chatbot training...")
        
        try:
            # Train on different aspects of the data
            self._train_product_knowledge()
            self._train_order_patterns()
            self._train_inventory_patterns()
            self._train_user_preferences()
            self._build_response_templates()
            self._generate_training_scenarios()
            
            logger.info("Chatbot training completed successfully!")
            return True
            
        except Exception as e:
            logger.error(f"Error during training: {e}")
            return False
    
    def _train_product_knowledge(self):
        """Extract and organize product knowledge from the dataset"""
        logger.info("Training product knowledge...")
        
        if 'products' not in self.data_service.dfs:
            return
        
        products_df = self.data_service.dfs['products']
        
        # Product categories and their characteristics
        self.product_knowledge['categories'] = {}
        for category in products_df['category'].unique():
            category_products = products_df[products_df['category'] == category]
            self.product_knowledge['categories'][category] = {
                'count': len(category_products),
                'avg_price': category_products['retail_price'].mean(),
                'price_range': {
                    'min': category_products['retail_price'].min(),
                    'max': category_products['retail_price'].max()
                },
                'brands': category_products['brand'].unique().tolist(),
                'departments': category_products['department'].unique().tolist()
            }
        
        # Brand analysis
        self.product_knowledge['brands'] = {}
        for brand in products_df['brand'].unique():
            brand_products = products_df[products_df['brand'] == brand]
            self.product_knowledge['brands'][brand] = {
                'product_count': len(brand_products),
                'categories': brand_products['category'].unique().tolist(),
                'avg_price': brand_products['retail_price'].mean(),
                'price_range': {
                    'min': brand_products['retail_price'].min(),
                    'max': brand_products['retail_price'].max()
                }
            }
        
        # Price analysis
        self.product_knowledge['pricing'] = {
            'overall_avg': products_df['retail_price'].mean(),
            'overall_min': products_df['retail_price'].min(),
            'overall_max': products_df['retail_price'].max(),
            'price_tiers': {
                'budget': products_df[products_df['retail_price'] <= 30]['retail_price'].mean(),
                'mid_range': products_df[(products_df['retail_price'] > 30) & (products_df['retail_price'] <= 80)]['retail_price'].mean(),
                'premium': products_df[products_df['retail_price'] > 80]['retail_price'].mean()
            }
        }
        
        # Department analysis
        self.product_knowledge['departments'] = {}
        for dept in products_df['department'].unique():
            dept_products = products_df[products_df['department'] == dept]
            self.product_knowledge['departments'][dept] = {
                'product_count': len(dept_products),
                'categories': dept_products['category'].unique().tolist(),
                'avg_price': dept_products['retail_price'].mean()
            }
    
    def _train_order_patterns(self):
        """Analyze order patterns and customer behavior"""
        logger.info("Training order patterns...")
        
        if 'orders' not in self.data_service.dfs or 'order_items' not in self.data_service.dfs:
            return
        
        orders_df = self.data_service.dfs['orders']
        order_items_df = self.data_service.dfs['order_items']
        
        # Order status patterns
        self.order_patterns['status_distribution'] = orders_df['status'].value_counts().to_dict()
        
        # Order size analysis
        self.order_patterns['order_sizes'] = {
            'avg_items': orders_df['num_of_item'].mean(),
            'size_distribution': orders_df['num_of_item'].value_counts().to_dict(),
            'large_orders': len(orders_df[orders_df['num_of_item'] > 2]),
            'small_orders': len(orders_df[orders_df['num_of_item'] <= 2])
        }
        
        # Gender-based patterns
        if 'gender' in orders_df.columns:
            self.order_patterns['gender_patterns'] = {
                'distribution': orders_df['gender'].value_counts().to_dict(),
                'avg_order_size_by_gender': orders_df.groupby('gender')['num_of_item'].mean().to_dict()
            }
        
        # Time-based patterns
        if 'created_at' in orders_df.columns:
            orders_df['created_at'] = pd.to_datetime(orders_df['created_at'])
            self.order_patterns['time_patterns'] = {
                'total_orders': len(orders_df),
                'date_range': {
                    'earliest': orders_df['created_at'].min().strftime('%Y-%m-%d'),
                    'latest': orders_df['created_at'].max().strftime('%Y-%m-%d')
                }
            }
        
        # Product popularity in orders
        if 'products' in self.data_service.dfs:
            products_df = self.data_service.dfs['products']
            order_items_with_products = order_items_df.merge(
                products_df, left_on='product_id', right_on='id', how='inner'
            )
            
            self.order_patterns['popular_products'] = order_items_with_products.groupby(
                ['product_id', 'name', 'category']
            ).size().sort_values(ascending=False).head(10).to_dict()
    
    def _train_inventory_patterns(self):
        """Analyze inventory patterns and stock management"""
        logger.info("Training inventory patterns...")
        
        if 'inventory_items' not in self.data_service.dfs:
            return
        
        inventory_df = self.data_service.dfs['inventory_items']
        
        # Stock availability analysis
        available_stock = inventory_df[inventory_df['sold_at'].isna()]
        sold_stock = inventory_df[inventory_df['sold_at'].notna()]
        
        self.inventory_patterns['stock_analysis'] = {
            'total_items': len(inventory_df),
            'available_items': len(available_stock),
            'sold_items': len(sold_stock),
            'availability_rate': len(available_stock) / len(inventory_df) * 100
        }
        
        # Product availability by category
        if 'product_category' in available_stock.columns:
            self.inventory_patterns['category_availability'] = available_stock.groupby(
                'product_category'
            ).size().sort_values(ascending=False).to_dict()
        
        # Distribution center analysis
        if 'product_distribution_center_id' in available_stock.columns:
            self.inventory_patterns['dc_availability'] = available_stock.groupby(
                'product_distribution_center_id'
            ).size().sort_values(ascending=False).to_dict()
        
        # Price-based availability
        if 'product_retail_price' in available_stock.columns:
            self.inventory_patterns['price_availability'] = {
                'budget_items': len(available_stock[available_stock['product_retail_price'] <= 30]),
                'mid_range_items': len(available_stock[(available_stock['product_retail_price'] > 30) & (available_stock['product_retail_price'] <= 80)]),
                'premium_items': len(available_stock[available_stock['product_retail_price'] > 80])
            }
    
    def _train_user_preferences(self):
        """Analyze user behavior and preferences"""
        logger.info("Training user preferences...")
        
        if 'users' not in self.data_service.dfs or 'orders' not in self.data_service.dfs:
            return
        
        users_df = self.data_service.dfs['users']
        orders_df = self.data_service.dfs['orders']
        
        # User demographics
        self.user_preferences['demographics'] = {
            'total_users': len(users_df),
            'gender_distribution': users_df['gender'].value_counts().to_dict() if 'gender' in users_df.columns else {},
            'age_analysis': {
                'avg_age': users_df['age'].mean() if 'age' in users_df.columns else None,
                'age_range': {
                    'min': users_df['age'].min() if 'age' in users_df.columns else None,
                    'max': users_df['age'].max() if 'age' in users_df.columns else None
                }
            } if 'age' in users_df.columns else {}
        }
        
        # Geographic analysis
        if 'state' in users_df.columns:
            self.user_preferences['geographic'] = {
                'top_states': users_df['state'].value_counts().head(5).to_dict(),
                'state_count': len(users_df['state'].unique())
            }
        
        # Traffic source analysis
        if 'traffic_source' in users_df.columns:
            self.user_preferences['traffic_sources'] = users_df['traffic_source'].value_counts().to_dict()
        
        # User order patterns
        user_order_counts = orders_df['user_id'].value_counts()
        self.user_preferences['order_patterns'] = {
            'avg_orders_per_user': user_order_counts.mean(),
            'most_active_users': user_order_counts.head(5).to_dict(),
            'single_order_users': len(user_order_counts[user_order_counts == 1]),
            'repeat_customers': len(user_order_counts[user_order_counts > 1])
        }
    
    def _build_response_templates(self):
        """Build intelligent response templates based on training data"""
        logger.info("Building response templates...")
        
        # Product-related templates
        self.response_patterns['product_templates'] = {
            'category_info': {
                'shirts': f"We have {self.product_knowledge.get('categories', {}).get('shirts', {}).get('count', 0)} shirts available, with prices ranging from ${self.product_knowledge.get('categories', {}).get('shirts', {}).get('price_range', {}).get('min', 0):.2f} to ${self.product_knowledge.get('categories', {}).get('shirts', {}).get('price_range', {}).get('max', 0):.2f}.",
                'pants': f"Our pants collection includes {self.product_knowledge.get('categories', {}).get('pants', {}).get('count', 0)} items, priced between ${self.product_knowledge.get('categories', {}).get('pants', {}).get('price_range', {}).get('min', 0):.2f} and ${self.product_knowledge.get('categories', {}).get('pants', {}).get('price_range', {}).get('max', 0):.2f}.",
                'dresses': f"We offer {self.product_knowledge.get('categories', {}).get('dresses', {}).get('count', 0)} beautiful dresses, with prices from ${self.product_knowledge.get('categories', {}).get('dresses', {}).get('price_range', {}).get('min', 0):.2f} to ${self.product_knowledge.get('categories', {}).get('dresses', {}).get('price_range', {}).get('max', 0):.2f}.",
                'shoes': f"Our shoe collection features {self.product_knowledge.get('categories', {}).get('shoes', {}).get('count', 0)} styles, ranging from ${self.product_knowledge.get('categories', {}).get('shoes', {}).get('price_range', {}).get('min', 0):.2f} to ${self.product_knowledge.get('categories', {}).get('shoes', {}).get('price_range', {}).get('max', 0):.2f}.",
                'accessories': f"We have {self.product_knowledge.get('categories', {}).get('accessories', {}).get('count', 0)} accessories available, priced from ${self.product_knowledge.get('categories', {}).get('accessories', {}).get('price_range', {}).get('min', 0):.2f} to ${self.product_knowledge.get('categories', {}).get('accessories', {}).get('price_range', {}).get('max', 0):.2f}."
            },
            'price_info': {
                'budget': f"We have budget-friendly options starting at ${self.product_knowledge.get('pricing', {}).get('price_tiers', {}).get('budget', 0):.2f}.",
                'mid_range': f"Our mid-range products average around ${self.product_knowledge.get('pricing', {}).get('price_tiers', {}).get('mid_range', 0):.2f}.",
                'premium': f"For premium quality, our products range up to ${self.product_knowledge.get('pricing', {}).get('price_tiers', {}).get('premium', 0):.2f}."
            }
        }
        
        # Order-related templates
        self.response_patterns['order_templates'] = {
            'status_info': f"Based on our data, {self.order_patterns.get('status_distribution', {}).get('shipped', 0)} orders are typically shipped, with an average of {self.order_patterns.get('order_sizes', {}).get('avg_items', 0):.1f} items per order.",
            'popular_products': "Our most popular products based on order data include: " + ", ".join(list(self.order_patterns.get('popular_products', {}).keys())[:3]) if self.order_patterns.get('popular_products') else "We have a variety of popular products available."
        }
        
        # Inventory templates
        self.response_patterns['inventory_templates'] = {
            'availability': f"Currently, {self.inventory_patterns.get('stock_analysis', {}).get('availability_rate', 0):.1f}% of our inventory is available for purchase.",
            'category_availability': "Our most available categories are: " + ", ".join(list(self.inventory_patterns.get('category_availability', {}).keys())[:3]) if self.inventory_patterns.get('category_availability') else "We have good availability across all categories."
        }
    
    def _generate_training_scenarios(self):
        """Generate realistic training scenarios based on the data"""
        logger.info("Generating training scenarios...")
        
        self.training_data['scenarios'] = []
        
        # Product inquiry scenarios
        for category in self.product_knowledge.get('categories', {}).keys():
            self.training_data['scenarios'].append({
                'type': 'product_inquiry',
                'user_input': f"I'm looking for {category}",
                'expected_response_type': 'product_info',
                'data_context': {
                    'category': category,
                    'count': self.product_knowledge['categories'][category]['count'],
                    'price_range': self.product_knowledge['categories'][category]['price_range']
                }
            })
        
        # Order status scenarios
        if 'orders' in self.data_service.dfs:
            sample_orders = self.data_service.dfs['orders'].head(3)
            for _, order in sample_orders.iterrows():
                self.training_data['scenarios'].append({
                    'type': 'order_status',
                    'user_input': f"What's the status of order #{order['order_id']}?",
                    'expected_response_type': 'order_info',
                    'data_context': {
                        'order_id': order['order_id'],
                        'status': order['status'],
                        'num_items': order['num_of_item']
                    }
                })
        
        # Inventory scenarios
        for category in self.inventory_patterns.get('category_availability', {}).keys():
            self.training_data['scenarios'].append({
                'type': 'inventory_inquiry',
                'user_input': f"How many {category} do you have in stock?",
                'expected_response_type': 'inventory_info',
                'data_context': {
                    'category': category,
                    'available': self.inventory_patterns['category_availability'][category]
                }
            })
    
    def get_enhanced_response(self, message: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Get enhanced response using trained knowledge"""
        message_lower = message.lower()
        
        # Product category detection
        for category in self.product_knowledge.get('categories', {}).keys():
            if category in message_lower:
                return {
                    'response_type': 'product_info',
                    'template': self.response_patterns.get('product_templates', {}).get('category_info', {}).get(category, f"We have great {category} available!"),
                    'data': self.product_knowledge['categories'][category],
                    'confidence': 0.9
                }
        
        # Price range detection
        if any(word in message_lower for word in ['cheap', 'budget', 'affordable']):
            return {
                'response_type': 'price_info',
                'template': self.response_patterns.get('product_templates', {}).get('price_info', {}).get('budget', "We have budget-friendly options available."),
                'data': self.product_knowledge.get('pricing', {}),
                'confidence': 0.8
            }
        
        # Order status detection
        order_match = re.search(r'order\s+(?:id\s+)?#?(\d+)', message_lower)
        if order_match:
            return {
                'response_type': 'order_status',
                'template': self.response_patterns.get('order_templates', {}).get('status_info', "I can help you check your order status."),
                'data': {'order_id': order_match.group(1)},
                'confidence': 0.95
            }
        
        # Inventory inquiry detection
        if any(word in message_lower for word in ['stock', 'available', 'inventory', 'left']):
            return {
                'response_type': 'inventory_info',
                'template': self.response_patterns.get('inventory_templates', {}).get('availability', "I can check our current inventory for you."),
                'data': self.inventory_patterns.get('stock_analysis', {}),
                'confidence': 0.85
            }
        
        return {
            'response_type': 'general',
            'template': "I'm here to help with your fashion needs!",
            'data': {},
            'confidence': 0.5
        }
    
    def get_training_summary(self) -> Dict[str, Any]:
        """Get a summary of the training results"""
        return {
            'product_knowledge': {
                'categories_analyzed': len(self.product_knowledge.get('categories', {})),
                'brands_analyzed': len(self.product_knowledge.get('brands', {})),
                'price_tiers': len(self.product_knowledge.get('pricing', {}).get('price_tiers', {}))
            },
            'order_patterns': {
                'status_types': len(self.order_patterns.get('status_distribution', {})),
                'popular_products': len(self.order_patterns.get('popular_products', {}))
            },
            'inventory_patterns': {
                'availability_rate': self.inventory_patterns.get('stock_analysis', {}).get('availability_rate', 0),
                'categories_available': len(self.inventory_patterns.get('category_availability', {}))
            },
            'user_preferences': {
                'total_users': self.user_preferences.get('demographics', {}).get('total_users', 0),
                'repeat_customers': self.user_preferences.get('order_patterns', {}).get('repeat_customers', 0)
            },
            'training_scenarios': len(self.training_data.get('scenarios', [])),
            'response_templates': len(self.response_patterns.get('product_templates', {}).get('category_info', {}))
        } 