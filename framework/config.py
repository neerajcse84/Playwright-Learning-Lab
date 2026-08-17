import os

BASE_URL = os.getenv(
    "BASE_URL",
    "http://127.0.0.1:5000"
)
BUILD_NUMBER = os.getenv("BUILD_NUMBER", "LOCAL")