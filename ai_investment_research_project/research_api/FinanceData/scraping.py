import requests
from bs4 import BeautifulSoup
from ..models import StockResearchData

def scrape_stock_price(ticker_symbol):
    url = f"https://finance.yahoo.com/quote/{ticker_symbol}"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0'} 
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        price_element = soup.find('span', class_=['base', 'yf-ipw1h0'], attrs={'data-testid': 'qsp-price'})

        if price_element:
            price_text = price_element.text.strip()
            return price_text
        else:
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error during scraping: {e}")
        return None
    

def scrape_market_cap(ticker_symbol):
    url = f"https://finance.yahoo.com/quote/{ticker_symbol}"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0'} 
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        market_cap_element = soup.find('fin-streamer', class_='yf-1jj98ts', attrs={'data-field': 'marketCap'})

        if market_cap_element:
            market_cap = market_cap_element.text.strip()
            return market_cap
        else:
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error during scraping: {e}")
        return None
    
def scrape_pe_ratio(ticker_symbol):
    url = f"https://finance.yahoo.com/quote/{ticker_symbol}"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0'} 
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        pe_ratio_element = soup.find('fin-streamer', class_='yf-1jj98ts', attrs={'data-field': 'trailingPE'})

        if pe_ratio_element:
            pe_ratio = pe_ratio_element.text.strip()
            return pe_ratio
        else:
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error during scraping: {e}")
        return None
    

def scrape_stock_data(ticker_symbol):
    url = f"https://finance.yahoo.com/quote/{ticker_symbol}"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0'} 

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        price_element = soup.find('span', class_=['base', 'yf-ipw1h0'], attrs={'data-testid': 'qsp-price'})
        price = price_element.text.strip()
        market_cap_element = soup.find('fin-streamer', class_='yf-1jj98ts', attrs={'data-field': 'marketCap'})
        market_cap = market_cap_element.text.strip()
        pe_ratio_element = soup.find('fin-streamer', class_='yf-1jj98ts', attrs={'data-field': 'trailingPE'})
        pe_ratio = pe_ratio_element.text.strip()


        return {
            'stock_price': price,
            'market_cap': market_cap,
            'pe_ratio': pe_ratio,
        }
    except requests.exceptions.RequestException as e:
        print(f"Error during scraping: {e}")
        return None
    except AttributeError as e:
        print(f"Error parsing HTML: {e}")
        return None