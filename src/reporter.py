import json
import os
from datetime import datetime

class ReportGenerator:
    def __init__(self, output_dir="reports"):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def generate_json(self, alert_data):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filepath = os.path.join(self.output_dir, f"report_{timestamp}.json")
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(alert_data, f, indent=4)
        return filepath

    def generate_html(self, alert_data):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        filename = f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
        filepath = os.path.join(self.output_dir, filename)

        cards = ""
        for item in alert_data:
            insights_html = item['insight'].replace('\n', '<br>')
            cards += f"""
            <div class="card">
                <div class="card-header">
                    <span class="badge threat">{item['threat']}</span>
                    <span class="ip">Attacker IP: {item['ip']}</span>
                </div>
                <div class="card-body">
                    <p><strong>Target URL:</strong> <code>{item['url']}</code></p>
                    <div class="ai-box">
                        <h4>🤖 SOC Analyst Insight (AI)</h4>
                        <p>{insights_html}</p>
                    </div>
                </div>
            </div>
            """

        html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>LogMind AI - Security Incident Report</title>
    <style>
        body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #0f172a; color: #f8fafc; margin: 0; padding: 20px; }}
        .container {{ max-width: 900px; margin: 0 auto; }}
        h1 {{ color: #38bdf8; text-align: center; border-bottom: 2px solid #334155; padding-bottom: 10px; }}
        .meta {{ text-align: center; color: #94a3b8; font-size: 0.9em; margin-bottom: 30px; }}
        .card {{ background: #1e293b; border-radius: 8px; border: 1px solid #334155; margin-bottom: 20px; padding: 20px; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1); }}
        .card-header {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px; border-bottom: 1px solid #334155; padding-bottom: 10px; }}
        .badge {{ background: #ef4444; color: white; padding: 4px 12px; border-radius: 20px; font-weight: bold; font-size: 0.85em; }}
        .ip {{ color: #cbd5e1; font-family: monospace; font-size: 1.1em; }}
        code {{ background: #0f172a; padding: 4px 8px; border-radius: 4px; color: #f43f5e; font-family: monospace; }}
        .ai-box {{ background: #0f172a; border-left: 4px solid #38bdf8; padding: 15px; margin-top: 15px; border-radius: 0 8px 8px 0; }}
        .ai-box h4 {{ margin: 0 0 10px 0; color: #38bdf8; }}
        .ai-box p {{ margin: 0; font-size: 0.95em; line-height: 1.6; color: #e2e8f0; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>LogMind AI - Security Report</h1>
        <div class="meta">Generated on: {timestamp} | Total Alerts: {len(alert_data)}</div>
        {cards}
    </div>
</body>
</html>"""

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(html_content)
        return filepath