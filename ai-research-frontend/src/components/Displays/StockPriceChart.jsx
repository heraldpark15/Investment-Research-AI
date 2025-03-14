import React, { useState, useEffect } from "react";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
} from "recharts";

const StockPriceChart = ({ ticker }) => {
  const [historicalData, setHistoricalData] = useState();
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchHistoricalData = async () => {
      setLoading(true);
      setError(null);
      try {
        const response = await fetch(
          `/api/historical-stock-price/?ticker=${ticker}`
        ); // Replace with your actual API endpoint
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        setHistoricalData(data);
      } catch (e) {
        setError(e.message);
      } finally {
        setLoading(false);
      }
    };

    if (ticker) {
      fetchHistoricalData();
    }
  }, [ticker]);

  if (loading) {
    return <div>Loading stock price history...</div>;
  }

  if (error) {
    return <div>Error fetching stock price history: {error}</div>;
  }

  if (!historicalData || historicalData.length === 0) {
    return <div>No historical data available for {ticker}.</div>;
  }

  return (
    <LineChart
      width={700}
      height={300}
      data={historicalData}
      margin={{ top: 5, right: 30, left: 20, bottom: 5 }}
    >
      <CartesianGrid strokeDasharray="3 3" />
      <XAxis dataKey="timestamp" />{" "}
      {/* Assuming your data has a 'timestamp' field */}
      <YAxis />
      <Tooltip />
      <Legend />
      <Line
        type="monotone"
        dataKey="price"
        stroke="#8884d8"
        name="Stock Price"
      />{" "}
      {/* Assuming your data has a 'price' field */}
    </LineChart>
  );
};

export default StockPriceChart;
