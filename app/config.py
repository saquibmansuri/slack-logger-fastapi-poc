from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    slack_token: str
    slack_channel: str
    rate_limit_max_messages: int = 10
    rate_limit_period_minutes: int = 10

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False
        env_prefix = ""
        extra = "ignore"
        
        # Map environment variables to settings fields
        field_mapping = {
            "slack_token": "SLACK_TOKEN",
            "slack_channel": "SLACK_CHANNEL",
            "rate_limit_max_messages": "RATE_LIMIT_MAX_MESSAGES",
            "rate_limit_period_minutes": "RATE_LIMIT_PERIOD_MINUTES",
        }

settings = Settings() 