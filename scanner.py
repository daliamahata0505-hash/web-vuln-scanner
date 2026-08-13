import argparse
import requests
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse


def scan_target(url):
    print("========================================")
    print("       WEB VULNERABILITY SCANNER")
    print("========================================")
    print(f"Target: {url}")
    print()

    results = {
        "SQL Injection": "Not Detected",
        "XSS": "Not Detected",
        "Path Traversal": "Not Detected"
    }

    try:
        response = requests.get(url, timeout=10)

        print("[+] Target is reachable")
        print(f"[+] Status Code: {response.status_code}")
        print(
            f"[+] Content-Type: "
            f"{response.headers.get('Content-Type', 'Unknown')}"
        )
        print()

        parameters = analyze_parameters(url)

        if parameters:
            check_sql_injection(url, parameters, results)
            check_xss(url, parameters, results)
            check_path_traversal(url, parameters, results)

        print_summary(url, results)

        return results

    except requests.RequestException as error:
        print("[-] Could not connect to target")
        print(f"[-] Error: {error}")

        return None


def analyze_parameters(url):
    parsed_url = urlparse(url)
    parameters = parse_qs(parsed_url.query)

    print("[*] Analyzing URL parameters...")

    if not parameters:
        print("[-] No URL parameters found")
        return {}

    print("[+] Parameters found:")

    for name, values in parameters.items():
        print(f"    {name} = {values[0]}")

    print()

    return parameters


def build_test_url(url, parameters):
    parsed_url = urlparse(url)

    new_query = urlencode(
        parameters,
        doseq=True
    )

    return urlunparse((
        parsed_url.scheme,
        parsed_url.netloc,
        parsed_url.path,
        parsed_url.params,
        new_query,
        parsed_url.fragment
    ))


def check_sql_injection(url, parameters, results):
    print("[*] Testing for possible SQL Injection...")

    sql_error_messages = [
        "sql syntax",
        "mysql",
        "mysqli",
        "postgresql",
        "sqlite",
        "ora-",
        "odbc",
        "sqlstate",
        "syntax error"
    ]

    for parameter in parameters:

        query_parameters = parse_qs(
            urlparse(url).query
        )

        original_value = query_parameters[parameter][0]

        try:

            # --------------------------------
            # SQL ERROR TEST
            # --------------------------------

            error_parameters = query_parameters.copy()

            error_parameters[parameter] = [
                original_value + "'"
            ]

            error_test_url = build_test_url(
                url,
                error_parameters
            )

            error_response = requests.get(
                error_test_url,
                timeout=10
            )

            error_text = error_response.text.lower()

            found_error = any(
                message in error_text
                for message in sql_error_messages
            )

            if found_error:

                print(
                    f"[!] Possible SQL Injection detected "
                    f"in parameter: {parameter}"
                )

                print(
                    "    Reason: SQL error message detected"
                )

                results["SQL Injection"] = "Possible"

                continue

            # --------------------------------
            # BOOLEAN TRUE TEST
            # --------------------------------

            true_parameters = query_parameters.copy()

            true_parameters[parameter] = [
                original_value + "' AND '1'='1"
            ]

            # --------------------------------
            # BOOLEAN FALSE TEST
            # --------------------------------

            false_parameters = query_parameters.copy()

            false_parameters[parameter] = [
                original_value + "' AND '1'='2"
            ]

            true_url = build_test_url(
                url,
                true_parameters
            )

            false_url = build_test_url(
                url,
                false_parameters
            )

            true_response = requests.get(
                true_url,
                timeout=10
            )

            false_response = requests.get(
                false_url,
                timeout=10
            )

            true_length = len(true_response.text)
            false_length = len(false_response.text)

            difference = abs(
                true_length - false_length
            )

            # --------------------------------
            # RESULT
            # --------------------------------

            if difference > 100:

                print(
                    f"[!] Possible SQL Injection detected "
                    f"in parameter: {parameter}"
                )

                print(
                    "    Reason: response behavior differs "
                    "between boolean tests"
                )

                print(
                    f"    True response length: {true_length}"
                )

                print(
                    f"    False response length: {false_length}"
                )

                results["SQL Injection"] = "Possible"

            else:

                print(
                    f"[-] No strong SQL injection indication "
                    f"in parameter: {parameter}"
                )

                print(
                    f"    Response difference: "
                    f"{difference} characters"
                )

        except requests.RequestException:

            print(
                f"[-] Could not test SQL Injection "
                f"parameter: {parameter}"
            )

    print()


def check_xss(url, parameters, results):
    print("[*] Testing for possible XSS...")

    xss_payload = "<script>alert('XSS')</script>"

    for parameter in parameters:

        query_parameters = parse_qs(
            urlparse(url).query
        )

        query_parameters[parameter] = [
            xss_payload
        ]

        test_url = build_test_url(
            url,
            query_parameters
        )

        try:

            response = requests.get(
                test_url,
                timeout=10
            )

            response_text = response.text.lower()

            if xss_payload.lower() in response_text:

                print(
                    f"[!] Possible XSS detected "
                    f"in parameter: {parameter}"
                )

                print(
                    "    Reason: test payload reflected "
                    "in response"
                )

                results["XSS"] = "Possible"

            else:

                print(
                    f"[-] No reflected XSS detected "
                    f"in parameter: {parameter}"
                )

        except requests.RequestException:

            print(
                f"[-] Could not test XSS "
                f"parameter: {parameter}"
            )

    print()


def check_path_traversal(url, parameters, results):
    print("[*] Testing for possible Path Traversal...")

    traversal_payloads = [
        "../../etc/passwd",
        "../../../etc/passwd",
        "../../../../etc/passwd"
    ]

    traversal_indicators = [
        "root:x:",
        "daemon:x:",
        "bin:x:",
        "/bin/bash",
        "/usr/sbin"
    ]

    for parameter in parameters:

        original_parameters = parse_qs(
            urlparse(url).query
        )

        detected = False
        test_failed = False

        for payload in traversal_payloads:

            test_parameters = original_parameters.copy()

            test_parameters[parameter] = [
                payload
            ]

            test_url = build_test_url(
                url,
                test_parameters
            )

            try:

                response = requests.get(
                    test_url,
                    timeout=10
                )

                response_text = response.text.lower()

                for indicator in traversal_indicators:

                    if indicator.lower() in response_text:

                        print(
                            f"[!] Possible Path Traversal "
                            f"detected in parameter: {parameter}"
                        )

                        print(
                            "    Reason: sensitive file "
                            "content indicator found"
                        )

                        results["Path Traversal"] = "Possible"

                        detected = True
                        break

                if detected:
                    break

            except requests.RequestException:

                print(
                    f"[-] Could not test Path Traversal "
                    f"parameter: {parameter}"
                )

                test_failed = True
                break

        if not detected and not test_failed:

            print(
                f"[-] No Path Traversal indication "
                f"in parameter: {parameter}"
            )

    print()


def print_summary(url, results):
    print("========================================")
    print("             SCAN SUMMARY")
    print("========================================")

    print(f"Target: {url}")
    print()

    print(
        f"SQL Injection       : "
        f"{results['SQL Injection']}"
    )

    print(
        f"XSS                 : "
        f"{results['XSS']}"
    )

    print(
        f"Path Traversal      : "
        f"{results['Path Traversal']}"
    )

    print()
    print("========================================")
    print("             SCAN COMPLETE")
    print("========================================")


def save_report(filename, url, results):

    try:

        with open(
            filename,
            "w",
            encoding="utf-8"
        ) as report:

            report.write(
                "========================================\n"
            )

            report.write(
                "       WEB VULNERABILITY SCANNER\n"
            )

            report.write(
                "========================================\n\n"
            )

            report.write(
                f"Target: {url}\n\n"
            )

            report.write(
                "SCAN RESULTS\n"
            )

            report.write(
                "------------\n"
            )

            report.write(
                f"SQL Injection       : "
                f"{results['SQL Injection']}\n"
            )

            report.write(
                f"XSS                 : "
                f"{results['XSS']}\n"
            )

            report.write(
                f"Path Traversal      : "
                f"{results['Path Traversal']}\n"
            )

            report.write("\n")

            report.write(
                "========================================\n"
            )

            report.write(
                "             SCAN COMPLETE\n"
            )

            report.write(
                "========================================\n"
            )

        print()
        print(
            f"[+] Report saved successfully: "
            f"{filename}"
        )

    except OSError as error:

        print(
            f"[-] Could not save report: {error}"
        )


# ========================================
# COMMAND-LINE INTERFACE
# ========================================

parser = argparse.ArgumentParser(
    description="CLI Web Vulnerability Scanner"
)

parser.add_argument(
    "--url",
    required=True,
    help="Target URL to scan"
)

parser.add_argument(
    "--output",
    help="Save scan results to a report file"
)

args = parser.parse_args()


# ========================================
# START SCANNER
# ========================================

results = scan_target(args.url)


# ========================================
# SAVE REPORT IF REQUESTED
# ========================================

if results is not None and args.output:

    save_report(
        args.output,
        args.url,
        results
    )