import React from 'react';
import { MessageCircle, ShoppingBag, Heart, Brain } from 'lucide-react';
import { Link } from 'react-router-dom';

const Header: React.FC = () => {
  return (
    <header className="bg-white shadow-sm border-b">
      <div className="container mx-auto px-4">
        <div className="flex items-center justify-between h-16">
          {/* Logo */}
          <div className="flex items-center space-x-2">
            <div className="w-8 h-8 bg-gradient-to-r from-primary-500 to-secondary-500 rounded-lg flex items-center justify-center">
              <MessageCircle className="w-5 h-5 text-white" />
            </div>
            <h1 className="text-xl font-bold text-gray-900">StyleBot</h1>
            <span className="text-sm text-gray-500">Fashion Assistant</span>
          </div>

          {/* Navigation */}
          <nav className="hidden md:flex items-center space-x-8">
            <Link to="/" className="text-gray-600 hover:text-primary-600 transition-colors">
              Chat
            </Link>
            <Link to="/training" className="text-gray-600 hover:text-primary-600 transition-colors flex items-center">
              <Brain className="w-4 h-4 mr-1" />
              Training
            </Link>
            <a href="#" className="text-gray-600 hover:text-primary-600 transition-colors">
              Products
            </a>
            <a href="#" className="text-gray-600 hover:text-primary-600 transition-colors">
              Orders
            </a>
            <a href="#" className="text-gray-600 hover:text-primary-600 transition-colors">
              Support
            </a>
          </nav>

          {/* Actions */}
          <div className="flex items-center space-x-4">
            <button className="p-2 text-gray-600 hover:text-primary-600 transition-colors">
              <Heart className="w-5 h-5" />
            </button>
            <button className="p-2 text-gray-600 hover:text-primary-600 transition-colors">
              <ShoppingBag className="w-5 h-5" />
            </button>
            <button className="bg-primary-600 text-white px-4 py-2 rounded-lg hover:bg-primary-700 transition-colors">
              Start Chat
            </button>
          </div>
        </div>
      </div>
    </header>
  );
};

export default Header; 