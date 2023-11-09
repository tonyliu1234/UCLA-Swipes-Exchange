import React from 'react';
import ActionCard from '../Components/ActionCard';
import { Box, Divider, Typography } from '@mui/material';
import PriceCenter from '../Components/PriceCenter';
import { grey } from '@mui/material/colors';

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
      <Box marginBottom={2}>
        <Typography variant="h3">SwipeX</Typography>
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
