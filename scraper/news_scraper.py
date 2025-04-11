import requests
from bs4 import BeautifulSoup
from typing import List, Dict
from urllib.parse import urljoin
import logging
import time
from database.db import Database
from .sites import NEWS_SITES
import os
logging.basicConfig(
    filename=os.path.join(os.path.dirname(__file__), "..", "logs", "scraper.log"),
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

class NewsScraper:
    def __init__(self):
        self.db = Database()
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }

    def scrape_site(self, site: Dict) -> List[Dict]:
        """Scrape headlines and links from a news site."""
        try:
            response = requests.get(site["url"], headers=self.headers, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")

            headlines = soup.select(site["headline_selector"])
            links = soup.select(site["link_selector"])
            news_items = []
            existing_links = self.db.get_existing_news_links()

            for headline, link in zip(headlines, links):
                headline_text = headline.get_text(strip=True)
                link_href = link.get("href")
                if not headline_text or not link_href:
                    logging.debug(f"Skipped invalid news from {site['name']}: headline='{headline_text}', link='{link_href}'")
                    continue

                full_link = urljoin(site["base_url"], link_href)
                if full_link in existing_links:
                    logging.debug(f"Skipped existing news with link: {full_link}")
                    continue

                news_items.append({
                    "headline": headline_text,
                    "link": full_link,
                    "source": site["name"]
                })

            logging.info(f"Scraped {len(news_items)} new items from {site['name']}")
            return news_items

        except requests.RequestException as e:
            logging.error(f"Error scraping {site['name']}: {e} (URL: {site['url']})")
            return []

    def scrape_all(self) -> None:
        """Scrape all configured news sites and store new results."""
        logging.info("Starting news scrape cycle")
        for site in NEWS_SITES:
            news_items = self.scrape_site(site)
            for item in news_items:
                success = self.db.insert_news(
                    headline=item["headline"],
                    link=item["link"],
                    source=item["source"]
                )
                if success:
                    logging.info(f"Stored new news: {item['headline']} from {item['source']} with link: {item['link']}")
                else:
                    logging.error(f"Failed to store news: {item['headline']} (link: {item['link']})")
            time.sleep(2)
        logging.info("Completed news scrape cycle")