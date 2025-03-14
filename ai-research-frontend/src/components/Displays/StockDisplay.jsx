import React, { useState, useEffect } from "react";
import useShowToast from "../../hooks/useShowToast";

function StockDisplay({ ticker }) {
  const [stockData, setStockData] = useEffect(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const showToast = useShowToast();

  useEffect(() => {
    async function fetchData() {
      setLoading(true);
      setError(null);

      try {
        const response = await fetch(`/api/basic-research/?ticker=${ticker}`);
        if (!response.ok) {
          throw new Error("Failed to fetch data");
        }
        const data = await response.json();
        setStockData(data);
      } catch (error) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    }
    fetchData();
  }, [ticker]);

  if (loading) {
    return (
      <Box textAlign="center" py={10}>
        <Spinner size="xl" />
      </Box>
    );
  }

  if (error) {
    return (
      <Alert status="error" variant="left-accent">
        <AlertIcon />
        {error}
      </Alert>
    );
  }

  if (!stockData) {
    return null;
  }

  const timestamp = new Date(stockData.last_updated);
  const localTimeString = timestamp.toLocaleString();

  return (
    <Box p={4} borderWidth="1px" borderRadius="md">
      <Heading size="lg" mb={4}>
        {stockData.ticker} - Stock Research
      </Heading>
      <Grid templateColumns="repeat(2, 1fr)" gap={6}>
        <GridItem>
          <VStack align="start" spacing={2}>
            <Text fontWeight="bold">Stock Price:</Text>
            <Text>{stockData.stock_price}</Text>
            <Text fontWeight="bold">Market Cap:</Text>
            <Text>{stockData.market_cap}</Text>
            <Text fontWeight="bold">P/E Ratio:</Text>
            <Text>{stockData.pe_ratio}</Text>
          </VStack>
        </GridItem>
        <GridItem>
          <VStack align="start" spacing={2}>
            <Text fontWeight="bold">Last Updated:</Text>
            <Text>{localTimeString}</Text>
            <Text fontWeight="bold">Summary:</Text>
            <Text>{stockData.summary}</Text>
          </VStack>
        </GridItem>
      </Grid>
    </Box>
  );
}

export default StockDisplay;
