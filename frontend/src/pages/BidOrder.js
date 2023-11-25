import React, { useState } from 'react';
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

const BidOrder = () => {
  const [selectedPrice, setSelectedPrice] = useState(null);

  const handlePriceSelection = (event, newPrice) => {
    setSelectedPrice(newPrice);
  };

  return (
    <Root>
      <Container>
        <Typography variant="subtitle1" gutterBottom>
          High Demand - 83 people are interested in this product
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
              $70 Buy Now
            </StyledToggleButton>
          </ToggleButtonGroup>
        </ToggleContainer>
        <TextField label="Or Name Your Price" style={{ marginBottom: '2rem' }} defaultValue="56" fullWidth margin="normal" />
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
          <Button variant="contained" color="grey">
            Place Bid
          </Button>
        </Box>
      </Container>
    </Root>
  );
};

export default BidOrder;
