import re
import os
from collections import defaultdict
from colorama import Fore, Style, init
from ai_agent import SOCAiAgent

init(autoreset=True)

LOG_FILE_PATH = os.path.join("logs", "sample_access.log")

ATTACK_PATTERNS = {
    "SQL Injection": [r"' OR '1'='1", r"UNION SELECT", r"--"],
    "Command Injection": [r";whoami", r"\|whoami", r"&&", r";\s*ls"],
    "Directory Traversal": [r"\.\./\.\./", r"/etc/passwd"]
}

def parse_log_line(line):
    regex = r'(\d+\.\d+\.\d+\.\d+)\s+-\s+-\s+\[(.*?)\]\s+"(\w+)\s+(.*?)\s+HTTP/.*?"\s+(\d+)\s+(\d+)'
    match = re.match(regex, line)
    if match:
        return {
            "ip": match.group(1),
            "timestamp": match.group(2),
            "method": match.group(3),
            "url": match.group(4),
            "status": int(match.group(5)),
            "size": int(match.group(6))
        }
    return None

def detect_threats(parsed_log):
    url = parsed_log["url"]
    detected_threats = []
    for threat_type, patterns in ATTACK_PATTERNS.items():
        for pattern in patterns:
            if re.search(pattern, url, re.IGNORECASE):
                detected_threats.append(threat_type)
                break
    return list(set(detected_threats))

def analyze_logs():
    if not os.path.exists(LOG_FILE_PATH):
        print(f"{Fore.RED}[!] Log file not found at {LOG_FILE_PATH}")
        return

    print(f"{Fore.CYAN}==================================================")
    print(f"{Fore.CYAN}[*] LogMind AI - Smart SOC Engine with LLM Agent")
    print(f"{Fore.CYAN}==================================================\n")

    try:
        ai_agent = SOCAiAgent()
        ai_enabled = True
    except Exception as e:
        print(f"{Fore.YELLOW}[!] AI Agent disabled: {e}\n")
        ai_enabled = False

    failed_login_attempts = defaultdict(int)

    with open(LOG_FILE_PATH, "r") as f:
        for line in f:
            log_data = parse_log_line(line.strip())
            if log_data:
                threats = detect_threats(log_data)
                
                if log_data["url"] == "/login.php" and log_data["status"] == 401:
                    failed_login_attempts[log_data["ip"]] += 1
                    if failed_login_attempts[log_data["ip"]] >= 3:
                        threats.append("Brute Force Attack")

                log_data["threats"] = list(set(threats))

                if log_data["threats"]:
                    print(f"{Fore.RED}[ALERT] Threat Identified!")
                    print(f"  └─ IP: {log_data['ip']}")
                    print(f"  └─ Target URL: {log_data['url']}")
                    print(f"  └─ Attack Type: {Fore.YELLOW}{', '.join(log_data['threats'])}{Style.RESET_ALL}")
                    
                    if ai_enabled:
                        print(f"{Fore.MAGENTA}  └─ Generating SOC Analyst Insight (LLM)...")
                        insight = ai_agent.analyze_threat(log_data['ip'], log_data['url'], log_data['threats'])
                        print(f"{Fore.LIGHTBLACK_EX}{insight}\n")
                        print("-" * 50)
                else:
                    print(f"{Fore.GREEN}[INFO] Normal Traffic: {log_data['ip']} -> {log_data['url']}")

if __name__ == "__main__":
    analyze_logs()