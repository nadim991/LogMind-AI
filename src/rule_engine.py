import re

class RuleEngine:
    def __init__(self):
        # Basic attack signatures (SQLi, XSS, Path Traversal)
        self.rules = {
            "SQL Injection": r"(union|select|insert|delete|drop|alter|--|' OR '1'='1)",
            "XSS Attack": r"(<script>|javascript:|onerror=|onload=)",
            "Path Traversal": r"(\.\./|\.\.\\)"
        }

    def analyze(self, url: str):
        detected_threats = []
        for threat_type, pattern in self.rules.items():
            if re.search(pattern, url, re.IGNORECASE):
                detected_threats.append(threat_type)
        return detected_threats