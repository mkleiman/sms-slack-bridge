#!/bin/bash

echo "🚀 Starting SMS-Slack Bridge..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found. Please run ./deploy.sh first."
    exit 1
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "❌ .env file not found. Please copy env_template.txt to .env and fill in your credentials."
    exit 1
fi

# Load environment variables (skip comments and empty lines)
echo "📋 Loading environment variables..."
set -a
source .env
set +a

# Start the Flask application
echo "🌐 Starting Flask application on http://localhost:5001"
echo "📱 SMS endpoint: http://localhost:5001/incoming/sms"
echo "💬 Slack endpoint: http://localhost:5001/incoming/slack"
echo ""
echo "Press Ctrl+C to stop the application"
echo ""

python main.py
