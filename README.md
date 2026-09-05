# 🛡️ LogMind AI — Smart SOC Engine with LLM Agent

![Python Version](https://img.shields.io/badge/python-3.10%2B-blue?style=for-the-badge&logo=python)
![Framework](https://img.shields.io/badge/Groq_API-GPT--OSS--20B-orange?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)
![SOC Security](https://img.shields.io/badge/Security-SOC_Analyst_AI-red?style=for-the-badge)

**LogMind AI** is a lightweight, hybrid Security Operations Center (SOC) Log Analysis Engine. It combines high-speed deterministic regex rules with Large Language Model (LLM) agents to analyze web server logs, detect attack signatures, map threats to the **MITRE ATT&CK** framework, and automatically generate executive incident reports in **HTML**, **JSON**, and **PDF** formats.

---

## 🚀 Key Features

- **Hybrid Detection Pipeline:** Combines traditional signature-based detection for web vulnerabilities with LLM intelligence.
- **Rule-Based Pattern Matching:**
  - 💉 **SQL Injection (SQLi):** Detects payload signatures and malicious query params.
  - ⚡ **Command Injection (CmdI):** Flags shell execution symbols (`|`, `;`, `$(...)`).
  - 🔨 **Brute Force Detection:** Stateful tracking of repeated 401 HTTP responses per IP.
- **LLM-Powered SOC Insights:** Integrated with Groq API (`openai/gpt-oss-20b`) for real-time:
  - Threat Severity & Impact Assessment.
  - Precise **MITRE ATT&CK** Technique ID mapping.
  - Immediate Mitigation Steps for Incident Response.
- **Multi-Format Automated Reporting:** Exports analysis results into clean **HTML**, **JSON**, and **PDF** files inside the `reports/` directory.

---

## 📂 Project Architecture

```text
LogMind-AI/
├── logs/
│   └── sample_access.log     # Test web server access log
├── reports/                  # Generated HTML, JSON, and PDF reports
├── src/
│   ├── ai_agent.py           # Groq LLM SOC Analyst Agent
│   ├── parser.py             # Main Log Parsing Engine & Rule Matching
│   ├── reporter.py           # HTML, JSON & PDF Generator Engine
│   ├── list_models.py        # Utility script to check active Groq models
│   └── test_env.py           # Utility script to test .env load
├── .env                      # API Keys (Git Ignored)
├── .gitignore
├── requirements.txt
└── README.md