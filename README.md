# SMS-Slack Bridge

A Python Flask application that bridges SMS messages (via Twilio) with Slack conversations.

## Features

- Receive SMS messages via Twilio webhooks
- Post SMS messages to Slack channels
- Reply to Slack messages via SMS
- Thread-based conversation tracking

## Local Development

### Prerequisites

- Python 3.11+
- Twilio account and credentials
- Slack workspace with bot token
- ngrok (for local webhook testing)

### Setup

1. **Clone and setup:**
   ```bash
   git clone <your-repo-url>
   cd sms-slack-bridge
   ./deploy.sh
   ```

2. **Configure environment variables:**
   ```bash
   cp env_template.txt .env
   # Edit .env with your credentials
   ```

3. **Start the application:**
   ```bash
   ./start.sh
   ```

4. **Test with ngrok:**
   ```bash
   ngrok http 5001
   ```

## Cloud Deployment

### Option 1: Render (Recommended - Free)

1. **Push to GitHub:**
   ```bash
   git add .
   git commit -m "Initial commit"
   git push origin main
   ```

2. **Deploy on Render:**
   - Go to [render.com](https://render.com)
   - Connect your GitHub account
   - Create new Web Service
   - Select your repository
   - Set environment variables in Render dashboard
   - Deploy!

3. **Update webhooks:**
   - Update Twilio webhook URL to your Render URL
   - Update Slack webhook URL to your Render URL

### Option 2: Railway

1. **Deploy on Railway:**
   - Go to [railway.app](https://railway.app)
   - Connect GitHub and deploy
   - Set environment variables
   - Get your public URL

### Option 3: Heroku

1. **Install Heroku CLI:**
   ```bash
   brew install heroku/brew/heroku
   ```

2. **Deploy:**
   ```bash
   heroku create your-app-name
   git push heroku main
   heroku config:set TWILIO_ACCOUNT_SID=your_sid
   # Set other environment variables
   ```

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `TWILIO_ACCOUNT_SID` | Your Twilio Account SID | Yes |
| `TWILIO_AUTH_TOKEN` | Your Twilio Auth Token | Yes |
| `TWILIO_NUMBER` | Your Twilio phone number | Yes |
| `SLACK_BOT_TOKEN` | Your Slack bot token | Yes |
| `SLACK_SIGNING_SECRET` | Your Slack signing secret | Yes |
| `PORT` | Port to run on (set by cloud platform) | No |
| `FLASK_DEBUG` | Enable debug mode (False for production) | No |

## API Endpoints

- `POST /incoming/twilio` - Receive SMS from Twilio
- `POST /incoming/slack` - Receive Slack events

## Troubleshooting

### SSL Certificate Issues
- **Local**: Use ngrok for HTTPS
- **Cloud**: Most platforms provide HTTPS automatically

### Port Issues
- **Local**: Default port 5001
- **Cloud**: Use `PORT` environment variable

### Environment Variables
- Ensure all required variables are set
- Check for typos in variable names
- Restart app after changing variables

## Support

For issues:
1. Check the logs in your cloud platform
2. Verify environment variables
3. Test endpoints locally first
4. Check Twilio and Slack webhook configurations
