# Exception Logger API

A FastAPI application that logs exceptions to Slack with rate limiting.

## Features

- Custom Python logging handler that sends exceptions to Slack
- Rate limiting to prevent flooding Slack channels (max 10 messages per 10 minutes by default)
- Docker and Docker Compose support for easy deployment
- Demo endpoints to test exception logging

## Setup

1. Clone this repository
2. Create a `.env` file with your Slack credentials:

```
SLACK_TOKEN=your_slack_token_here
SLACK_CHANNEL=your_slack_channel_here
RATE_LIMIT_MAX_MESSAGES=10
RATE_LIMIT_PERIOD_MINUTES=10
```

### Detailed Steps for Creating a Slack App and Getting a Token

1. Go to https://api.slack.com/apps
2. Click "Create New App"
3. Choose "From scratch"
4. Enter a name for your app (e.g., "Exception Logger")
5. Select the workspace where you want to install the app
6. Click "Create App"

#### Adding Required Permissions:

1. In the left sidebar, click on "OAuth & Permissions"
2. Scroll down to "Scopes" section
3. Under "Bot Token Scopes", click "Add an OAuth Scope"
4. Add the `chat:write` permission (this allows the app to send messages)
5. You may also want to add `chat:write.public` if you need to post to public channels without being invited
6. You may also need these `channels:read` to view basic information about public channels in a workspace
7. You may also need these `groups:read` to view basic information about private channels that this app has been added to
8. You may also need these `im:read` to view basic information about direct messages that this app has been added to
9. You may also need these `mpim:read` to view basic information about group direct messages that TestApp has been added to

#### Installing the App to Your Workspace:

1. Scroll up to the "OAuth Tokens for Your Workspace" section
2. Click "Install to Workspace"
3. Review the permissions and click "Allow"
4. Copy the "Bot User OAuth Token" (it starts with `xoxb-`)
5. Add this token to your `.env` file as `SLACK_TOKEN`

#### Setting Up the Channel:

1. Create a new channel in Slack or use an existing one for logging

##### For Private Channels:

1. You **must** invite the bot to your private channel:

   - Open the private channel in Slack
   - Click on the channel name at the top to open the channel details
   - Click "Integrations" tab
   - Click "Add apps"
   - Find and select your bot (the name you gave it when creating the app)
   - The bot must be added to the channel before it can post messages there

2. Get the channel ID:

   - Right-click on the channel name in the sidebar
   - Select "Copy link"
   - The channel ID is the last part of the URL (after the last `/`)
   - Example: In `https://workspace.slack.com/archives/C12345ABCDE`, the ID is `C12345ABCDE`

3. Use this channel ID in your `.env` file:
   ```
   SLACK_CHANNEL=C12345ABCDE
   ```
   - For private channels, you must use the channel ID, not the channel name

##### For Public Channels:

1. You can use either the channel ID (as described above) or the channel name (e.g., `#exceptions`)
2. Add this to your `.env` file as `SLACK_CHANNEL`

## Running Locally

```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
uvicorn app.main:app --reload
```

## Running with Docker

```bash
# Build and start the container
docker-compose up -d

# View logs
docker-compose logs -f
```

## Testing the Application

Once the application is running (either locally or with Docker), you can test it using any of the following methods:

### Using the Swagger UI

1. Open your browser and navigate to http://localhost:8000/docs
2. You'll see the interactive API documentation
3. Test the endpoints by clicking on them and then clicking the "Try it out" button:
   - `/demo/` - A simple endpoint that returns a welcome message
   - `/demo/error` - Triggers a division by zero error (will send a message to Slack)
   - `/demo/warning` - Logs a warning message (won't send to Slack as it's not an error)
   - `/demo/custom-error` - Logs a custom error message (will send to Slack)

### Using cURL

Test the error endpoint (this will trigger a Slack notification):

```bash
curl -X GET "http://localhost:8000/demo/error"
```

Test the custom error endpoint:

```bash
curl -X GET "http://localhost:8000/demo/custom-error?message=Test%20error%20message"
```

### Verifying Slack Integration

After triggering an error:

1. Check your configured Slack channel
2. You should see an error message with details about the exception
3. The rate limiting will ensure that no more than 10 messages are sent in a 10-minute period

### Troubleshooting

If you don't see messages in Slack:

1. Check that your `.env` file has the correct `SLACK_TOKEN` and `SLACK_CHANNEL`
2. Verify that the bot has been added to the channel (especially important for private channels)
3. Check the application logs for any errors:
   ```bash
   docker-compose logs -f
   ```

## API Endpoints

- `GET /` - Root endpoint
- `GET /demo/` - Demo endpoint
- `GET /demo/error` - Triggers a division by zero error
- `GET /demo/warning` - Logs a warning message
- `GET /demo/custom-error` - Logs a custom error message

## Documentation

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
