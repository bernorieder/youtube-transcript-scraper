# youtube-transcript-scraper

## description
Since YouTube does not provide automatically generated transcripts via its API and normal scraping does not work with YT's ajaxy interface, this script uses browser automation to click through the YouTube web interface and download the transcript file.

## requirements
* a functioning webdriver environment (tested with [https://github.com/mozilla/geckodriver/releases][1]);
* the selenium package for Python;
* a CSV file with a column for video ids as input;

## use
* download script;
* enable a virtual environment (venv)
* install dependencies with `pip install -r requirements.txt`
* modify `videos.csv` with a list of videos you wish to fetch captions from. Each line should contain at least the video id and optionally the video publish date
* run the script `python captions.py`

[1]:	https://github.com/mozilla/geckodriver/releases