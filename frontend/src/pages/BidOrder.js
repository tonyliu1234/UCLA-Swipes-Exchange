import React, { useState, useEffect } from 'react';
import styled from '@emotion/styled';
import { Button, Box, MenuItem, FormControl, Select, InputLabel, TextField, Typography, ToggleButtonGroup, ToggleButton } from '@mui/material';

const Root = styled.div`
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  width: 100vw;
  background-image: url(https://source.unsplash.com/random?wallpapers);
  background-size: cover;
  background-position: center;
`;

const Container = styled(Box)`
  padding: 16px;
  margin: 16px;
  width: 34rem;
  box-shadow: 0px 3px 6px #00000029;
  border-radius: 4px;
  background-color: rgba(255, 255, 255, 0.5);
  backdrop-filter: blur(8px);
`;

const ToggleContainer = styled.div`
  display: flex;
  justify-content: center;
  align-items: center;
  margin: 0 auto;
  width: 100%;
  margin-bottom: 2rem;
  margin-top: 1.2rem;
`;

const StyledToggleButton = styled(ToggleButton)`
  border: 1px solid #c4c4c4;
  margin: 0px;
  text-align: center;
  line-height: 40px;
  &:not(:first-child) {
    border-left: 1px solid #c4c4c4;
  }
  &.Mui-selected {
    background-color: #000;
    color: white;
  }
`;

const fetchBidStats = async () => {
    try {
      const response = await fetch('http://localhost:5000/orders', {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
      });
  
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const orders = await response.json();
  
      let bidCount = 0;
      let lowestAskPrice = Infinity;
  
      orders.forEach(order => {
        if (order.side === 'BID') {
          bidCount++;
        }
        if (order.side === 'ASK' && order.price < lowestAskPrice) {
          lowestAskPrice = order.price;
        }
      });
  
      return { totalBids: bidCount, lowestAsk: lowestAskPrice === Infinity ? 0 : lowestAskPrice };
    } catch (error) {
      console.error('Error fetching bid stats:', error);
    }
  };
  

const BidOrder = () => {
    const [totalBids, setTotalBids] = useState(0);
    const [lowestAsk, setLowestAsk] = useState(0);
    const [currentPrice, setCurrentPrice] = useState(null);
    const [selectedPrice, setSelectedPrice] = useState(null);

    const handlePriceSelection = (event, newPrice) => {
        setSelectedPrice(newPrice);
    };
    
    useEffect(() => {
      fetchBidStats().then(stats => {
        if (stats) {
          setTotalBids(stats.totalBids);
          setLowestAsk(stats.lowestAsk);
        }
      });
    }, []);
    
    useEffect(() => {
      if (selectedPrice === 70) { // Assuming 70 is the 'Buy Now' price
        setCurrentPrice(lowestAsk);
      } else if (selectedPrice === 51 || selectedPrice === 56) { // Good Bid or Better Bid
        setCurrentPrice(selectedPrice);
      }
    }, [selectedPrice, lowestAsk]);

    const handleSubmit = async () => {
        // Assuming you have a state variable for the bid price and expiration
        const bidOrder = {
          price: currentPrice,
          owner_id: 'ownerId', // You need to get the actual owner's ID
          side: 'BID',
          // Include other necessary fields
        };
      
        try {
          const response = await fetch('http://localhost:5000/orders', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify(bidOrder),
          });
      
          if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
          }
      
          // Handle the response, e.g., showing a success message
        } catch (error) {
          console.error('Error submitting bid order:', error);
        }
      };
    

  return (
    <Root>
      <Container>
        <Typography variant="subtitle1" gutterBottom>
          High Demand - {totalBids} people are interested in this product
        </Typography>
        <Typography variant="h6">Size: US XL</Typography>
        <ToggleContainer>
          <ToggleButtonGroup
            value={selectedPrice}
            exclusive
            onChange={handlePriceSelection}
            aria-label="price selection"
            style={{ justifyContent: 'center' }}
          >
            <StyledToggleButton value={51} aria-label="good bid">
              $51 Good Bid
            </StyledToggleButton>
            <StyledToggleButton value={56} aria-label="better bid">
              $56 Better Bid
            </StyledToggleButton>
            <StyledToggleButton value={70} aria-label="buy now">
              ${lowestAsk} Buy Now
            </StyledToggleButton>
          </ToggleButtonGroup>
        </ToggleContainer>
        <TextField label="Or Name Your Price" style={{ marginBottom: '2rem' }} value={currentPrice || ''} fullWidth margin="normal" onChange={e => setCurrentPrice(e.target.value)} />
        <FormControl fullWidth>
          <InputLabel>Bid Expiration</InputLabel>
          <Select defaultValue={30}>
            <MenuItem value={30}>30 Days</MenuItem>
            <MenuItem value={60}>60 Days</MenuItem>
            <MenuItem value={90}>90 Days</MenuItem>
          </Select>
        </FormControl>
        <Box display="flex" justifyContent="space-between" my={2}>
          <Button variant="text" style={{color: 'black'}}>Cancel</Button>
          <Button variant="contained" color="grey" onClick={handleSubmit}>
            Place Bid
          </Button>
        </Box>
      </Container>
    </Root>
  );
};

export default BidOrder;
