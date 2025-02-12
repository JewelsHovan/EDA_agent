import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# OpenAI API configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MODEL_NAME = "gpt-4o"  # or any other OpenAI model you prefer

# Agent configuration
MAX_STEPS = 25
PLANNING_INTERVAL = 3

# Visualization settings
PLOT_STYLE = "default"
FIGURE_SIZE = (12, 8)
DPI = 150
