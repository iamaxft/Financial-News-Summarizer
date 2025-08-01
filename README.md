
Financial News Scraper & SummarizerThis project features an intelligent Python script that automates the process of scraping financial news from the Reserve Bank of India (RBI) website,
generating concise summaries using Natural Language Processing (NLP), and delivering them as a daily email digest.The script is designed to be resilient against website changes by
using Selenium for browser automation and Goose3 for intelligent content extraction.FeaturesAutomated Web Scraping: Uses Selenium to control a headless Chrome browser,
bypassing anti-scraping measures and handling JavaScript-heavy websites.Intelligent Content Filtering: Scans the "What's New" section and intelligently identifies relevant articles 
based on keywords (e.g., "press-release", "monetary policy", "notification").AI-Powered Summarization: Employs the sumy library with the LSA algorithm to generate concise, 
3-sentence summaries of each article.Duplicate Prevention: Keeps track of already processed articles in a seen_articles.json file to ensure only new updates are sent.Automated Email
Alerts: Sends a professionally formatted HTML email digest of the new articles. If no new articles are found, it sends a notification stating so.
Flexible Scheduling: Includes a built-in scheduler to run the task automatically every day, with an easy on/off toggle for testing and control.

Tech StackLanguage: 

**Python 3Web Scraping & Automation: Selenium, 
BeautifulSoup4Article Content Extraction: Goose3NLP 
(Summarization): Sumy
NLTKScheduling: ScheduleEmailing: smtplibSetup 
and InstallationFollow these steps to get the project running on your local machine.**

1. Clone the Repositorygit clone https://github.com/iamaxft/Financial_News_Summarizer.git
cd Financial_News_Summarizer
Create a Virtual EnvironmentIt's highly recommended to use a virtual environment to manage project dependencies.

# For Windows
python -m venv venv
venv\Scripts\activate

# For macOS/Linux
python3 -m venv venv
source venv/bin/activate

2. Install DependenciesInstall all the required libraries using the requirements.txt file.pip install -r requirements.txt

3. Download ChromeDriverThis project uses Selenium to control Google Chrome.Check your Chrome version: Go to Settings > About Chrome.

4. Download the matching ChromeDriver: Go to the Chrome for Testing dashboard and download the correct version for your operating system.

5. Place the driver: Unzip the downloaded file and place the chromedriver.exe (or chromedriver on macOS/Linux) file in the root directory of this project.

6. Configure the ScriptOpen the main.py file and update the CONFIGURATION section at the top:ENABLE_SCHEDULE: Set to True to run daily, or False to run only once.

7. SENDER_EMAIL: Your Gmail address.SENDER_PASSWORD: Your 16-character Google App Password.RECEIVER_EMAIL: The email address where you want to receive the digest.

UsageTo run the script, simply execute the main.py file from your terminal:python main.py

If ENABLE_SCHEDULE is False, the script will run once and then exit.If ENABLE_SCHEDULE is True, 

the script will run once immediately for testing and then continue running in the background to trigger again at the scheduled time (default is 8:00 AM daily). 
Press Ctrl+C to stop the scheduler.
