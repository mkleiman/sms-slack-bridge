#!/bin/bash

echo "🚀 SMS-Slack Bridge Deployment Script"
echo "====================================="

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.7+ first."
    exit 1
fi

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 is not installed. Please install pip first."
    exit 1
fi

echo "✅ Python and pip are available"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📚 Installing dependencies..."
pip install -r requirements.txt

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "⚠️  .env file not found!"
    echo "📝 Please copy env_template.txt to .env and fill in your credentials:"
    echo "   cp env_template.txt .env"
    echo "   Then edit .env with your Twilio and Slack credentials"
    echo ""
    echo "🔑 Required credentials:"
    echo "   - TWILIO_ACCOUNT_SID"
    echo "   - TWILIO_AUTH_TOKEN"
    echo "   - TWILIO_NUMBER"
    echo "   - SLACK_BOT_TOKEN"
    echo "   - SLACK_SIGNING_SECRET"
    echo ""
    echo "After setting up .env, run this script again."
    exit 1
fi

echo "✅ Environment file found"

# Check if ngrok is available
if ! command -v ngrok &> /dev/null; then
    echo "⚠️  ngrok is not installed. For development, please install ngrok:"
    echo "   https://ngrok.com/download"
    echo ""
    echo "For production deployment, you can skip this step."
fi

echo ""
echo "🎉 Setup complete! You can now:"
echo ""
echo "1. Start the Flask app:"
echo "   source venv/bin/activate"
echo "   python main.py"
echo ""
echo "2. In another terminal, start ngrok (for development):"
echo "   ngrok http 5000"
echo ""
echo "3. Update your Twilio and Slack webhook URLs with the ngrok URL"
echo ""
echo "📖 See README.md for detailed setup instructions"
