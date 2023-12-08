// BidsPage.js
import React, { useState, useEffect } from 'react';
import { List, ListItem, ListItemText, Card, Typography, Button } from '@mui/material';
import { useHistory } from 'react-router-dom/cjs/react-router-dom.min';
import axios from 'axios'; // Assuming you are using axios for API calls


const apiUrl = process.env.REACT_APP_API_URL === undefined ? "" : process.env.REACT_APP_API_URL

const AsksPage = () => {
    const [asks, setAsks] = useState([]);
    const history = useHistory();
    useEffect(() => {
        const fetchOrders = async () => {
            try {
                const response = await axios.get(`${apiUrl}/order/list_order`); // Adjust this API endpoint as needed
                const asks = response.data.filter(order => order.side === 'ASK');
                asks.sort((a, b) => new Date(b.posted) - new Date(a.posted));
                setAsks(asks);
            } catch (error) {
                console.error('Error fetching orders:', error);
            }
        };

        fetchOrders();
    }, []);
    const goBack = () => {
        history.push('userProfile');
    };
    return (
        <>
            <Button onClick={goBack} style={{ margin: '20px' }}>Back to Profile</Button>
        <List>
            {asks.map(ask => (
                <ListItem key={ask._id}>
                    <Card variant="outlined" style={{ width: '100%' }}>
                        <ListItemText 
                            primary={`$${ask.price}`}
                            secondary={
                                <>
                                  <Typography component="span">
                                    {`Posted: ${new Date(ask.posted).toLocaleString()}`}
                                  </Typography>
                                  <Typography component="span" style={{ display: 'block' }}>
                                  {`Matching Status: ${ask.is_matched ? "matched" : "not matched"}`}
                                  </Typography>
                                </>
                              }
                        />
                    </Card>
                </ListItem>
            ))}
        </List>
        </>
        
    );
};

export default AsksPage;
