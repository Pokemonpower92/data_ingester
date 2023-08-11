"""Constants for the EDGAR api"""
COMPANY_TICKER_URL = "https://www.sec.gov/files/company_tickers.json"
SUBMISSIONS_ZIP_URL = "https://www.sec.gov/Archives/edgar/daily-index/bulkdata/submissions.zip"
SUBMISSION_URL = "https://data.sec.gov/submissions/CIK{}.json"

DAILY_INDEX = "edgar/daily-index"
COMPANY_TICKERS = "files/company_tickers.json"
SESSION = "submissions/CIK{}.json"

CIK_LENGTH = 10

WEBSITE = "google.com"
EMAIL = "thisaintreal3456322891345@gmail.com"
HEADERS = {"User-Agent": f"{WEBSITE} {EMAIL}"}

# Cache constants
COMPANY_TICKER_KEY = "company_tickers"
