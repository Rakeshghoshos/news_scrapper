# News websites (global and Indian financial news)
NEWS_SITES = [
    {"name": "Bloomberg", "url": "https://www.bloomberg.com/markets", "headline_selector": "h1, a.headline", "link_selector": "h1 a, a.headline", "base_url": "https://www.bloomberg.com"},
    {"name": "Reuters", "url": "https://www.reuters.com/markets/", "headline_selector": "h3", "link_selector": "a[href*='/markets/']", "base_url": "https://www.reuters.com"},
    {"name": "Financial Times", "url": "https://www.ft.com/markets", "headline_selector": "h3, a.js-teaser-heading-link", "link_selector": "a.js-teaser-heading-link", "base_url": "https://www.ft.com"},
    {"name": "CNBC", "url": "https://www.cnbc.com/markets/", "headline_selector": "a.Card-title", "link_selector": "a.Card-title", "base_url": "https://www.cnbc.com"},
    {"name": "Forbes", "url": "https://www.forbes.com/money/", "headline_selector": "h2, a[data-ga-track*='headline']", "link_selector": "a[data-ga-track*='headline']", "base_url": "https://www.forbes.com"},
    {"name": "The Wall Street Journal", "url": "https://www.wsj.com/news/markets", "headline_selector": "h3, a.WSJTheme--headline--link", "link_selector": "a.WSJTheme--headline--link", "base_url": "https://www.wsj.com"},
    {"name": "Yahoo Finance", "url": "https://finance.yahoo.com/topic/markets/", "headline_selector": "h3, a[data-test-locator='headline']", "link_selector": "a[data-test-locator='headline']", "base_url": "https://finance.yahoo.com"},
    {"name": "Moneycontrol", "url": "https://www.moneycontrol.com/news/business/markets/", "headline_selector": "h2 a", "link_selector": "h2 a", "base_url": "https://www.moneycontrol.com"},
    {"name": "Economic Times", "url": "https://economictimes.indiatimes.com/markets/stocks/news", "headline_selector": "h3 a", "link_selector": "h3 a", "base_url": "https://economictimes.indiatimes.com"},
    {"name": "NDTV Profit", "url": "https://www.ndtvprofit.com/markets", "headline_selector": "h2, a.story__title", "link_selector": "a.story__title", "base_url": "https://www.ndtvprofit.com"},
    {"name": "Financial Express", "url": "https://www.financialexpress.com/market/", "headline_selector": "h3, a.post-title", "link_selector": "a.post-title", "base_url": "https://www.financialexpress.com"},
    {"name": "Business Standard", "url": "https://www.business-standard.com/markets", "headline_selector": "h2, a[href*='/article/']", "link_selector": "a[href*='/article/']", "base_url": "https://www.business-standard.com"},
    {"name": "Mint", "url": "https://www.livemint.com/market", "headline_selector": "h2, a.headline", "link_selector": "a.headline", "base_url": "https://www.livemint.com"}
]