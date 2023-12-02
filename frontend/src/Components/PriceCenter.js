import {
  Box,
  Button,
  Drawer,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Typography,
  Paper,
} from '@mui/material';
import React, { useEffect, useState } from 'react';
import PriceChart from './PriceChart';

const PriceCenter = ({ orders }) => {
  const [lastSale, setLastSale] = useState(-1);
  const [averagePrice, setAveragePrice] = useState(-1);
  const [priceChange, setPriceChange] = useState(-1);
  const [priceChangePercentage, setPriceChangePercentage] = useState(-1);

  const [open, setOpen] = useState(false);
  const [filteredOrders, setFilteredOrders] = useState([]);

  useEffect(() => {
    if (orders.length > 0) {
      setLastSale(orders[orders.length - 1].price);

      let total = 0;
      orders.forEach((order) => {
        total += order.price;
      });
      setAveragePrice(total / orders.length);

      const change = lastSale - averagePrice;
      setPriceChange(change);
      const changePercentage = (change / averagePrice) * 100;
      setPriceChangePercentage(changePercentage);
    }
  }, [averagePrice, lastSale, orders]);

  const handleOpen = (type) => {
    let filtered;
    switch (type) {
      case 'ask':
        filtered = orders.filter(
          (order) => order.side === 'ASK' && order.is_matched === false
        );
        break;
      case 'bid':
        filtered = orders.filter(
          (order) => order.side === 'BID' && order.is_matched === false
        );
        break;
      case 'sale':
        filtered = orders.filter((order) => order.is_matched === true);
        break;
      default:
        filtered = [];
    }
    setFilteredOrders(filtered);
    setOpen(true);
  };

  const handleClose = () => {
    setOpen(false);
  };

  return (
    <>
      <Box
        sx={{
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
        }}
      >
        <Typography variant="subtitle1">Last Sale: ${lastSale}</Typography>
        <Typography variant="subtitle1">
          Average Price: ${averagePrice.toFixed(1)}
        </Typography>
        <Box
          sx={{
            color: 'red',
            display: 'flex',
            alignItems: 'center',
            gap: 0.5,
          }}
        >
          <Typography variant="subtitle1">
            {priceChange > 0 ? '↑' : '↓'}
          </Typography>
          <Typography variant="subtitle1">
            {priceChange < 0 ? '-' : ''}${Math.abs(priceChange.toFixed(1))} (
            {priceChange < 0 ? '-' : ''}
            {Math.abs(priceChangePercentage.toFixed(1))}%)
          </Typography>
        </Box>
      </Box>
      <PriceChart orders={orders} />
      <Box
        sx={{
          display: 'flex',
          justifyContent: 'space-between',
        }}
      >
        <Button variant="text" onClick={() => handleOpen('ask')}>
          View Asks
        </Button>
        <Button variant="text" onClick={() => handleOpen('bid')}>
          View Bids
        </Button>
        <Button variant="text" onClick={() => handleOpen('sale')}>
          View Sales
        </Button>
        <Drawer anchor="right" open={open} onClose={handleClose}>
          <TableContainer component={Paper}>
            <Table sx={{ minWidth: 650 }} aria-label="simple table">
              <TableHead>
                <TableRow>
                  <TableCell>
                    <Typography variant="h7" fontWeight="fontWeightBold">
                      Date
                    </Typography>
                  </TableCell>
                  <TableCell>
                    <Typography variant="h7" fontWeight="fontWeightBold">
                      Time
                    </Typography>
                  </TableCell>
                  <TableCell>
                    <Typography variant="h7" fontWeight="fontWeightBold">
                      Price
                    </Typography>
                  </TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {filteredOrders.length > 0 ? (
                  filteredOrders.map((order) => {
                    const date = new Date(order.posted);
                    return (
                      <TableRow key={order._id}>
                        <TableCell>{date.toLocaleDateString()}</TableCell>
                        <TableCell>{date.toLocaleTimeString()}</TableCell>
                        <TableCell>{order.price}</TableCell>
                      </TableRow>
                    );
                  })
                ) : (
                  <TableRow>
                    <TableCell colSpan={3}>No orders to display</TableCell>
                  </TableRow>
                )}
              </TableBody>
            </Table>
          </TableContainer>
        </Drawer>
      </Box>
    </>
  );
};

export default PriceCenter;
