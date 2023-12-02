import React, { useEffect, useState } from 'react';
import ActionCard from '../Components/ActionCard';
import { Box, Divider, IconButton, Typography } from '@mui/material';
import PriceCenter from '../Components/PriceCenter';
import { grey } from '@mui/material/colors';
import AccountCircle from '@mui/icons-material/AccountCircle';

const mockData = [
  {
    _id: '6567264bd623ad3e4a6a0cfd',
    is_matched: false,
    owner_id: '65671a2fada3e0383290e582',
    posted: 'Wed, 29 Nov 2023 03:53:47 GMT',
    price: 9,
    side: 'BID',
  },
  {
    _id: '65672aa16d0ea2f52bfd7517',
    is_matched: false,
    owner_id: '65671a2fada3e0383290e582',
    posted: 'Wed, 29 Nov 2023 04:12:17 GMT',
    price: 8,
    side: 'ASK',
  },
  {
    _id: '65672ac0d11d51e8ec3c7cee',
    is_matched: true,
    owner_id: '65671a2fada3e0383290e582',
    posted: 'Mon, 27 Nov 2023 04:12:48 GMT',
    price: 9,
    side: 'BID',
  },
  {
    _id: '65672ad37be56623d5913458',
    is_matched: true,
    owner_id: '65671a2fada3e0383290e582',
    posted: 'Tue, 26 Nov 2023 04:13:07 GMT',
    price: 10,
    side: 'ASK',
  },
  {
    _id: '6567fe3a68e54896946c619b',
    is_matched: false,
    owner_id: '65671a2fada3e0383290e582',
    posted: 'Wed, 29 Nov 2023 19:15:06 GMT',
    price: 8,
    side: 'BID',
  },
  {
    _id: '6567ff3079af9914d23f7e65',
    is_matched: false,
    owner_id: '65671a2fada3e0383290e582',
    posted: 'Wed, 29 Nov 2023 19:19:12 GMT',
    price: 7,
    side: 'ASK',
  },
  {
    _id: '6567ff4682ab59430b3bb34a',
    is_matched: true,
    owner_id: '65671a2fada3e0383290e582',
    posted: 'Wed, 29 Nov 2023 19:19:34 GMT',
    price: 9,
    side: 'BID',
  },
];

const fetchOrders = async () => {
  try {
    // TODO: change to prod endpoint
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

    return orders;
  } catch (error) {
    console.error('Error fetching order stats:', error);
  }
};

const Home = () => {
  // const [orders, setOrders] = useState([]);

  // useEffect(async () => {
  //   const data = await fetchOrders();
  //   setOrders(data);
  // }, [fetchOrders]);

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
      <ActionCard orders={mockData} />
      <Box marginY={2}>
        <Divider />
      </Box>
      <PriceCenter orders={mockData} />
    </Box>
  );
};

export default Home;
