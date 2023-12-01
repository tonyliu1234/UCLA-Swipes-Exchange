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
        <Button
          variant="outlined"
          onClick={() => {
            window.location.href = '/bid';
          }}
        >
          Place Bid
        </Button>
        <Typography>or</Typography>
        <Button
          variant="contained"
          color="primary"
          onClick={() => {
            window.location.href = '/bid';
          }}
        >
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
        <Button
          variant="contained"
          color="primary"
          onClick={() => {
            window.location.href = '/ask';
          }}
        >
          Sell for $7
        </Button>
        <Typography>or</Typography>
        <Button
          variant="outlined"
          onClick={() => {
            window.location.href = '/ask';
          }}
        >
          Ask for more
        </Button>
      </Box>
    </>
  );
};

export default ActionCard;
