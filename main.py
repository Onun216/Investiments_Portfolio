import json
import re
from pathlib import Path
from time import sleep
from urllib.request import Request, urlopen

from getuseragent import UserAgent
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from access_info import gf_api_token

ROOT_FOLDER = Path(__file__).parent
CHROMEDRIVER_EXEC = ROOT_FOLDER / 'drivers' / 'chromedriver'
CHROMEDRIVER_EXEC = '/Users/nuno/PycharmProjects/Investimentos_Portfolio/drivers/chromedriver'


# Factory
def make_chrome_browser(*options: str) -> webdriver.Chrome:
    chrome_options = webdriver.ChromeOptions()
    chrome_options.binary_location = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

    if options is not None:
        for option in options:
            chrome_options.add_argument(option)

    chrome_service = Service(
        executable_path=str(CHROMEDRIVER_EXEC),
    )

    browser = webdriver.Chrome(
        service=chrome_service,
        options=chrome_options,
    )
    browser.implicitly_wait(10)

    return browser


yahoo = 'https://finance.yahoo.com/'
consent_xpath_yahoo = '//*[@id="consent-page"]/div/div/div/form/div[2]/div[2]/button[1]'
search_box_yahoo = '//*[@id="yfin-usr-qry"]'
stock_quote = '//*[@id="quote-header-info"]/div[3]/div[1]/div[1]/fin-streamer[1]'
stock_mkt_cap = '//*[@id="quote-summary"]/div[2]/table/tbody/tr[1]/td[2]'
stock_ticker = '//*[@id="quote-header-info"]/div[2]/div[1]/div[1]/h1'

if __name__ == '__main__':
    # Use the GuruFocus API to get financial info
    # Note: For all stocks that are not traded in the US,
    # please replace {symbol} with {exchange:symbol} when calling the api. For example: ASX:ABC
    from companies import companies, choose_companies, sold_positions, companies_positions, profit_loss
    from financial_info import df, gf_choose_metric

    if choose_companies(companies()) == 'Gurufocus':
        try:
            ua = UserAgent()
            the_ua = ua.Random()
            options = (f'--disable-gpu', '--no-sandbox', '--headless={True}')
            browser = make_chrome_browser(*options)
            # US only
            ticker = input('Ticker: ').upper()

            # Show full dataframe, y/n
            see_financial_metrics = input('Ver tabela com todas as métricas disponíveis?[Y/n] ').lower()
            if see_financial_metrics == 'y':
                print(df.to_string())

            # Insert category and metric
            cat, metric = gf_choose_metric()
            url = f'https://api.gurufocus.com/public/user/{gf_api_token}/stock/{ticker}/financials'
            gf_request = Request(url, headers={'User-Agent': the_ua})
            gf_info = urlopen(gf_request).read()
            data = json.loads(gf_info.decode('utf8'))
            print(f'{metric}:')
            for info in data['financials']['annuals'][cat][metric]:
                print(info)

        except Exception as e:
            print(e)

    else:
        company_name = input('Empresa: ')
        bought = companies_positions(company_name)
        sold = sold_positions(company_name)
        profit_loss(company_name, bought, sold)
        # TIME_TO_WAIT = 60
        options = (f'--disable-gpu', '--no-sandbox', '--user-agent={user_agent}', '--headless={True}')
        browser = make_chrome_browser(*options)
        browser.get(yahoo)

        try:
            if company_name != 'ALL':
                # Accept cookies
                consent_button = browser.find_element(By.XPATH, consent_xpath_yahoo)
                consent_button.click()

                # Search company_name finance yahoo
                search_box = browser.find_element(By.XPATH, search_box_yahoo)
                search_box.send_keys(company_name)
                sleep(1)
                search_box.send_keys(Keys.ENTER)

                # Get stock ticker
                ticker_info = browser.find_element(By.XPATH, stock_ticker)
                temp_ticker = ticker_info.text.split()
                ticker = temp_ticker[-1]

                # Get stock quote, currency and mkt cap
                quote = browser.find_element(By.XPATH, stock_quote)
                temp_element = browser.find_element(By.XPATH, '//*[@id="quote-header-info"]/div[2]/div[1]/div[2]/span')
                currency = temp_element.text.split()
                mkt_cap = browser.find_element(By.XPATH, stock_mkt_cap)

                print(f'Ticker {ticker} \nCotação actual: {currency[-1]} {quote.text}')
                print(f'Capitalização de mercado: {mkt_cap.text}')

                # Remove parentheses from ticker
                usable_ticker = re.sub(r'[()]', '', ticker)
                browser.quit()

        except NoSuchElementException:
            print('Elementos não encontrados!')

        except ConnectionError:
            print('Erro de conexão!')

        except TypeError as e:
            print('Sem dados')
            browser.quit()
