from dotenv import load_dotenv
import os

load_dotenv()  # loads .env into environment

def get_env_variable(var_name: str) -> str:
    """Get environment variable and raise error if not set."""
    value = os.getenv(var_name)
    if not value:
        raise ValueError(f"{var_name} is not set in the environment")
    return value

IMAP_HOST = get_env_variable("IMAP_HOST")
IMAP_PORT = get_env_variable("IMAP_PORT")
SMTP_HOST = get_env_variable("SMTP_HOST")
SMTP_PORT = get_env_variable("SMTP_PORT")
EMAIL_USER = get_env_variable("EMAIL_USER")
EMAIL_PASS = get_env_variable("EMAIL_PASS")
DB_URL = get_env_variable("DB_URL")
