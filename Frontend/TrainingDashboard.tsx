import React, { useState, useEffect } from 'react';
import { 
  Brain, 
  BarChart3, 
  TrendingUp, 
  RefreshCw, 
  CheckCircle, 
  AlertCircle,
  Users,
  Package,
  ShoppingCart,
  Database,
  Activity,
  Zap
} from 'lucide-react';
import { api } from '../services/api';

interface TrainingStatus {
  status: string;
  summary: {
    product_knowledge: {
      categories_analyzed: number;
      brands_analyzed: number;
      price_tiers: number;
    };
    order_patterns: {
      status_types: number;
      popular_products: number;
    };
    inventory_patterns: {
      availability_rate: number;
      categories_available: number;
    };
    user_preferences: {
      total_users: number;
      repeat_customers: number;
    };
    training_scenarios: number;
    response_templates: number;
  };
  message: string;
}

interface TrainingAnalytics {
  product_analytics: any;
  order_analytics: any;
  inventory_analytics: any;
  user_analytics: any;
}

interface TrainingTest {
  input_message: string;
  enhanced_response: any;
  regular_response: any;
  comparison: any;
}

const TrainingDashboard: React.FC = () => {
  const [trainingStatus, setTrainingStatus] = useState<TrainingStatus | null>(null);
  const [analytics, setAnalytics] = useState<TrainingAnalytics | null>(null);
  const [testMessage, setTestMessage] = useState('');
  const [testResult, setTestResult] = useState<TrainingTest | null>(null);
  const [loading, setLoading] = useState(false);
  const [retraining, setRetraining] = useState(false);

  useEffect(() => {
    loadTrainingStatus();
    loadAnalytics();
  }, []);

  const loadTrainingStatus = async () => {
    try {
      setLoading(true);
      const response = await api.getTrainingStatus();
      setTrainingStatus(response);
    } catch (error) {
      console.error('Error loading training status:', error);
    } finally {
      setLoading(false);
    }
  };

  const loadAnalytics = async () => {
    try {
      const response = await api.getTrainingAnalytics();
      setAnalytics(response);
    } catch (error) {
      console.error('Error loading analytics:', error);
    }
  };

  const handleRetrain = async () => {
    try {
      setRetraining(true);
      await api.retrainChatbot();
      await loadTrainingStatus();
      await loadAnalytics();
    } catch (error) {
      console.error('Error retraining:', error);
    } finally {
      setRetraining(false);
    }
  };

  const handleTestMessage = async () => {
    if (!testMessage.trim()) return;
    
    try {
      setLoading(true);
      const response = await api.testTrainingResponse(testMessage);
      setTestResult(response);
    } catch (error) {
      console.error('Error testing message:', error);
    } finally {
      setLoading(false);
    }
  };

  const StatCard: React.FC<{ title: string; value: string | number; icon: React.ReactNode; color: string }> = ({ 
    title, value, icon, color 
  }) => (
    <div className={`bg-white rounded-lg p-6 shadow-sm border-l-4 ${color}`}>
      <div className="flex items-center justify-between">
        <div>
          <p className="text-sm font-medium text-gray-600">{title}</p>
          <p className="text-2xl font-bold text-gray-900">{value}</p>
        </div>
        <div className="text-gray-400">
          {icon}
        </div>
      </div>
    </div>
  );

  const MetricCard: React.FC<{ title: string; data: any; icon: React.ReactNode }> = ({ 
    title, data, icon 
  }) => (
    <div className="bg-white rounded-lg p-6 shadow-sm">
      <div className="flex items-center mb-4">
        <div className="text-blue-500 mr-3">
          {icon}
        </div>
        <h3 className="text-lg font-semibold text-gray-900">{title}</h3>
      </div>
      <div className="space-y-2">
        {Object.entries(data).map(([key, value]) => (
          <div key={key} className="flex justify-between">
            <span className="text-sm text-gray-600 capitalize">
              {key.replace(/_/g, ' ')}:
            </span>
            <span className="text-sm font-medium text-gray-900">
              {typeof value === 'number' ? value.toLocaleString() : String(value)}
            </span>
          </div>
        ))}
      </div>
    </div>
  );

  if (loading && !trainingStatus) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500"></div>
      </div>
    );
  }

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="mb-8">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">Training Dashboard</h1>
            <p className="text-gray-600 mt-2">Monitor and manage your chatbot's training status</p>
          </div>
          <button
            onClick={handleRetrain}
            disabled={retraining}
            className="flex items-center px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50"
          >
            {retraining ? (
              <RefreshCw className="w-4 h-4 mr-2 animate-spin" />
            ) : (
              <RefreshCw className="w-4 h-4 mr-2" />
            )}
            {retraining ? 'Retraining...' : 'Retrain Chatbot'}
          </button>
        </div>
      </div>

      {/* Training Status */}
      {trainingStatus && (
        <div className="mb-8">
          <div className="flex items-center mb-4">
            <CheckCircle className="w-6 h-6 text-green-500 mr-2" />
            <h2 className="text-xl font-semibold text-gray-900">Training Status</h2>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            <StatCard
              title="Categories Analyzed"
              value={trainingStatus.summary.product_knowledge.categories_analyzed}
              icon={<Package className="w-6 h-6" />}
              color="border-blue-500"
            />
            <StatCard
              title="Brands Analyzed"
              value={trainingStatus.summary.product_knowledge.brands_analyzed}
              icon={<TrendingUp className="w-6 h-6" />}
              color="border-green-500"
            />
            <StatCard
              title="Training Scenarios"
              value={trainingStatus.summary.training_scenarios}
              icon={<Brain className="w-6 h-6" />}
              color="border-purple-500"
            />
            <StatCard
              title="Response Templates"
              value={trainingStatus.summary.response_templates}
              icon={<Zap className="w-6 h-6" />}
              color="border-yellow-500"
            />
          </div>
        </div>
      )}

      {/* Analytics */}
      {analytics && (
        <div className="mb-8">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">Training Analytics</h2>
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <MetricCard
              title="Product Analytics"
              data={analytics.product_analytics}
              icon={<Package className="w-5 h-5" />}
            />
            <MetricCard
              title="Order Analytics"
              data={analytics.order_analytics}
              icon={<ShoppingCart className="w-5 h-5" />}
            />
            <MetricCard
              title="Inventory Analytics"
              data={analytics.inventory_analytics}
              icon={<Database className="w-5 h-5" />}
            />
            <MetricCard
              title="User Analytics"
              data={analytics.user_analytics}
              icon={<Users className="w-5 h-5" />}
            />
          </div>
        </div>
      )}

      {/* Test Training */}
      <div className="bg-white rounded-lg shadow-sm p-6">
        <h2 className="text-xl font-semibold text-gray-900 mb-4">Test Training Response</h2>
        <div className="flex gap-4 mb-4">
          <input
            type="text"
            value={testMessage}
            onChange={(e) => setTestMessage(e.target.value)}
            placeholder="Enter a test message..."
            className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          />
          <button
            onClick={handleTestMessage}
            disabled={!testMessage.trim() || loading}
            className="px-6 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 disabled:opacity-50"
          >
            Test
          </button>
        </div>

        {testResult && (
          <div className="space-y-4">
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
              <div className="bg-gray-50 rounded-lg p-4">
                <h3 className="font-semibold text-gray-900 mb-2">Enhanced Response</h3>
                <p className="text-sm text-gray-600 mb-2">
                  Confidence: {(testResult.enhanced_response.confidence * 100).toFixed(1)}%
                </p>
                <p className="text-gray-800">{testResult.enhanced_response.template}</p>
              </div>
              <div className="bg-gray-50 rounded-lg p-4">
                <h3 className="font-semibold text-gray-900 mb-2">Regular Response</h3>
                <p className="text-sm text-gray-600 mb-2">
                  Confidence: {(testResult.regular_response.confidence * 100).toFixed(1)}%
                </p>
                <p className="text-gray-800">{testResult.regular_response.message}</p>
              </div>
            </div>
            
            <div className="bg-blue-50 rounded-lg p-4">
              <h3 className="font-semibold text-gray-900 mb-2">Improvement Analysis</h3>
              <div className="grid grid-cols-3 gap-4 text-sm">
                <div>
                  <span className="text-gray-600">Enhanced Confidence:</span>
                  <span className="ml-2 font-medium">
                    {(testResult.comparison.enhanced_confidence * 100).toFixed(1)}%
                  </span>
                </div>
                <div>
                  <span className="text-gray-600">Regular Confidence:</span>
                  <span className="ml-2 font-medium">
                    {(testResult.comparison.regular_confidence * 100).toFixed(1)}%
                  </span>
                </div>
                <div>
                  <span className="text-gray-600">Improvement:</span>
                  <span className={`ml-2 font-medium ${
                    testResult.comparison.improvement > 0 ? 'text-green-600' : 'text-red-600'
                  }`}>
                    {(testResult.comparison.improvement * 100).toFixed(1)}%
                  </span>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default TrainingDashboard; 