import React from 'react';
import { Box, Button, Typography } from '@mui/material';

const ActionCard = () => {
  return (
    <>
      <Box
        sx={{
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
          marginBottom: 0.5,
        }}
      >
        <Typography>Buy a swipe:</Typography>
        <Button variant="outlined">Place Bid</Button>
        <Typography>or</Typography>
        <Button variant="contained" color="primary">
          Buy for $10
        </Button>
      </Box>
      <Box
        sx={{
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
        }}
      >
        <Typography>Sell a swipe:</Typography>
        <Button variant="contained" color="primary">
          Sell for $7
        </Button>
        <Typography>or</Typography>
        <Button variant="outlined">Ask for more</Button>
      </Box>
    </>
  );
};

export default ActionCard;
