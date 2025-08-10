#!/usr/bin/env python3
"""
Test script to verify the SMS-Slack Bridge setup
"""

import sys
import os

def test_python_version():
    """Test if Python version is compatible"""
    print("🐍 Testing Python version...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 7:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} is compatible")
        return True
    else:
        print(f"❌ Python {version.major}.{version.minor}.{version.micro} is not compatible. Need 3.7+")
        return False

def test_dependencies():
    """Test if required packages can be imported"""
    print("\n📦 Testing dependencies...")
    
    try:
        import flask
        print(f"✅ Flask {flask.__version__}")
    except ImportError:
        print("❌ Flask not installed")
        return False
    
    try:
        import twilio
        print(f"✅ Twilio {twilio.__version__}")
    except ImportError:
        print("❌ Twilio not installed")
        return False
    
    try:
        import slack_sdk
        print(f"✅ Slack SDK {slack_sdk.__version__}")
    except ImportError:
        print("❌ Slack SDK not installed")
        return False
    
    try:
        import dotenv
        print(f"✅ python-dotenv {dotenv.__version__}")
    except ImportError:
        print("❌ python-dotenv not installed")
        return False
    
    return True

def test_environment():
    """Test environment variables"""
    print("\n🔑 Testing environment variables...")
    
    required_vars = [
        "TWILIO_ACCOUNT_SID",
        "TWILIO_AUTH_TOKEN", 
        "TWILIO_NUMBER",
        "SLACK_BOT_TOKEN",
        "SLACK_SIGNING_SECRET"
    ]
    
    missing_vars = []
    for var in required_vars:
        if os.getenv(var):
            print(f"✅ {var} is set")
        else:
            print(f"❌ {var} is not set")
            missing_vars.append(var)
    
    if missing_vars:
        print(f"\n⚠️  Missing environment variables: {', '.join(missing_vars)}")
        print("Please copy env_template.txt to .env and fill in your credentials")
        return False
    
    return True

def test_flask_app():
    """Test if Flask app can be created"""
    print("\n🚀 Testing Flask app creation...")
    
    try:
        from main import app
        print("✅ Flask app created successfully")
        print(f"✅ App name: {app.name}")
        return True
    except Exception as e:
        print(f"❌ Failed to create Flask app: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 SMS-Slack Bridge Setup Test")
    print("=" * 40)
    
    tests = [
        test_python_version,
        test_dependencies,
        test_environment,
        test_flask_app
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print("\n" + "=" * 40)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Your setup is ready.")
        print("\nNext steps:")
        print("1. Start the Flask app: python main.py")
        print("2. Start ngrok: ngrok http 5000")
        print("3. Update Twilio and Slack webhook URLs")
    else:
        print("⚠️  Some tests failed. Please fix the issues above.")
        sys.exit(1)

if __name__ == "__main__":
    main()
