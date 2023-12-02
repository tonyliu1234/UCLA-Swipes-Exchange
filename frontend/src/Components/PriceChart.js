import { blue } from '@mui/material/colors';
import React, { useEffect, useState } from 'react';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
} from 'recharts';

const PriceChart = ({ orders }) => {
  const [matchedOrders, setMatchedOrders] = useState([]);

  useEffect(() => {
    if (orders) {
      console.log(orders);
      const matchedData = orders.filter((item) => item.is_matched);

      matchedData.forEach((item) => {
        item.posted = new Date(item.posted).toLocaleString();
      });

      setMatchedOrders(matchedData);
    }
  }, [orders]);

  return (
    <LineChart
      width={500}
      height={300}
      data={matchedOrders}
      margin={{ left: -30 }}
    >
      <CartesianGrid strokeDasharray="3 3" />
      <XAxis
        dataKey="posted"
        tickFormatter={(str) => {
          const date = new Date(str);
          return date.toLocaleDateString();
        }}
      />
      <YAxis />
      <Tooltip />
      <Line
        type="monotone"
        dataKey="price"
        stroke={blue[600]}
        activeDot={{ r: 8 }}
      />
    </LineChart>
  );
};

export default PriceChart;
