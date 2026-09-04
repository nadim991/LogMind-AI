import os
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq

env_path = Path(__file__).resolve().parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

class SOCAiAgent:
    def __init__(self):
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY is missing in .env file")
        self.client = Groq(api_key=api_key)

    def analyze_threat(self, ip, url, threat_types):
        prompt = f"""
You are a Senior SOC Analyst reviewing an automated security log alert.
Log Info:
- Source IP: {ip}
- Target URI: {url}
- Detected Attacks: {', '.join(threat_types)}

Provide a concise security breakdown with exactly 3 bullet points:
1. **Severity & Impact**: Explain the operational risk.
2. **MITRE ATT&CK Mapping**: Specify Technique ID and Name.
3. **Mitigation Action**: Immediate SOC response recommendation.

Be concise, technical, and direct.
"""
        try:
            response = self.client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model="openai/gpt-oss-20b",
                temperature=0.2,
                max_tokens=500
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"AI Analysis Unavailable: {str(e)}"