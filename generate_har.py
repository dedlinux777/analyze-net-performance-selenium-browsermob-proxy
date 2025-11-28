import os
import sys
import time
import json
from browsermobproxy import Server
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# project-relative locations (ensure these directories exist in the project root)
BROWSERMOB_DIR = os.path.join(BASE_DIR, "browsermob-proxy-2.1.4")
JDK_DIR = os.path.join(BASE_DIR, "jdk1.8.0_471")

HAR_FILENAME = os.path.join(BASE_DIR, "exactspace_network.har")
SUMMARY_JSON = os.path.join(BASE_DIR, "network_summary.json")
TARGET_URL = "https://exactspace.co/"


# Validate and set up Java environment (process-only)
java_bin_dir = os.path.join(JDK_DIR, "bin")
if not os.path.isdir(java_bin_dir):
    print(f"ERROR: Expected bundled JDK not found at: {java_bin_dir}")
    print("Please ensure 'jdk1.8.0_471' is extracted in the same folder as this script.")
    sys.exit(1)

# java bin to PATH for subprocesses
os.environ["JAVA_HOME"] = JDK_DIR
os.environ["PATH"] = java_bin_dir + os.pathsep + os.environ.get("PATH", "")


bmp_exec = os.path.join(BROWSERMOB_DIR, "bin", "browsermob-proxy")

if os.name == "nt" and os.path.exists(bmp_exec + ".bat"):
    bmp_exec = bmp_exec + ".bat"

if not os.path.exists(bmp_exec):
    print("ERROR: browsermob-proxy executable not found. Expected at:", bmp_exec)
    print("Please ensure 'browsermob-proxy-2.1.4' folder exists in the same folder as this script.")
    sys.exit(1)



def categorize_status(status):
    try:
        s = int(status)
    except Exception:
        return None
    if 100 <= s < 200:
        return "1XX"
    if 200 <= s < 300:
        return "2XX"
    if 300 <= s < 400:
        return "3XX"
    if 400 <= s < 500:
        return "4XX"
    if 500 <= s < 600:
        return "5XX"
    return None

def write_json_summary(total, counts, out_path):
    categories = ["1XX", "2XX", "3XX", "4XX", "5XX"]
    summary_list = []
    for cat in categories:
        cnt = counts.get(cat, 0)
        percent = 0.0
        if total > 0:
            percent = round((cnt / total) * 100.0, 2)
        summary_list.append({
            "category": cat,
            "count": cnt,
            "percentage": float(f"{percent:.2f}")
        })
    out = {
        "total_requests": total,
        "status_summary": summary_list
    }
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2)
    print(f"Wrote summary JSON to: {out_path}")



def main():
    server = None
    driver = None
    try:
        print("Starting BrowserMob Proxy server using bundled executable:")
        print("  ", bmp_exec)
        server = Server(bmp_exec)
        server.start()

        proxy = server.create_proxy(params={"trustAllServers": "true"})
        print("Proxy started. Proxy endpoint:", proxy.proxy)


        chrome_options = Options()
        chrome_options.add_argument("--ignore-certificate-errors")
        chrome_options.add_argument(f"--proxy-server={proxy.proxy}")

        chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])

        print("Launching Chrome via Selenium Manager (webdriver.Chrome()) ...")
        driver = webdriver.Chrome(options=chrome_options)


        try:
            proxy.new_har("exactspace.co", options={"captureHeaders": True, "captureContent": True})
        except TypeError:
            proxy.new_har("exactspace.co")

        print(f"Navigating to {TARGET_URL}")
        driver.get(TARGET_URL)

        # wait for resources to load; increase if dynamic content loads later
        time.sleep(8)

        # Save HAR
        har_data = proxy.har  # dictionary
        with open(HAR_FILENAME, "w", encoding="utf-8") as f:
            json.dump(har_data, f, indent=2)
        print("Saved HAR to:", HAR_FILENAME)

        # Parse HAR entries for status codes
        entries = har_data.get("log", {}).get("entries", [])
        total_requests = len(entries)
        counts = {}
        for entry in entries:
            status = entry.get("response", {}).get("status")
            cat = categorize_status(status)
            if cat:
                counts[cat] = counts.get(cat, 0) + 1

        print("Total requests:", total_requests)
        print("Counts by category:", counts)

        # Write the required JSON summary file
        write_json_summary(total_requests, counts, SUMMARY_JSON)

        print("\nFiles produced:")
        print(" - HAR:", os.path.abspath(HAR_FILENAME))
        print(" - Summary JSON:", os.path.abspath(SUMMARY_JSON))

    except Exception as e:
        print("ERROR during run:", e)
        raise
    finally:
        try:
            if driver:
                driver.quit()
        except Exception:
            pass
        try:
            if server:
                server.stop()
        except Exception:
            pass

if __name__ == "__main__":
    main()
