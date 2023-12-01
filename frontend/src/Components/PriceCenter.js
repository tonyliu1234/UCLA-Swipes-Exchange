import { Box, Button, Typography } from '@mui/material';
import React from 'react';
import PriceChart from './PriceChart';

const PriceCenter = () => {
  return (
    <>
      <Box
        sx={{
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
        }}
      >
        <Typography variant="subtitle1">Last Sale: $8.7</Typography>
        <Box
          sx={{
            color: 'red',
            display: 'flex',
            alignItems: 'center',
            gap: 0.5,
          }}
        >
          <Typography variant="subtitle1">↓</Typography>
          <Typography variant="subtitle1">-$1.8 (-12%)</Typography>
        </Box>
      </Box>
      <PriceChart />
      <Box
        sx={{
          display: 'flex',
          justifyContent: 'space-between',
        }}
      >
        <Button variant="text">View Asks</Button>
        <Button variant="text">View Bids</Button>
        <Button variant="text">View Sales</Button>
      </Box>
    </>
  );
};

export default PriceCenter;
