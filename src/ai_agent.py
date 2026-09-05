import os
import groq

class AIAgent:
    def __init__(self):
        # Initialize Groq client
        api_key = os.getenv("GROQ_API_KEY")
        self.client = groq.Groq(api_key=api_key) if api_key else None

    def analyze_threat(self, ip: str, url: str, threats: list):
        if not self.client:
            return "AI Analysis skipped: GROQ_API_KEY missing."

        prompt = f"Analyze this security threat: IP {ip}, URL {url}, Threats: {threats}. Provide a 2-sentence summary and mitigation step."
        
        try:
            response = self.client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model="llama-3.3-70b-versatile"
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"AI Analysis failed: {str(e)}"