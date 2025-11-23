import os
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not SUPABASE_URL:
    print("Warning: SUPABASE_URL is not set.")
if not SUPABASE_KEY:
    print("Warning: SUPABASE_KEY is not set.")
if not GEMINI_API_KEY:
    print("Warning: GEMINI_API_KEY is not set.")
