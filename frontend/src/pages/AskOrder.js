import React, { useState, useEffect } from 'react';
import { useHistory } from 'react-router-dom/cjs/react-router-dom.min';
import uclaAskImage from '../images/UCLA_ASK.jpg';
import {InputAdornment, Typography, Box, MenuItem, FormControl, Select, InputLabel, Input, ToggleButtonGroup, ToggleButton, Button } from "@mui/material";
import styled from '@emotion/styled';

const Root = styled.div`
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh; 
  width: 100vw; 
  background-image: url(${uclaAskImage});
  background-size: cover;
  background-position: center;
`;

const Container = styled.div`
  width: 50%;
  max-width: 600px;
  margin: 0;
  padding: 16px;
  box-shadow: 0px 3px 6px #00000029;
  border-radius: 4px;
  background-color: rgba(255, 255, 255, 0.5);
  backdrop-filter: blur(8px);
`;

const ToggleContainer = styled.div`
  display: flex;
  justifyContent: center;
  alignItems: ;center;
  margin: 0 auto;
  width: 100%;
  marginBottom: 2Rem;
  marginTop: 1.2Rem;
`;

const StyledToggleButtonGroup = styled(ToggleButtonGroup)`
  .MuiToggleButtonGroup-grouped {
    margin: 8px;
    border: none;
    &:not(:first-child) {
      border-radius: 20px;
    }
    &:first-child {
      border-radius: 20px;
    }
    display: flex;
    justify-content: center;
    height: 2.4rem;
    width: 18rem;
  }
`;

const StyledToggleButton = styled(ToggleButton)`
  border: 1px solid #c4c4c4;
  &.Mui-selected {
    background-color: #000;
    color: #fff;
    &:hover {
      background-color: #000;
    }
  }
  text-align: center;
  line-height: 40px;
`;

const StyledInput = styled(Input)({
  fontSize: '1.25rem', // Adjust the font size as needed, '1.25rem' is similar to h6
});

const fetchOrderStats = async () => {
  try {
    const response = await fetch('/order/list_all_order', { // Adjust the URL to where your orders are fetched from
      method: 'GET',
      credentials: 'include',
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    const orders = await response.json();
    
    // Process orders to calculate stats
    let askCount = 0;
    let largestBidPrice = 10;

    orders.forEach(order => {
      if (order.side === 'ASK' && order.is_matched !== true) {
        askCount++;
      }
      if (order.side === 'BID' && order.price > largestBidPrice && order.is_matched !== true) {
        largestBidPrice = order.price;
      }
    });

    return { totalAsks: askCount, largestBid: largestBidPrice || 0 };
  } catch (error) {
    console.error('Error fetching order stats:', error);
  }
};


const submitAskOrder = async (price, size) => {
  const order = {
    price: price,
    size: size, // Size is assumed to be a part of the order, based on your frontend
    // Other fields as required by your backend
    side: 'ASK',
  };

  try {
    const response = await fetch('/order/create_order', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(order),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    console.error('Error submitting ask order:', error);
  }
}





const AskOrder = () => {
  const [price, setPrice] = useState(10);
  const [size, setSize] = useState('');

  const [totalAsks, setTotalAsks] = useState(0);
  const [largestBid, setLargestBid] = useState(10);
  const [alignment, setAlignment] = useState('left');

  const history = useHistory();

  const handleCancel = () => {
    history.push('/');
  };

  const handleSubmit = () => {
    const intPrice = parseInt(price, 10);
    if (!isNaN(intPrice)) {
      submitAskOrder(intPrice, size).then(response => {
        alert('Successfully created order!');
        history.push('/');
      }).catch(error => {
        console.error('Error submitting ask order:', error);
      });
    
      setPrice('');
      setSize('');
    } else {
      console.error('Invalid price value');
    }
  }
  

  const handleAlignment = (event, newAlignment) => {
    setAlignment(newAlignment);
  };

  useEffect(() => {
    fetchOrderStats().then(stats => {
      if (stats) {
        setTotalAsks(stats.totalAsks);
        setLargestBid(stats.largestBid);
        // Now you have totalAsks and largestBid to use in your UI
      }
      if (alignment === 'right') { // 'right' corresponds to 'Sell Now'
        setPrice(largestBid); // Set price to the largest bid
      } else {
        setPrice(0);
      }
    });
  }, [alignment, largestBid]);
  

  return (
    <Root>
    <Container>
      <Typography variant="subtitle1" gutterBottom>
        Inventory is High, Act Fast - There are {totalAsks} asks for the swipes!
      </Typography>
      <ToggleContainer> {/* Wrap your StyledToggleButtonGroup with a div */}
      <StyledToggleButtonGroup
        size="large"
        value={alignment}
        exclusive
        onChange={handleAlignment}
        aria-label="text alignment"
      >
        <StyledToggleButton value="left" aria-label="left aligned">
          Place Ask
        </StyledToggleButton>
        <StyledToggleButton value="right" aria-label="right aligned">
          Sell Now
        </StyledToggleButton>
      </StyledToggleButtonGroup>
    </ToggleContainer>
      <FormControl fullWidth>
        <InputLabel htmlFor="price">Price</InputLabel>
        <StyledInput
          id="price"
          type="number"
          value={price}
          onChange={(e) => setPrice(e.target.value)}
          startAdornment={
            <InputAdornment position="start">
              <Typography variant="h6">$</Typography>
            </InputAdornment>
          }
        />
      </FormControl>
      <Box display="flex" justifyContent="space-between" my={2}>
        <Button variant="text" style={{color: 'black'}} onClick={handleCancel}>Cancel</Button>
        <Button variant="contained" color="grey" onClick={handleSubmit}>
          Submit
        </Button>
      </Box>
    </Container>
    </Root>
  );
};

export default AskOrder;
