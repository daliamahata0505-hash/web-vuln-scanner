# Web Vulnerability Scanner

A Python-based command-line web vulnerability scanner developed as a Cyber Security project.

## Features

The scanner currently checks URL parameters for:

* SQL Injection
* Reflected Cross-Site Scripting (XSS)
* Path Traversal
* HTTP connectivity
* HTTP status code
* Content-Type
* URL parameter discovery
* Scan summary
* Text report generation

## Technologies Used

* Python
* Requests
* argparse
* urllib.parse
* PowerShell
* Visual Studio Code

## Project Structure

```text
web-vuln-scanner/
│
├── scanner.py
├── requirements.txt
├── README.md
├── scan_report.txt
├── sqli_lab_report.txt
├── xss_lab_report.txt
├── path_traversal_lab_report.txt
└── .gitignore
```

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/daliamahata0505-hash/web-vuln-scanner.git
cd web-vuln-scanner
```

### 2. Create a Virtual Environment

On Windows PowerShell:

```powershell
python -m venv venv
```

### 3. Activate the Virtual Environment

```powershell
.\venv\Scripts\Activate.ps1
```

After successful activation, the terminal should look similar to:

```text
(venv) PS C:\Users\...\web-vuln-scanner>
```

### 4. Install Dependencies

```powershell
pip install -r requirements.txt
```

## Usage

Run the scanner by providing a target URL:

```powershell
python scanner.py --url "https://example.com/?id=1"
```

To save scan results to a text report:

```powershell
python scanner.py --url "https://example.com/?id=1" --output scan_report.txt
```

## Command-Line Options

### `--url`

Specifies the target URL to scan.

Example:

```powershell
python scanner.py --url "https://example.com/?id=1"
```

### `--output`

Optionally saves the scan results to a text file.

Example:

```powershell
python scanner.py --url "https://example.com/?id=1" --output scan_report.txt
```

## Vulnerability Detection

### SQL Injection

The scanner performs basic SQL Injection checks using:

* SQL error-message detection
* Boolean-based true/false response comparison
* Response-length comparison

Example:

```text
[*] Testing for possible SQL Injection...
[!] Possible SQL Injection detected in parameter: category
    Reason: response behavior differs between boolean tests
    True response length: 4950
    False response length: 3776
```

### Reflected Cross-Site Scripting (XSS)

The scanner checks whether a test payload is reflected in the server response.

Example:

```text
[*] Testing for possible XSS...
[!] Possible XSS detected in parameter: search
    Reason: test payload reflected in response
```

### Path Traversal

The scanner tests URL parameters with path traversal payloads and checks responses for indicators of sensitive file content.

Example:

```text
[*] Testing for possible Path Traversal...
[!] Possible Path Traversal detected in parameter: filename
    Payload: ../../../../etc/passwd
    Reason: sensitive file content indicator found
```

## Testing

The scanner was tested against deliberately vulnerable **PortSwigger Web Security Academy** labs.

### Test Results

| Vulnerability  | Result   |
| -------------- | -------- |
| SQL Injection  | Detected |
| Reflected XSS  | Detected |
| Path Traversal | Detected |

### SQL Injection Test

The scanner successfully identified possible SQL Injection through differences between boolean test responses.

```text
[!] Possible SQL Injection detected in parameter: category
    Reason: response behavior differs between boolean tests
    True response length: 4950
    False response length: 3776
```

### XSS Test

The scanner successfully identified reflected XSS.

```text
[!] Possible XSS detected in parameter: search
    Reason: test payload reflected in response
```

### Path Traversal Test

The scanner successfully identified possible Path Traversal.

```text
[!] Possible Path Traversal detected in parameter: filename
    Payload: ../../../../etc/passwd
    Reason: sensitive file content indicator found
```

## Example Scan

```text
========================================
       WEB VULNERABILITY SCANNER
========================================
Target: https://example.com/?id=1

[+] Target is reachable
[+] Status Code: 200
[+] Content-Type: text/html

[*] Analyzing URL parameters...
[+] Parameters found:
    id = 1

[*] Testing for possible SQL Injection...
[-] No strong SQL injection indication in parameter: id

[*] Testing for possible XSS...
[-] No reflected XSS detected in parameter: id

[*] Testing for possible Path Traversal...
[-] No Path Traversal indication in parameter: id

========================================
             SCAN SUMMARY
========================================
Target: https://example.com/?id=1

SQL Injection       : Not Detected
XSS                 : Not Detected
Path Traversal      : Not Detected

========================================
             SCAN COMPLETE
========================================
```

## Report Generation

The scanner supports saving results to a text file.

Example:

```powershell
python scanner.py --url "https://example.com/?id=1" --output scan_report.txt
```

The generated report contains:

* Target URL
* SQL Injection result
* XSS result
* Path Traversal result
* Scan completion status

## Limitations

This project is intended for educational purposes and is not a replacement for professional security testing tools.

The scanner uses basic response-based detection techniques. Therefore, it may produce:

* False positives
* False negatives
* Detection failures caused by network timeouts
* Different results depending on application behavior

The scanner currently focuses primarily on URL query parameters.

It does not provide comprehensive coverage of all web application vulnerabilities.

## Ethical Use

Use this scanner only against systems that you own or have explicit permission to test.

Do not scan websites, applications, servers, APIs, or other systems without authorization.

For learning and testing, use deliberately vulnerable environments such as PortSwigger Web Security Academy.

## Future Improvements

Possible future improvements include:

* Configurable request timeout
* Custom User-Agent support
* Additional SQL Injection detection techniques
* Additional XSS contexts
* POST parameter testing
* HTTP header analysis
* JSON/API parameter testing
* More detailed reports
* Logging support
* Multithreaded scanning
* Additional vulnerability checks

## Author

**Dalia Mahata**

Cyber Security Project
