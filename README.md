# 🔐 Web Vulnerability Scanner

A Python-based command-line web vulnerability scanner developed as a Cyber Security project.

The tool performs basic, response-based checks for common web vulnerabilities in URL query parameters and generates readable scan results and text reports.

> ⚠️ **Educational Use Only:** This project is intended for authorized security testing and deliberately vulnerable environments such as PortSwigger Web Security Academy.

---

## 🚀 Features

The scanner currently supports:

- SQL Injection detection
- Reflected Cross-Site Scripting (XSS) detection
- Path Traversal detection
- HTTP connectivity testing
- HTTP status-code detection
- Content-Type detection
- URL parameter discovery
- Response-based vulnerability analysis
- Command-line interface
- Text report generation
- Basic error and timeout handling

---

## 🛠️ Technologies Used

- **Python 3**
- **Requests**
- **argparse**
- **urllib.parse**
- **PowerShell**
- **Visual Studio Code**
- **Git & GitHub**

---

## 📂 Project Structure

```text
web-vuln-scanner/
│
├── scanner.py
├── requirements.txt
├── README.md
├── LICENSE
├── scan_report.txt
├── sqli_lab_report.txt
├── xss_lab_report.txt
├── path_traversal_lab_report.txt
└── .gitignore