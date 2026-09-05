import os
import re
from collections import defaultdict
from colorama import Fore, Style, init
from ai_agent import SOCAiAgent
from reporter import ReportGenerator

init(autoreset=True)

class LogParser:
    def __init__(self, log_file):
        self.log_file = log_file
        self.failed_attempts = defaultdict(int)
        self.alerts = []
        
        try:
            self.agent = SOCAiAgent()
            self.ai_enabled = True
        except Exception:
            self.ai_enabled = False

        self.sqli_pattern = re.compile(r"('|\"|%27|--|union\s+select|select\s+.*\s+from)", re.IGNORECASE)
        self.cmdi_pattern = re.compile(r"(;|\|\||&&|\$\(.*\)|`.*`)", re.IGNORECASE)

    def parse(self):
        print(Fore.CYAN + "="*50)
        print(Fore.CYAN + "[*] LogMind AI - Smart SOC Engine with LLM Agent")
        print(Fore.CYAN + "="*50 + "\n")

        if not self.ai_enabled:
            print(Fore.YELLOW + "[!] AI Agent disabled: Check .env for GROQ_API_KEY\n")

        if not os.path.exists(self.log_file):
            print(Fore.RED + f"[X] Error: File '{self.log_file}' not found!")
            return

        with open(self.log_file, "r") as f:
            for line in f:
                parts = line.split()
                if len(parts) < 7:
                    continue
                
                ip = parts[0]
                method = parts[5].replace('"', '')
                url = parts[6]
                status = parts[8] if len(parts) > 8 else "200"

                threats = []
                if self.sqli_pattern.search(url):
                    threats.append("SQL Injection")
                if self.cmdi_pattern.search(url):
                    threats.append("Command Injection")
                
                if "/login" in url and status == "401":
                    self.failed_attempts[ip] += 1
                    if self.failed_attempts[ip] >= 3:
                        threats.append("Brute Force Attack")

                if threats:
                    print(Fore.RED + f"[ALERT] Threat Identified!")
                    print(Fore.WHITE + f"  └─ IP: {ip}")
                    print(Fore.WHITE + f"  └─ Target URL: {url}")
                    print(Fore.WHITE + f"  └─ Attack Type: {', '.join(threats)}")
                    
                    insight_text = "AI Analysis Disabled"
                    if self.ai_enabled:
                        print(Fore.MAGENTA + "  └─ Generating SOC Analyst Insight (LLM)...")
                        insight_text = self.agent.analyze_threat(ip, url, threats)
                        print(Fore.CYAN + insight_text)

                    self.alerts.append({
                        "ip": ip,
                        "url": url,
                        "threat": ", ".join(threats),
                        "insight": insight_text
                    })
                    print("-" * 50)
                else:
                    print(Fore.GREEN + f"[INFO] Normal Traffic: {ip} -> {url}")

        if self.alerts:
            reporter = ReportGenerator()
            json_file = reporter.generate_json(self.alerts)
            html_file = reporter.generate_html(self.alerts)
            print("\n" + Fore.GREEN + f"[+] HTML Report Generated: {html_file}")
            print(Fore.GREEN + f"[+] JSON Report Generated: {json_file}")

if __name__ == "__main__":
    parser = LogParser("logs/sample_access.log")
    parser.parse()