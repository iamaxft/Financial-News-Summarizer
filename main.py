import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import schedule
import json

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
from goose3 import Goose

# Imports for the summarizer part
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer as Summarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words

# --- CONFIGURATION ---
# Scheduling Toggle: Set to True to run on schedule, False to run once.
ENABLE_SCHEDULE = True

# Email Configuration
SENDER_EMAIL = "skfourcc@gmail.com"
SENDER_PASSWORD = "ftlu yhce xwro qqwr"  # Use the App Password you generated
RECEIVER_EMAIL = "multiverse940@gmail.com"

# File to store the titles of already seen articles
SEEN_ARTICLES_FILE = 'seen_articles.json'


def send_email(subject, html_content):
    """Sends the news digest as an HTML email."""
    print("Preparing to send email...")
    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = RECEIVER_EMAIL
    msg['Subject'] = subject

    # Attach the HTML content
    msg.attach(MIMEText(html_content, 'html'))

    try:
        # Connect to Gmail's SMTP server
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.send_message(msg)
        print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")


def format_digest_as_html(digest):
    """Formats the list of articles into a clean HTML string for the email."""
    if not digest:
        return "<p>No new articles found today.</p>"

    html = "<h1>Your Financial News Digest</h1>"
    for item in digest:
        html += f"""
        <div style="margin-bottom: 20px; border-bottom: 1px solid #eee; padding-bottom: 10px;">
            <h3 style="margin-bottom: 5px;">{item['title']}</h3>
            <p><strong>Summary:</strong> {item['summary']}</p>
            <a href="{item['link']}">Read full article</a>
        </div>
        """
    return html


def load_seen_articles():
    """Loads the set of seen article titles from a file."""
    try:
        with open(SEEN_ARTICLES_FILE, 'r') as f:
            return set(json.load(f))
    except (FileNotFoundError, json.JSONDecodeError):
        return set()


def save_seen_articles(titles):
    """Saves the set of seen article titles to a file."""
    with open(SEEN_ARTICLES_FILE, 'w') as f:
        json.dump(list(titles), f)


def scrape_and_summarize_rbi():
    # This function remains the same as the previous working version
    # (The function from the previous step that uses Goose3)
    print("Launching browser using local chromedriver.exe...")
    driver = None
    try:
        service = Service(executable_path='chromedriver.exe')
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--log-level=3')
        driver = webdriver.Chrome(service=service, options=options)

        WHATS_NEW_URL = "https://website.rbi.org.in/en/web/rbi/whats-new"

        print(f"Navigating to: {WHATS_NEW_URL}")
        driver.get(WHATS_NEW_URL)
        time.sleep(5)

        print("Finding all links and filtering for important news...")
        all_links = driver.find_elements(By.TAG_NAME, "a")
        keywords = ['press-release', 'notification', 'circular', 'monetary', 'policy']

        articles = []
        for link in all_links:
            title = link.text.strip()
            url = link.get_attribute('href')
            if not title or not url:
                continue
            if any(keyword in url.lower() or keyword in title.lower() for keyword in keywords):
                if {'title': title, 'link': url} not in articles:
                    articles.append({'title': title, 'link': url})

        print(f"Found {len(articles)} relevant articles.")

        print("\nGenerating summaries using Goose3 article extractor...")
        news_digest = []
        LANGUAGE = "english"
        SENTENCES_COUNT = 3

        g = Goose()

        for article in articles[:5]:
            print(f"  -> Visiting and summarizing: {article['title']}")
            try:
                driver.get(article['link'])
                page_source = driver.page_source
                extracted_article = g.extract(raw_html=page_source)
                article_text = extracted_article.cleaned_text

                if not article_text:
                    article_text = "Goose could not extract main content."

                parser = PlaintextParser.from_string(article_text, Tokenizer(LANGUAGE))
                stemmer = Stemmer(LANGUAGE)
                summarizer = Summarizer(stemmer)
                summarizer.stop_words = get_stop_words(LANGUAGE)
                summary_sentences = summarizer(parser.document, SENTENCES_COUNT)
                summary = " ".join([str(s) for s in summary_sentences])

                news_digest.append({**article, 'summary': summary})

            except Exception as e:
                news_digest.append({**article, 'summary': f"Could not summarize (Reason: {e})"})

        return news_digest

    finally:
        if driver:
            print("\nClosing browser.")
            driver.quit()


def job():
    """The main job to be scheduled."""
    print(f"\n--- Running scheduled job at {time.ctime()} ---")

    # 1. Load articles we've already seen
    seen_titles = load_seen_articles()

    # 2. Scrape for the latest articles
    latest_articles = scrape_and_summarize_rbi()

    # 3. Filter out the articles we've already seen
    new_articles = [article for article in latest_articles if article['title'] not in seen_titles]

    if not new_articles:
        print("No new articles found since last check.")
        # Send an email saying nothing is new
        send_email("Financial News: No New Updates", "<p>No new articles were found on the RBI website today.</p>")
    else:
        print(f"Found {len(new_articles)} new articles. Preparing email digest.")
        # Format the new articles for the email
        html_digest = format_digest_as_html(new_articles)
        send_email("Your Daily Financial News Digest", html_digest)

        # 4. Update the seen articles file with the new titles
        for article in new_articles:
            seen_titles.add(article['title'])
        save_seen_articles(seen_titles)


# Main execution block
# Main execution block for immediate testing
if __name__ == "__main__":
    # This will run the job once, right now, for testing purposes.
    print("Running the job immediately to test email functionality...")
    job()
    print("\nTest run complete.")