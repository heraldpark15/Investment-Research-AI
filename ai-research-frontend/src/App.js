import React, { useState } from "react";
import "./App.css";
import { ChakraProvider } from "@chakra-ui/react"

function TickerInput({ onTickerSubmit }) {
  const [ticker, setTicker] = useState("");

  const handleInputChange = (event) => {
    setTicker(event.target.value.toUpperCase());
  };

  const handleSubmit = () => {
    if (ticker.trim() !== "") {
      onTickerSubmit(ticker);
    } else {
      alert("Please enter a ticker symbol. ");
    }
  };

  return (
    <div>
      <input
        type="Text"
        placeholder="Enter Ticker Symbol (e.g. AAPL)"
        value={ticker}
        onChange={handleInputChange}
      ></input>
      <button onClick={handleSubmit}>Get Research</button>
    </div>
  );
}

function ResearchDisplay({ researchData, loading }) {
  return (
    <div>
      <h2>Research Results</h2>
      {loading ? (
        <p>Loading research data...</p>
      ) : researchData ? (
        <div>
          <p>
            <strong>Ticker:</strong> {researchData.ticker}
          </p>
          <p>
            <strong>Stock Price:</strong> {researchData.stock_price}
          </p>
          <p>
            <strong>Market Capitalization:</strong> {researchData.market_cap}
          </p>
          <p>
            <strong>P/E Ratio:</strong> {researchData.pe_ratio}
          </p>
          <p>
            <strong>Summary:</strong> {researchData.summary}
          </p>
          {researchData.error && (
            <p className="error">
              <strong>Error:</strong> {researchData.error}
            </p>
          )}
        </div>
      ) : (
        <p>Enter a ticker symbol and click 'Get Research' to see results.</p>
      )}
    </div>
  );
}

function App() {
  const [researchData, setResearchData] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleTickerSubmit = async (ticker) => {
    setResearchData(null);
    setLoading(true);

    try {
      const response = await fetch(`http://127.0.0.1:8000/api/basic-research/?ticker=${ticker}`);

      if (!response.ok) {
        const errorData = await response.json();
        let errorMessage = `API Error: ${response.status} ${response.statusText}`;

        if (errorData && errorData.detail) {
          errorMessage += ` - ${errorData.detail}`;
        }

        throw new Error(errorMessage);
      }

      const data = await response.json();

      setResearchData(data);
    } catch (error) {
      console.error("Error fetching research data: ", error);
      setResearchData({ error: error.errorMessage });
    } finally {
      setLoading(false);
    }
  };
  return (
    <div className="App">
      <h1>AI Investment Research Tool</h1>
      <TickerInput onTickerSubmit={handleTickerSubmit} />
      <ResearchDisplay researchData={researchData} loading={loading} />
    </div>
  );
}

export default App;
