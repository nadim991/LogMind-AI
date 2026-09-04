import os
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq

env_path = Path(__file__).resolve().parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

key = os.getenv("GROQ_API_KEY")
if not key:
    print("GROQ_API_KEY Missing!")
else:
    client = Groq(api_key=key)
    try:
        models = client.models.list()
        print("Available Groq Models for your Key:")
        for m in models.data:
            print(f" - {m.id}")
    except Exception as e:
        print("Error fetching models:", e)