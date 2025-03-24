# Investment Research Co-Pilot

<div align="center">
  <h2 align="center">Northstar Co-Pilot</h1>
  <p align="center">
    Leveraging AI for next-generation research
  </p>
</div>

## About The Project

![copilotpreview](https://github.com/user-attachments/assets/cd5641ab-2078-45e7-91b6-157e5663e87d)

This application utilizes an autonomous multi-agent architecture to create an investment reserach co-pilot. 
Equipped with real-time information and accurate financial data, Northstar is designed to assist you in your search of equities, markets, and more. 

This project is part of Grad 5900: Applied Generative AI at the University of Connecticut-Storrs.


## Getting Started

To get a local copy up and running follow these simple example steps.

### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/heraldpark15/Investment-Research-AI
   ```
2. Get an API key for Claude Sonnet 3.7 by Anthropic [[https://www.anthropic.com/api](https://www.anthropic.com/api)]
3. Enter your Claude API in `.env` in /ai_investment_research/research_api
   ```py
   ANTHROPIC_API_KEY = 'ENTER YOUR API'
   ```
4. Get a Polygon API key for financial data [[https://polygon.io/](https://polygon.io/)]
5. Enter your Polygon API key in `.env` in /ai_investment_research/research_api
   ```py
   POLYGON_API_KEY = 'ENTER YOUR API'
   ```
6. Get a Tavily API key for real-time web search [[https://tavily.com/](https://tavily.com/)]
7. Enter your Tavily API key in  `.env` in /ai_investment_research/research_api
   ```py
   TAVILY_API_KEY = 'ENTER YOUR API'
   ```
9. Start Django server from /ai_investment_research
    ```py
    python manage.py runserver
    ```
10. Start React frontend from /ai-research-frontend
    ```sh
    npm start
    ```
11. Enjoy!

## Tools Utilized

- Claude Sonnet 3.7
- Polygon.io API
- Tavily API
- Python
- JavaScript
- React
- Django
- LangGraph
- Chakra UI

## Creator
[Herald Park](https://www.linkedin.com/in/heraldpark/)
