import React, { useEffect, useState } from 'react';
import { Box, Button, Typography } from '@mui/material';

const ActionCard = ({ orders }) => {
  const [lowestAsk, setLowestAsk] = useState(-1);
  const [highestBid, setHighestBid] = useState(-1);

  useEffect(() => {
    let minAsk = Number.MAX_VALUE;
    let maxBid = Number.MIN_VALUE;

    orders.forEach(({ price, side }) => {
      if (side === 'ASK') {
        minAsk = Math.min(minAsk, price);
      }
      if (side === 'BID') {
        maxBid = Math.max(maxBid, price);
      }
    });

    if (minAsk !== Number.MAX_VALUE) {
      setLowestAsk(minAsk);
    }
    if (maxBid !== Number.MIN_VALUE) {
      setHighestBid(maxBid);
    }
  }, [orders]);

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
          {lowestAsk === -1 ? 'No asks now' : 'Buy for $' + lowestAsk}
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
          {highestBid === -1 ? 'No bids now' : 'Sell for $' + highestBid}
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
