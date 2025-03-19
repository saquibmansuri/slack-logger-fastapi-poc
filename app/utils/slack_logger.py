import logging
import time
from typing import Dict, List, Optional
import traceback
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

from app.config import settings

class RateLimitedSlackHandler(logging.Handler):
    """
    A custom logging handler that sends log messages to Slack with rate limiting.
    
    This handler will only send a maximum number of messages within a specified time period.
    """
    
    def __init__(
        self,
        slack_token: str,
        channel: str,
        max_messages: int = 10,
        period_minutes: int = 10,
        level: int = logging.ERROR
    ):
        """
        Initialize the handler with Slack credentials and rate limiting parameters.
        
        Args:
            slack_token: The Slack API token
            channel: The Slack channel to send messages to
            max_messages: Maximum number of messages to send in the period
            period_minutes: Time period in minutes for rate limiting
            level: The logging level for this handler
        """
        super().__init__(level)
        self.slack_client = WebClient(token=slack_token)
        self.channel = channel
        self.max_messages = max_messages
        self.period_seconds = period_minutes * 60
        
        # Rate limiting state
        self.message_timestamps: List[float] = []
        self.message_count = 0
        self.rate_limit_notification_sent = False
        
        # Formatter for log messages
        self.setFormatter(
            logging.Formatter('%(levelname)s - %(name)s - %(message)s')
        )
    
    def emit(self, record: logging.LogRecord) -> None:
        """
        Emit a log record to Slack, respecting rate limits.
        
        Args:
            record: The log record to emit
        """
        # Check if we should send this message based on rate limits
        current_time = time.time()
        
        # Remove timestamps older than our period
        self.message_timestamps = [
            ts for ts in self.message_timestamps 
            if current_time - ts <= self.period_seconds
        ]
        
        # If we've hit the rate limit, send notification and don't send the message
        if len(self.message_timestamps) >= self.max_messages:
            # Only send rate limit notification once per period
            if not self.rate_limit_notification_sent:
                try:
                    self.slack_client.chat_postMessage(
                        channel=self.channel,
                        text=f"⚠️ *RATE LIMIT REACHED*: Maximum of {self.max_messages} messages per {self.period_seconds // 60} minutes exceeded. Some log messages will be suppressed until {self.period_seconds // 60} minutes have passed since the first message.",
                        unfurl_links=False,
                        unfurl_media=False
                    )
                    self.rate_limit_notification_sent = True
                except Exception as e:
                    print(f"Error sending rate limit notification to Slack: {str(e)}")
            return
        
        # Add current timestamp to our list
        self.message_timestamps.append(current_time)
        
        # Reset the notification flag if we're under the limit again
        if self.rate_limit_notification_sent:
            self.rate_limit_notification_sent = False
        
        try:
            # Format the log message
            message = self.format(record)
            
            # Add exception info if available
            if record.exc_info:
                message += "\n\n```\n"
                message += "".join(traceback.format_exception(*record.exc_info))
                message += "\n```"
            
            # Send to Slack
            self.slack_client.chat_postMessage(
                channel=self.channel,
                text=message,
                unfurl_links=False,
                unfurl_media=False
            )
        except SlackApiError as e:
            # Don't use logging here to avoid potential infinite recursion
            print(f"Error sending message to Slack: {e.response['error']}")
        except Exception as e:
            print(f"Unexpected error in SlackHandler: {str(e)}")

def setup_logger(name: str = "app") -> logging.Logger:
    """
    Set up and configure a logger with the Slack handler.
    
    Args:
        name: The name for the logger
        
    Returns:
        A configured logger instance
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    
    # Add console handler for all logs
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)
    
    # Add Slack handler for ERROR and above
    slack_handler = RateLimitedSlackHandler(
        slack_token=settings.slack_token,
        channel=settings.slack_channel,
        max_messages=settings.rate_limit_max_messages,
        period_minutes=settings.rate_limit_period_minutes,
        level=logging.ERROR
    )
    logger.addHandler(slack_handler)
    
    return logger 