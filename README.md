# Basic Git Scraper Template

This template provides a starting point for **git scraping**—the technique of scraping data from websites and automatically committing it to a Git repository using workflows, [coined by Simon Willison](https://simonwillison.net/2020/Oct/9/git-scraping/).

Git scraping helps create an audit trail capturing snapshots of data over time. It leverages Git's version control and a continuous integration's scheduling capabilities to regularly scrape sites and save data without needing to manage servers.

The key benefit is automating web scrapers to run on a schedule with little overhead. The scraped data gets stored incrementally so you can review historical changes. This helps enable use-cases like price monitoring, content updates tracking, research datasets building, and more. The ability to have these resources for virtually free, enables the use of this technique for a wide range of projects.

Tools like GitHub Actions, GitLab CI and others make git scraping adaptable to diverse sites and data needs. The scraping logic just needs to output data serialized formats like CSV, JSON etc which gets committed back to git. This makes the data easily consumable downstream for analysis and vis.

This template includes a sample workflow to demonstrate the core git scraping capabilities. Read on to learn how to customize it!

## Overview

The workflow defined in `.github/workflows/scrape.yaml` runs on a defined schedule to:

1. Checkout the code
2. Set up the Python environment
3. Install dependencies via Pipenv
4. Run the python script `script.py` to scrape data
5. Commit any updated data files to the Git repository

## Scheduling

The workflow schedule is configured with [cron syntax](https://docs.github.com/en/actions/using-workflows/events-that-trigger-workflows#schedule) to run:

- Every day at 8PM UTC

This once-daily scraping is a good rule-of-thumb, as it is generally respectful of the target website, as it does not contribute to any measurable burden to the site's resources.

You can use [crontab.guru](https://crontab.guru/) to generate your own cron schedule.

## Python Libraries

The main libraries used are:

- [`bs4`](https://www.crummy.com/software/BeautifulSoup/) - BeautifulSoup for parsing HTML
- [`requests`](https://requests.readthedocs.io/en/latest/) - Making HTTP requests to scrape web pages
- [`loguru`](https://github.com/Delgan/loguru) - Logging errors and run info
- [`pytz`](https://github.com/stub42/pytz) - Handling datetimes and timezones  
- [`waybackpy`](https://github.com/akamhy/waybackpy/) - Scraping web archives (optional)

## Getting Started

To adapt this for your own scraping project:

- Use [this template to create your own repository](https://docs.github.com/en/repositories/creating-and-managing-repositories/creating-a-repository-from-a-template#creating-a-repository-from-a-template)
- Modify `script.py` to scrape different sites and data points:
  - Modifying the request URL
  - Parsing the HTML with BeautifulSoup to extract relevant data
  - Processing and outputting the scraped data as CSV, JSON etc
- Update the workflow schedule as needed
- Output and commit the scraped data to CSV, JSON or other formats
- Add any additional libraries to `Pipfile` that you need
- Update this `README.md` with project specifics

Feel free to use this as a starter kit for your Python web scraping projects!

## Setting Up a Local Development

It is recommended to use a version manager, and virtual environments and environment managers for local development of Python projects.

**asdf** is a version manager that allows you to easily install and manage multiple versions of languages and runtimes like Python. This is useful so you can upgrade/downgrade Python versions without interfering with your system Python.

**Pipenv** creates a **virtual environment** for your project to isolate its dependencies from other projects. This allows you to install packages safely without impacting globally installed packages that other tools or apps may rely on. The virtual env also allows reproducibility of builds across different systems.

Below we detail how to setup these environments to develop this template scrape project locally.

### Setting Up a Python Environment

Once you have installed `asdf`, you can install the Python plugin with:

```bash
asdf plugin add python
```

Then you can install the latest version of Python with:

```bash
asdf install python latest
```

After that, you can first install `pipenv` with:

```bash
pip install pipenv
```

### Installing Project Dependencies

Then you can install the dependencies with:

```bash
pipenv install --dev
```

This will create a virtual environment and install the dependencies from the `Pipfile`. The `--dev` flag will also install the development dependencies, which includes `ipykernel` for Jupyter Notebook support.

### Running the Script

You can then run the script to try it out with:

```bash
pipenv run python script.py
```

## Licensing

This software is distributed under the terms of the MIT License. You have the freedom to use, modify, distribute, and sell it for any purpose. However, you must include the original copyright notice and the permission notice found in the LICENSE file in all copies or substantial portions of the software.

You can [read more about the MIT license](https://choosealicense.com/licenses/mit/), and [compare different open-source licenses at `choosealicense.com`](https://choosealicense.com/licenses/).

## Some Ethical Guidelines to Consider

Web scraping is a powerful tool for gathering data, and its [legality has been upheld](https://en.wikipedia.org/wiki/HiQ_Labs_v._LinkedIn).

But it is important to use it responsibly and ethically. Here are some guidelines to consider:

1. Review the website's Terms of Service and [`robots.txt`](https://en.wikipedia.org/wiki/robots.txt) file to understand allowances and restrictions for automated scraping before starting.

2. Avoid scraping copyrighted content verbatim without permission. Summarizing is safer. Use data judiciously under "fair use" principles.

3. Do not enable illegal or fraudulent uses of scraped data, and be mindful of security and privacy.

4. Check that your scraping activity does not overload or harm the website's servers. Scale activity gradually.

5. Reflect on whether scraping could unintentionally reveal private user or organizational information from the site.

6. Consider if scraped data could negatively impact the website's value or business model.

7. Assess if decisions made using the data could contribute to bias, discrimination or unfair profiling.

8. Validate quality of scraped data, and recognize limitations in ensuring relevance and accuracy inherent with web data.  

9. Document your scraping process thoroughly for replicability, transparency and accountability.

10. Continuously re-evaluate your scraping program against applicable laws and ethical principles.

# Scraper Change: Scraping the Featured Headline

### Overview

I updated the scraper to extract the top headline from the "Featured" section of *The Daily Pennsylvanian* homepage. Previously, the script targeted a different section of the page. This update enhances the scraper by focusing on a dedicated section that highlights key stories, ensuring that the retrieved headline is a significant and relevant news article.

### Reasoning

I decided to scrape the "Featured" section was made to prioritize top editorial selections rather than general headlines. The "Featured" section often contains curated content that is more relevant and prominent. This approach provides a more consistent and meaningful headline for tracking.

### Implementation

Now the script identifies the "Featured" section by searching for an `<h3>` tag with the class `"frontpage-section"`, ensuring that the extracted headline is always from this highlighted area. The scraper then finds the first article link within this section and extracts its text. I also updated error handling by adding request timeouts and logging mechanisms to track any failures! This improves the scraper’s reliability and ensures that the collected data is more aligned with key stories highlighted by *The Daily Pennsylvanian*!

# Cron Schedule Explanation

I updated the cron schedule so the scraper now runs twice a day instead of just once. The new schedule has two cron expressions: `0 8 * * *` and `0 20 * * *`. The first one runs the scraper every day at 8:00 AM UTC, and the second one runs it again at 8:00 PM UTC. The `* * *` means it runs every day, no matter the date, month, or day of the week. This way, I’m getting more frequent updates and making sure the scraper catches any changes throughout the day.
