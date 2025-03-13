from django.db import models

class StockResearchData(models.Model):
    ticker_symbol = models.CharField(max_length=10, db_index=True)  # Stock ticker, indexed for faster lookups
    stock_price = models.FloatField(null=True, blank=True)         # Stock price, allow null/blank if scraping fails
    market_cap = models.CharField(max_length=50, blank=True)      
    pe_ratio = models.CharField(max_length=20, blank=True)        
    summary = models.TextField(blank=True)                         
    research_timestamp = models.DateTimeField(auto_now_add=True)   # Timestamp, auto-set on creation

    def __str__(self):
        return f"Research Data for {self.ticker_symbol} - {self.research_timestamp}"

    class Meta:
        verbose_name_plural = "Stock Research Data" # Nicer plural name in Admin panel