import React, { useState, useEffect } from 'react';
import { useHistory } from 'react-router-dom/cjs/react-router-dom.min';
import styled from '@emotion/styled';
import uclaBidImage from '../images/UCLA_BID.jpg';
import { Button, Box, MenuItem, FormControl, Select, InputLabel, TextField, Typography, ToggleButtonGroup, ToggleButton } from '@mui/material';

const Root = styled.div`
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  width: 100vw;
  background-image: url(${uclaBidImage});
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
      const response = await fetch('/order/list_all_order', {
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
      let bidPrices = [];
      orders.forEach(order => {
        if (order.side === 'BID' && order.is_matched !== true) {
          bidCount++;
          bidPrices.push(order.price)
        }
        console.log(order.price)
        if (order.side === 'ASK' && order.price < lowestAskPrice) {
          lowestAskPrice = order.price;
        }
      });
      bidPrices.sort((a, b) => a - b);
      const goodBid = calculatePercentile(bidPrices, 50);
      const betterBid = calculatePercentile(bidPrices, 70);
  
      return { 
        totalBids: bidCount, 
        lowestAsk: lowestAskPrice === Infinity ? 10 : lowestAskPrice,
        goodBid: goodBid === null ? 10 : goodBid,
        betterBid: betterBid === null ? 10 : betterBid 
      };
    } catch (error) {
      console.error('Error fetching bid stats:', error);
    }
  };

  const calculatePercentile = (sortedPrices, percentile) => {
    if (sortedPrices.length === 0) {
      return null;
    }
    const index = Math.ceil(percentile / 100.0 * sortedPrices.length) - 1;
    return sortedPrices[index];
  };
  

const BidOrder = () => {
    const [totalBids, setTotalBids] = useState(0);
    const [lowestAsk, setLowestAsk] = useState(0);
    const [goodBid, setGoodBid] = useState(10);
    const [betterBid, setBetterBid] = useState(10);
    const [currentPrice, setCurrentPrice] = useState(null);
    const [selectedPrice, setSelectedPrice] = useState(null);

    const history = useHistory();
  
    const handleCancel = () => {
      history.push('/'); // Navigate to the root or another desired route
    };

    const handlePriceSelection = (event, newValue) => {
      const price = newValue.split('-')[1];
      setSelectedPrice(newValue);
      setCurrentPrice(price);
    };
    
    
    useEffect(() => {
      fetchBidStats().then(stats => {
        if (stats) {
          setTotalBids(stats.totalBids);
          setLowestAsk(stats.lowestAsk);
          setGoodBid(stats.goodBid);
          setBetterBid(stats.betterBid);
          setSelectedPrice(stats.lowestAsk);
          const lowestPriceValue = Math.min(stats.lowestAsk, stats.goodBid, stats.betterBid);
          let initialSelection;
          if (lowestPriceValue === stats.lowestAsk) {
            initialSelection = `buy-${stats.lowestAsk}`;
          } else if (lowestPriceValue === stats.goodBid) {
            initialSelection = `good-${stats.goodBid}`;
          } else {
            initialSelection = `better-${stats.betterBid}`;
          }

          setSelectedPrice(initialSelection);
          setCurrentPrice(initialSelection.split('-')[1]);
        }
      });
    }, []);
    
    useEffect(() => {
      if (selectedPrice === lowestAsk) {
        setCurrentPrice(lowestAsk);
      } else if (selectedPrice === goodBid || selectedPrice === betterBid) { // Good Bid or Better Bid
        setCurrentPrice(selectedPrice);
      }
    }, [selectedPrice, lowestAsk]);

    const handleSubmit = () => {
      const intPrice = parseInt(currentPrice, 10);
      if (!isNaN(intPrice)) {
        submitBidOrder(intPrice).then(response => {
          alert('Successfully created order!');
          history.push('/');
        }).catch(error => {
          console.error('Error submitting bid order:', error);
        });
      } else {
        console.error('Invalid price value');
      }
    }

    const submitBidOrder = async (price) => {
        // Assuming you have a state variable for the bid price and expiration
        const bidOrder = {
          price: price,
          owner_id: 'ownerId', // You need to get the actual owner's ID
          side: 'BID',
          // Include other necessary fields
        };
      
        try {
          const response = await fetch('/order/create_order', {
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
          High Demand - {totalBids} bids are there!
        </Typography>
        <ToggleContainer>
          <ToggleButtonGroup
            value={selectedPrice}
            exclusive
            onChange={handlePriceSelection}
            aria-label="price selection"
            style={{ justifyContent: 'center' }}
          >
            <StyledToggleButton value={`good-${goodBid}`} aria-label="good bid">
              ${goodBid} Good Bid
            </StyledToggleButton>
            <StyledToggleButton value={`better-${betterBid}`} aria-label="better bid">
              ${betterBid} Better Bid
            </StyledToggleButton>
            <StyledToggleButton value={`buy-${lowestAsk}`} aria-label="buy now">
              ${lowestAsk} Buy Now
            </StyledToggleButton>
          </ToggleButtonGroup>
        </ToggleContainer>
        <TextField label="Or Name Your Price" style={{ marginBottom: '2rem' }} value={currentPrice || ''} fullWidth margin="normal" onChange={e => setCurrentPrice(e.target.value)} />
        <Box display="flex" justifyContent="space-between" my={2}>
          <Button variant="text" style={{color: 'black'}} onClick={handleCancel}>Cancel</Button>
          <Button variant="contained" color="grey" onClick={handleSubmit}>
            Place Bid
          </Button>
        </Box>
      </Container>
    </Root>
  );
};

export default BidOrder;
