import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

BASE_URL = "https://www.shl.com"
CATALOG_BASE = "https://www.shl.com/products/product-catalog/"
HEADERS = {"User-Agent": "Mozilla/5.0"}

def get_all_assessment_links():
    assessment_links = set()

    # SHL catalog pagination (observed up to ~372)
    for start in range(0, 400, 12):
        url = f"{CATALOG_BASE}?start={start}&type=1"
        print(f"🔍 Crawling catalog page: {url}")

        response = requests.get(url, headers=HEADERS)
        soup = BeautifulSoup(response.text, "html.parser")

        for a in soup.find_all("a", href=True):
            href = a["href"]

            # ONLY individual test solution pages
            if "/products/product-catalog/view/" in href:
                full_url = BASE_URL + href if href.startswith("/") else href
                assessment_links.add(full_url)

        time.sleep(1)

    return list(assessment_links)


def scrape_assessment(url):
    response = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(response.text, "html.parser")

    def safe_text(selector):
        el = soup.select_one(selector)
        return el.get_text(strip=True) if el else ""

    return {
        "name": safe_text("h1"),
        "url": url,
        "description": safe_text(".product-description"),
        "test_type": safe_text(".product-tags"),
        "duration": safe_text("li:-soup-contains('Duration')"),
        "remote_support": safe_text("li:-soup-contains('Remote')"),
        "adaptive_support": safe_text("li:-soup-contains('Adaptive')")
    }


def main():
    print("🚀 Starting SHL catalog crawl...")
    links = get_all_assessment_links()
    print(f"✅ Total individual assessment pages found: {len(links)}")

    records = []

    for idx, link in enumerate(links):
        try:
            print(f"[{idx+1}/{len(links)}] Scraping {link}")
            data = scrape_assessment(link)
            records.append(data)
            time.sleep(0.8)
        except Exception as e:
            print(f"❌ Failed: {link} | {e}")

    df = pd.DataFrame(records)
    output_path = "data/raw/shl_assessments_raw.csv"
    df.to_csv(output_path, index=False)

    print(f"\n🎉 SUCCESS: Saved {len(df)} assessments to {output_path}")


if __name__ == "__main__":
    main()
