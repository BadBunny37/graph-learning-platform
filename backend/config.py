import os
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

if not SUPABASE_URL:
    print("Warning: SUPABASE_URL is not set.")
if not SUPABASE_KEY:
    print("Warning: SUPABASE_KEY is not set.")
if not OPENROUTER_API_KEY:
    print("Warning: OPENROUTER_API_KEY is not set.")
