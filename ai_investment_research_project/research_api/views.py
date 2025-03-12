from rest_framework.decorators import api_view
from rest_framework.response import Response
from .scraping import scrape_stock_price, scrape_market_cap, scrape_pe_ratio

@api_view(['GET'])
def hello_world(request):
    return Response({"message": "Hello, world!"})

@api_view(['GET'])
def get_stock_price_view(request):
    ticker = request.GET.get('ticker', 'AAPL')
    price = scrape_stock_price(ticker)

    if price:
        return Response({"ticker": ticker, "price": price})
    else:
        return Response({"error": "Could not retrieve stock price"}, status=400)

@api_view(['GET'])
def get_market_cap_view(request):
    ticker = request.GET.get('ticker', 'AAPL')
    market_cap = scrape_market_cap(ticker)

    if market_cap:
        return Response({"ticker": ticker, "Market Cap (intraday)": market_cap})
    else:
        return Response({"error": "Could not retrieve market capitalization"}, status=400)

@api_view(['GET'])
def get_pe_ratio_view(request):
    ticker = request.GET.get('ticker', 'AAPL')
    pe_ratio = scrape_pe_ratio(ticker)

    if pe_ratio:
        return Response({"ticker": ticker, "PE Ratio (TTM)": pe_ratio})
    else: 
        return Response({"error": "Could not retrieve PE ratio"}, status=400)
