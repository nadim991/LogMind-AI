import json
import os
from datetime import datetime
from xhtml2pdf import pisa

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

    def _get_html_content(self, alert_data, timestamp):
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
                        <h4>SOC Analyst Insight (AI)</h4>
                        <p>{insights_html}</p>
                    </div>
                </div>
            </div>
            """

        return f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body {{ font-family: Helvetica, Arial, sans-serif; background: #ffffff; color: #1e293b; padding: 10px; }}
        h1 {{ color: #0284c7; text-align: center; border-bottom: 2px solid #cbd5e1; padding-bottom: 5px; font-size: 20px; }}
        .meta {{ text-align: center; color: #64748b; font-size: 11px; margin-bottom: 20px; }}
        .card {{ background: #f8fafc; border: 1px solid #cbd5e1; margin-bottom: 15px; padding: 12px; border-radius: 4px; }}
        .card-header {{ margin-bottom: 8px; border-bottom: 1px solid #e2e8f0; padding-bottom: 5px; }}
        .badge {{ background: #dc2626; color: white; padding: 3px 8px; font-weight: bold; font-size: 10px; border-radius: 3px; }}
        .ip {{ color: #334155; font-family: monospace; font-size: 12px; float: right; }}
        code {{ background: #f1f5f9; padding: 2px 4px; color: #be123c; font-family: monospace; font-size: 11px; }}
        .ai-box {{ background: #f0f9ff; border-left: 3px solid #0284c7; padding: 8px; margin-top: 10px; }}
        .ai-box h4 {{ margin: 0 0 5px 0; color: #0369a1; font-size: 12px; }}
        .ai-box p {{ margin: 0; font-size: 10px; line-height: 1.4; color: #334155; }}
    </style>
</head>
<body>
    <h1>LogMind AI - Security Incident Report</h1>
    <div class="meta">Generated on: {timestamp} | Total Alerts: {len(alert_data)}</div>
    {cards}
</body>
</html>"""

    def generate_html(self, alert_data):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        filename = f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
        filepath = os.path.join(self.output_dir, filename)
        
        html_content = self._get_html_content(alert_data, timestamp)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(html_content)
        return filepath

    def generate_pdf(self, alert_data):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        filename = f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        filepath = os.path.join(self.output_dir, filename)

        html_content = self._get_html_content(alert_data, timestamp)
        
        with open(filepath, "wb") as pdf_file:
            pisa_status = pisa.CreatePDF(html_content, dest=pdf_file)

        return filepath if not pisa_status.err else None