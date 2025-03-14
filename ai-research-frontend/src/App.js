import React, { useState } from "react";
import "./App.css";
import useShowToast from "./hooks/useShowToast";
import {
  Button,
  Input,
  Text,
  Box,
  Spinner,
  Center,
  VStack,
} from "@chakra-ui/react";
import { Toaster } from "./components/ui/toaster";
import StockPriceChart from "./components/Displays/StockPriceChart";

function TickerInput({ onTickerSubmit }) {
  const showToast = useShowToast();
  const [ticker, setTicker] = useState("");

  const handleInputChange = (event) => {
    setTicker(event.target.value.toUpperCase());
  };

  const handleSubmit = () => {
    if (ticker.trim() !== "") {
      onTickerSubmit(ticker);
    } else {
      showToast("Error", "Please enter a ticker symbol.", "error");
      return;
    }
  };

  return (
    <Box
      padding="4"
      borderWidth="1px"
      borderRadius="md"
      maxWidth="400px"
      mx="auto"
    >
      <VStack spacing={4}>
        <Input
          type="text"
          placeholder="Enter Ticker Symbol (e.g. AAPL)"
          value={ticker}
          onChange={handleInputChange}
          size="lg"
          variant="outline"
        />
        <Button
          onClick={handleSubmit}
          colorScheme="blue"
          size="lg"
          width="full"
        >
          Get Research
        </Button>
      </VStack>
    </Box>
  );
}

function ResearchDisplay({ researchData, loading }) {
  return (
    <Box
      padding="4"
      borderWidth="1px"
      borderRadius="md"
      maxWidth="600px"
      mx="auto"
    >
      <Text fontSize="2xl" fontWeight="bold" marginBottom={4}>
        Research Results
      </Text>
      {loading ? (
        <Center>
          <Spinner size="xl" />
        </Center>
      ) : researchData ? (
        <VStack spacing={4} align="flex-start">
          <Text>
            <strong>Ticker:</strong> {researchData.ticker}
          </Text>
          <Text>
            <strong>Stock Price:</strong> {researchData.stock_price}
          </Text>
          <Text>
            <strong>Market Capitalization:</strong> {researchData.market_cap}
          </Text>
          <Text>
            <strong>P/E Ratio:</strong> {researchData.pe_ratio}
          </Text>
          <Text>
            <strong>Summary:</strong> {researchData.summary}
          </Text>
          {researchData.error && (
            <Text color="red.500">
              <strong>Error:</strong> {researchData.error}
            </Text>
          )}
        </VStack>
      ) : (
        <Text>
          Enter a ticker symbol and click 'Get Research' to see results.
        </Text>
      )}
    </Box>
  );
}

function App() {
  const [researchData, setResearchData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [selectedTickerForChart, setSelectedTickerForChart] = useState(null);

  const handleTickerSubmit = async (ticker) => {
    setResearchData(null);
    setLoading(true);
    setSelectedTickerForChart(ticker);

    try {
      const response = await fetch(
        `http://127.0.0.1:8000/api/basic-research/?ticker=${ticker}`
      );

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
      setResearchData({ error: error.message });
      setSelectedTickerForChart(null);
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      <VStack
        spacing={8}
        padding="6"
        align="center"
        minHeight="100vh"
        justify="center"
      >
        <Text fontSize="3xl" fontWeight="bold" color="teal.500">
          AI Investment Research Tool
        </Text>
        <TickerInput onTickerSubmit={handleTickerSubmit} />
        <ResearchDisplay researchData={researchData} loading={loading} />
        {/* {selectedTickerForChart && <StockPriceChart ticker={selectedTickerForChart} />} */}
      </VStack>
      <Toaster />
    </>
  );
}

export default App;
