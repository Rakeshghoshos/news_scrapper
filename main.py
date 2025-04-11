from fastapi import FastAPI, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from scraper.news_scraper import NewsScraper
from database.db import Database
from models.news import NewsItem
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime
import logging
import os
import asyncio

LOG_FILE = os.path.join(os.path.dirname(__file__), "logs", "scraper.log")
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

app = FastAPI(title="Financial News Scraper")
news_scraper = NewsScraper()
db = Database()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def clear_logs():
    try:
        if os.path.exists(LOG_FILE):
            os.remove(LOG_FILE)
            print(f"{datetime.utcnow()} - INFO - Log file {LOG_FILE} deleted successfully")
        else:
            logging.info("Log file does not exist; no action taken")
    except OSError as e:
        logging.error(f"Error deleting log file: {e}")

async def continuous_news_scrape():
    while True:
        news_scraper.scrape_all()
        await asyncio.sleep(5)

scheduler = AsyncIOScheduler()
scheduler.add_job(
    db.delete_all_data,
    "cron",
    hour=0,
    minute=0,
    timezone="UTC",
    id="nightly_cleanup"
)
scheduler.add_job(
    clear_logs,
    "interval",
    hours=48,
    id="log_cleanup"
)

scheduler.start()

@app.on_event("startup")
async def startup_event():
    logging.info("Starting FastAPI application and scheduler")
    asyncio.create_task(continuous_news_scrape())

@app.on_event("shutdown")
async def shutdown_event():
    scheduler.shutdown()
    logging.info("Shutting down FastAPI application and scheduler")

@app.get("/news", response_model=list[NewsItem])
async def get_news():
    news = db.get_all_news()
    return [
        NewsItem(
            headline=item["headline"],
            link=item["link"],
            source=item["source"],
            scraped_at=datetime.fromisoformat(item["scraped_at"])
        )
        for item in news
    ]

@app.post("/scrape/news")
async def trigger_news_scrape(background_tasks: BackgroundTasks):
    background_tasks.add_task(news_scraper.scrape_all)
    return {"message": "News scraping started in the background"}
