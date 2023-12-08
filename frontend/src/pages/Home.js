import React, { useEffect, useState } from 'react';
import ActionCard from '../Components/ActionCard';
import { Box, Divider, IconButton, Typography } from '@mui/material';
import PriceCenter from '../Components/PriceCenter';
import { grey } from '@mui/material/colors';
import AccountCircle from '@mui/icons-material/AccountCircle';

const apiUrl =
  process.env.REACT_APP_API_URL === undefined
    ? ''
    : process.env.REACT_APP_API_URL;

const fetchOrders = async () => {
  try {
    const response = await fetch(`${apiUrl}/order/list_all_order`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    const orders = await response.json();

    return orders;
  } catch (error) {
    console.error('Error fetching order stats:', error);
  }
};

const Home = () => {
  const [orders, setOrders] = useState([]);

  useEffect(() => {
    fetchOrders().then((data) => {
      if (data) {
        setOrders(data);
        // Now you have totalAsks and largestBid to use in your UI
      }
    });
  }, []);

  return (
    <Box
      sx={{
        display: 'flex',
        flexDirection: 'column',
        p: 2,
        gap: 2,
        maxWidth: 500,
        mx: 'auto', // centers the box
        marginTop: 10,
      }}
    >
      <Box
        sx={{
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
        }}
      >
        <Typography variant="h3">SwipeX</Typography>
        <IconButton
          onClick={() => {
            window.location.href = '/userProfile';
          }}
        >
          <AccountCircle sx={{ fontSize: '2rem' }} />
        </IconButton>
      </Box>
      <Box marginBottom={2}>
        <Box marginY={1}></Box>
        <Typography variant="h6" color={grey['600']}>
          UCLA Meal Swipe Exchange Center{' '}
        </Typography>
      </Box>
      <ActionCard orders={orders} />
      <Box marginY={2}>
        <Divider />
      </Box>
      <PriceCenter orders={orders} />
    </Box>
  );
};

export default Home;
