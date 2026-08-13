# Web Vulnerability Scanner

A Python-based command-line web vulnerability scanner developed as a Cyber Security project.

## Features

The scanner currently checks URL parameters for:

- SQL Injection
- Reflected Cross-Site Scripting (XSS)
- Path Traversal
- HTTP connectivity
- HTTP status code
- Content-Type
- URL parameter discovery
- Scan summary
- Text report generation

## Technologies Used

- Python
- Requests
- argparse
- urllib.parse
- PowerShell
- VS Code

## Project Structure

```text
web-vuln-scanner/
│
├── scanner.py
├── requirements.txt
├── README.md
├── scan_report.txt
│
├── scanner_backup.py
├── scanner_summary_backup.py
├── scanner_v3_backup.py
├── scanner_xss_backup.py
│
└── venv/