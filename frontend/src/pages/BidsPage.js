// BidsPage.js
import React, { useState, useEffect } from 'react';
import { List, ListItem, ListItemText, Card, Typography, Button } from '@mui/material';
import { useHistory } from 'react-router-dom/cjs/react-router-dom.min';
import axios from 'axios'; // Assuming you are using axios for API calls

const BidsPage = () => {
    const [bids, setBids] = useState([]);
    const history = useHistory();

    useEffect(() => {
        const fetchOrders = async () => {
            try {
                const response = await axios.get('/order/list_order'); // Adjust this API endpoint as needed
                let bids = response.data.filter(order => order.side === 'BID');
    
                // Sorting bids by posted date, newest first
                bids.sort((a, b) => new Date(b.posted) - new Date(a.posted));
    
                setBids(bids);
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
                {bids.map(bid => (
                    <ListItem key={bid._id}>
                        <Card variant="outlined" style={{ width: '100%' }}>
                            <ListItemText 
                                primary={`$${bid.price}`}
                                secondary={
                                    <>
                                        <Typography component="span">
                                            {`Posted: ${new Date(bid.posted).toLocaleString()}`}
                                        </Typography>
                                        <Typography component="span" style={{ display: 'block' }}>
                                        {`Matching Status: ${bid.is_matched ? "matched" : "not matched"}`}
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

export default BidsPage;
