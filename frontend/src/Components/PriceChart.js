import { blue } from '@mui/material/colors';
import React from 'react';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
} from 'recharts';

const data = [
  {
    _id: '6567264bd623ad3e4a6a0cfd',
    is_matched: true,
    owner_id: '65671a2fada3e0383290e582',
    posted: 'Wed, 29 Nov 2023 03:53:47 GMT',
    price: 9,
    side: 'BID',
  },
  {
    _id: '65672aa16d0ea2f52bfd7517',
    is_matched: true,
    owner_id: '65671a2fada3e0383290e582',
    posted: 'Wed, 29 Nov 2023 04:12:17 GMT',
    price: 8,
    side: 'BID',
  },
  {
    _id: '65672ac0d11d51e8ec3c7cee',
    is_matched: true,
    owner_id: '65671a2fada3e0383290e582',
    posted: 'Wed, 29 Nov 2023 04:12:48 GMT',
    price: 9,
    side: 'BID',
  },
  {
    _id: '65672ad37be56623d5913458',
    is_matched: true,
    owner_id: '65671a2fada3e0383290e582',
    posted: 'Wed, 29 Nov 2023 04:13:07 GMT',
    price: 10,
    side: 'BID',
  },
  {
    _id: '6567fe3a68e54896946c619b',
    is_matched: true,
    owner_id: '65671a2fada3e0383290e582',
    posted: 'Wed, 29 Nov 2023 19:15:06 GMT',
    price: 8,
    side: 'BID',
  },
  {
    _id: '6567ff3079af9914d23f7e65',
    is_matched: true,
    owner_id: '65671a2fada3e0383290e582',
    posted: 'Wed, 29 Nov 2023 19:19:12 GMT',
    price: 7,
    side: 'BID',
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

// Filtering the data to include only matched entries
const matchedData = data.filter((item) => item.is_matched);

// Parsing the date
matchedData.forEach((item) => {
  item.posted = new Date(item.posted).toLocaleString();
});

const PriceChart = () => (
  <LineChart width={500} height={300} data={matchedData} margin={{ left: -30 }}>
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

export default PriceChart;
