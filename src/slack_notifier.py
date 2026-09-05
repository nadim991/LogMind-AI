import os
import requests

class SlackNotifier:
    def __init__(self):
        self.webhook_url = os.getenv("SLACK_WEBHOOK_URL")

    def send_threat_alert(self, ip, url, threat_type, insight_text):
        if not self.webhook_url:
            print("[!] Slack Webhook URL not set. Skipping notification.")
            return

        # insight_text স্ট্রিংয়ে রূপান্তর নিশ্চিত করা
        formatted_insight = str(insight_text) if insight_text else "Suspicious activity detected."

        payload = {
            "text": "🚨 *LogMind AI - Security Threat Alert!*",
            "attachments": [
                {
                    "color": "#ef4444",
                    "fields": [
                        {"title": "Attacker IP", "value": ip, "short": True},
                        {"title": "Threat Type", "value": threat_type, "short": True},
                        {"title": "Target Endpoint", "value": f"`{url}`", "short": False},
                        {"title": "AI SOC Analyst Insight", "value": formatted_insight, "short": False}
                    ]
                }
            ]
        }

        try:
            response = requests.post(self.webhook_url, json=payload)
            return response.status_code == 200
        except Exception as e:
            print(f"[X] Failed to send Slack alert: {e}")
            return False