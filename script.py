"""
Scrapes the top "Featured" headline from The Daily Pennsylvanian website
and saves it to a JSON file that tracks headlines over time.
"""

import os
import sys
import bs4
import requests
import loguru
import daily_event_monitor

def scrape_featured_headline():
    """
    Scrapes the top headline from the 'Featured' section of The Daily Pennsylvanian homepage.

    Returns:
        str: The headline text if found, otherwise an empty string.
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
    }

    homepage_url = "https://www.thedp.com"
    loguru.logger.info(f"Requesting homepage: {homepage_url}")
    
    try:
        response = requests.get(homepage_url, headers=headers, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        loguru.logger.error(f"Error fetching homepage: {e}")
        return ""

    soup = bs4.BeautifulSoup(response.text, "html.parser")

    # Find the "Featured" section
    featured_section = soup.find("h3", class_="frontpage-section")
    if featured_section and "Featured" in featured_section.text:
        featured_article = featured_section.find_next("a", class_="frontpage-link standard-link")
        if featured_article:
            headline = featured_article.text.strip()
            loguru.logger.info(f"Featured Headline: {headline}")
            return headline

    loguru.logger.warning("Could not find 'Featured' article headline.")
    return ""


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
        data_point = scrape_featured_headline()
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
