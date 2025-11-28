# Automated Network Request Analysis using Selenium & BrowserMob Proxy

This script automates the process of capturing and analyzing network requests from a target website using:

- **Python 3**
- **Selenium WebDriver (with Selenium Manager auto-driver)**
- **BrowserMob Proxy**
- **Portable Java 8 (bundled inside the project)**

The script loads the chosen target website, generates a `.har` (HTTP Archive) file of all network traffic, parses the captured requests, and produces a JSON summary of HTTP status code categories.

---

## Features

- Fully automated HAR generation using BrowserMob Proxy  
- No manual ChromeDriver setup (Selenium Manager downloads automatically)  
- Portable Java 8 bundled and auto-configured at runtime  
- Categorizes responses by HTTP status groups:
  - **1XX**, **2XX**, **3XX**, **4XX**, **5XX**
- Outputs:
  - A complete `.har` file
  - A detailed JSON report with counts and percentages
- Fully portable by using relative paths (`__file__`)  
- Works on Windows without modifying system-wide JAVA settings

---

## Folder Structure

```

project-root/
│
├── browsermob-proxy-2.1.4/        # BrowserMob Proxy (bundled)
├── jdk1.8.0_471/                  # Portable Java 8 (bundled)
├── myenv/                         # Virtual environment (optional)
│
├── generate_har.py                # Main automation script
├── requirements.txt               # Python dependencies
├── example_network.har            # HAR output (generated)
├── network_summary.json           # Parsed HTTP status summary (generated)
└── README.md

````

---

## ⚙️ Installation

### 1. (Optional) Create a Virtual Environment

```bash
python -m venv myenv
myenv\Scripts\activate     # Windows
````

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

BrowserMob Proxy and Java 8 do **not** need to be installed system-wide — they are bundled in the repository.

---

## ▶️ Usage

Run the script:

```bash
python generate_har.py
```

The script will:

1. Set a local `JAVA_HOME` pointing to the bundled Java 8
2. Start BrowserMob Proxy for network capture
3. Launch Chrome using Selenium
4. Navigate to the configured website

   * Default: `https://example.com`
5. Generate a `.har` file
6. Parse and summarize HTTP status codes
7. Write the output to `network_summary.json`

---

## 📤 Output Files

### 1. **HAR File**

```
example_network.har
```

Contains complete network trace information during loading of the selected site.

### 2. **JSON Summary**

```
network_summary.json
```

Example structure:

```json
{
  "total_requests": 95,
  "status_summary": [
    {"category": "1XX", "count": 0, "percentage": 0.00},
    {"category": "2XX", "count": 78, "percentage": 82.11},
    {"category": "3XX", "count": 10, "percentage": 10.53},
    {"category": "4XX", "count": 4, "percentage": 4.21},
    {"category": "5XX", "count": 3, "percentage": 3.16}
  ]
}
```

---

## 📝 Notes

* The project uses **relative paths** to make it fully portable.
* No system-wide Java installation is required — simply extract `jdk1.8.0_471` into the project root.
* Bundle BrowserMob Proxy by extracting it into the project root:

  * **Java 8:**
    [https://www.oracle.com/java/technologies/downloads/#java8](https://www.oracle.com/java/technologies/downloads/#java8)
  * **BrowserMob Proxy:**
    [https://github.com/lightbody/browsermob-proxy/releases/tag/browsermob-proxy-2.1.4](https://github.com/lightbody/browsermob-proxy/releases/tag/browsermob-proxy-2.1.4)
* Tested on Windows + Python 3.10+ with Selenium 4.20+.

---

## 🤝 Contributions

Contributions, improvements, and pull requests are welcome!
