import React, { useState, useEffect } from 'react';
import { Typography, Box, MenuItem, FormControl, Select, InputLabel, Input, ToggleButtonGroup, ToggleButton, Button } from "@mui/material";
import styled from '@emotion/styled';

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

const fetchOrderStats = async () => {
  try {
    const response = await fetch('http://localhost:5000');
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    const data = await response.json();
    return data; // Assuming data contains fields like { totalAsks: number, largestBid: number }
  } catch (error) {
    console.error('Error fetching order stats:', error);
  }
}

const submitAskOrder = async (price, size) => {
  const order = {
    price: price,
    size: size, // Size is assumed to be a part of the order, based on your frontend
    // Other fields as required by your backend
  };

  try {
    const response = await fetch('http://localhost:5000', {
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
  useEffect(() => {
    fetchOrderStats().then(stats => {
      if (stats) {
        // Update your state or UI with the fetched stats
        console.log('Total asks:', stats.totalAsks);
        console.log('Largest bid:', stats.largestBid);
      }
    });
  }, []);

  const [price, setPrice] = useState('');
  const [size, setSize] = useState('');


  const handleSubmit = () => {
    // Assuming you have state variables for price and size
    submitAskOrder(price, size).then(response => {
      // Handle response, maybe clear the form or show a success message
      console.log('Order submitted:', response);
    });
    setPrice('');
    setSize('');
  }
  
  const [alignment, setAlignment] = useState('left');

  const handleAlignment = (event, newAlignment) => {
    setAlignment(newAlignment);
  };

  return (
    <Root>
    <Container>
      <Typography variant="subtitle1" gutterBottom>
        Inventory is High, Act Fast - There are {price} asks on this item.
      </Typography>
      <Typography variant="h6">Size: US XL</Typography>
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
        <Input id="price" style={{marginBottom: '2Rem'}} startAdornment={<Typography variant="h6">$</Typography>} />
      </FormControl>
      <FormControl fullWidth>
        <InputLabel id="ask-expiration-label">Ask Expiration</InputLabel>
        <Select
          labelId="ask-expiration-label"
          defaultValue={30}
        >
          <MenuItem value={30}>30 Days</MenuItem>
          <MenuItem value={60}>60 Days</MenuItem>
          <MenuItem value={90}>90 Days</MenuItem>
        </Select>
      </FormControl>
      <Box display="flex" justifyContent="space-between" my={2}>
        <Button variant="text" style={{color: 'black'}}>Cancel</Button>
        <Button variant="contained" color="grey" onClick={handleSubmit}>
          Submit
        </Button>
      </Box>
    </Container>
    </Root>
  );
};

export default AskOrder;
