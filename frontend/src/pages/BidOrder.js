import React, { useState } from 'react';
import { makeStyles, withStyles } from '@material-ui/styles';
import { Button, Box, MenuItem, FormControl, Select, InputLabel, TextField, Typography, ToggleButtonGroup, ToggleButton } from '@material-ui/core';
const useStyles = makeStyles((theme) => ({
  root: {
    display: 'flex',
    justifyContent: 'center',
    alignItems: 'center',
    height: '100vh', // Full height of the viewport
    width: '100vw', // Full width of the viewport
    backgroundImage: `url(https://source.unsplash.com/random?wallpapers)`,
    backgroundSize: 'cover', // Cover the entire viewport
    backgroundPosition: 'center', // Center the background image
  },
  container: {
    width: '50%', // Half the width of the screen
    maxWidth: '600px', // Optional: if you want to limit how wide it can get
    margin: '0', // No margin for centering purposes
    padding: '16px',
    boxShadow: '0px 3px 6px #00000029',
    borderRadius: '4px',
    backgroundColor: 'rgba(255, 255, 255, 0.5)', // Adjust transparency here
    backdropFilter: 'blur(8px)', // Apply a blur effect to the background content
  },
  toggleContainer: {
    display: 'flex',
    justifyContent: 'center', // This will center the toggle buttons wrapper div
    alignItems: 'center',
    margin: '0 auto', // Centers the container itself if needed
    width: '100%', // Ensures the container takes the full width
    marginBottom: '2Rem',
    marginTop: '1.2Rem',
  },
}));

const StyledToggleButton = withStyles({
  root: {
    border: '1px solid #c4c4c4',
    '&:not(:first-child)': {
      borderLeft: '1px solid #c4c4c4', // Reinforce the left border for all but the first button
    },
    '&.Mui-selected': {
      backgroundColor: '#000', // Black background for selected state
      color: 'white', // White text for selected state
    },
    margin: '5px',
    textAlign: 'center',
    lineHeight: '40px', // Adjust the line height to match your button's height
  },
})(ToggleButton);

const BidOrder = () => {
  const classes = useStyles();
  const [selectedPrice, setSelectedPrice] = useState(null); // Add state for selected price

  // Handle the selection of a price
  const handlePriceSelection = (event, newPrice) => {
    setSelectedPrice(newPrice);
  };

  return (
    <Box className={classes.root}>
      <Box className={classes.container} p={2}  m={2} style={{ width: '34rem' }}>
        <Typography variant="subtitle1" gutterBottom>
          High Demand - 83 people are interested in this product
        </Typography>
        <Typography variant="h6">Size: US XL</Typography>
        {/* Pricing Options */}
        <div className={classes.toggleContainer}>
        <ToggleButtonGroup
          value={selectedPrice}
          exclusive
          onChange={handlePriceSelection}
          aria-label="price selection"
          alignItems='center'
        >
          <StyledToggleButton value={51} style={{marginRight: '4.3Rem', border: '1px solid #c4c4c4'}} aria-label="good bid">
            $51 Good Bid
          </StyledToggleButton>
          <StyledToggleButton value={56} style={{marginRight: '4.3Rem', border: '1px solid #c4c4c4'}} aria-label="better bid">
            $56 Better Bid
          </StyledToggleButton>
          <StyledToggleButton value={70} style={{border: '1px solid #c4c4c4',}} aria-label="buy now">
            $70 Buy Now
          </StyledToggleButton>
        </ToggleButtonGroup>
        </div>
        {/* Name Your Price */}
        <TextField label="Or Name Your Price" style={{ marginBottom: '2rem' }} defaultValue="56" fullWidth margin="normal" />
        <FormControl fullWidth>
        <InputLabel>Bid Expiration</InputLabel>
        <Select defaultValue={30}>
          <MenuItem value={30}>30 Days</MenuItem>
          <MenuItem value={60}>60 Days</MenuItem>
          <MenuItem value={90}>90 Days</MenuItem>
        </Select>
      </FormControl>
      <Box display="flex" justifyContent="space-between" my={2}>
        <Button variant="text" style={{color: 'black'}}>Cancel</Button>
        <Button variant="contained" color="grey">
          Place Bid
        </Button>
      </Box>
      </Box>
    </Box>
  );
};

export default BidOrder;
