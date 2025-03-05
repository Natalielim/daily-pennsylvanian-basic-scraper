"""
Scrapes a headline from The Daily Pennsylvanian website and saves it to a 
JSON file that tracks headlines over time.
"""

import os
import sys
import json
import bs4
import requests
import loguru
import daily_event_monitor

def scrape_most_read_article():
    """
    Scrapes the most read article headline by making two HTTP requests:
    1. Fetches the homepage and extracts the most-read article URL.
    2. Fetches the article page and extracts its headline.

    Returns:
        str: The article headline if found, otherwise an empty string.
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
    }

    # Step 1: Fetch the homepage
    homepage_url = "https://www.thedp.com"
    loguru.logger.info(f"Requesting homepage: {homepage_url}")
    
    try:
        response = requests.get(homepage_url, headers=headers, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        loguru.logger.error(f"Error fetching homepage: {e}")
        return ""

    soup = bs4.BeautifulSoup(response.text, "html.parser")

    # Find Most Read section
    most_read_section = soup.find("span", id="mostRead")
    if not most_read_section:
        loguru.logger.warning("Could not find 'Most Read' section.")
        return ""

    # Extract first article link
    first_article = most_read_section.find("a", class_="frontpage-link standard-link")
    if not first_article or not first_article.get("href"):
        loguru.logger.warning("Could not find 'Most Read' article link.")
        return ""

    article_url = homepage_url + first_article["href"]
    loguru.logger.info(f"Most Read Article URL: {article_url}")

    # Step 2: Fetch the article page
    try:
        article_response = requests.get(article_url, headers=headers, timeout=10)
        article_response.raise_for_status()
    except requests.RequestException as e:
        loguru.logger.error(f"Error fetching article page: {e}")
        return ""

    article_soup = bs4.BeautifulSoup(article_response.text, "html.parser")

    # Extract article headline (usually <h1>)
    headline = article_soup.find("h1")
    if not headline:
        loguru.logger.warning("Could not find article headline.")
        return ""

    headline_text = headline.text.strip()
    loguru.logger.info(f"Extracted Headline: {headline_text}")

    return headline_text


if __name__ == "__main__":

    # Setup logger to track runtime
    loguru.logger.add("scrape.log", rotation="1 day")

    # Create data dir if needed
    loguru.logger.info("Creating data directory if it does not exist")
    try:
        os.makedirs("data", exist_ok=True)
    except Exception as e:
        loguru.logger.error(f"Failed to create data directory: {e}")
        sys.exit(1)

    # Load daily event monitor
    loguru.logger.info("Loading daily event monitor")
    dem = daily_event_monitor.DailyEventMonitor(
        "data/daily_pennsylvanian_headlines.json"
    )

    # Run scrape
    loguru.logger.info("Starting scrape")
    try:
        data_point = scrape_most_read_article()
    except Exception as e:
        loguru.logger.error(f"Failed to scrape data point: {e}")
        data_point = None

    # Save data
    if data_point:
        dem.add_today(data_point)
        dem.save()
        loguru.logger.info("Saved daily event monitor")

    def print_tree(directory, ignore_dirs=[".git", "__pycache__"]):
        loguru.logger.info(f"Printing tree of files/dirs at {directory}")
        for root, dirs, files in os.walk(directory):
            dirs[:] = [d for d in dirs if d not in ignore_dirs]
            level = root.replace(directory, "").count(os.sep)
            indent = " " * 4 * (level)
            loguru.logger.info(f"{indent}+--{os.path.basename(root)}/")
            sub_indent = " " * 4 * (level + 1)
            for file in files:
                loguru.logger.info(f"{sub_indent}+--{file}")

    print_tree(os.getcwd())

    loguru.logger.info("Printing contents of data file {}".format(dem.file_path))
    with open(dem.file_path, "r") as f:
        loguru.logger.info(f.read())

    # Finish
    loguru.logger.info("Scrape complete")
    loguru.logger.info("Exiting")
