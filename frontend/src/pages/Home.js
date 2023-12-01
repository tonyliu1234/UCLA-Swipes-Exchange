import React from 'react';
import ActionCard from '../Components/ActionCard';
import { Box, Divider, IconButton, Typography } from '@mui/material';
import PriceCenter from '../Components/PriceCenter';
import { grey } from '@mui/material/colors';
import AccountCircle from '@mui/icons-material/AccountCircle';

const Home = () => {
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
      <ActionCard />
      <Box marginY={2}>
        <Divider />
      </Box>
      <PriceCenter />
    </Box>
  );
};

export default Home;
