import React, { useState } from 'react';
import { Typography, Box, MenuItem, FormControl, Select, InputLabel, Input, ToggleButtonGroup, ToggleButton, Button } from '@material-ui/core';
import { makeStyles, withStyles } from '@material-ui/styles';

const useStyles = makeStyles({
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
  // Add this inside your useStyles
  toggleContainer: {
    display: 'flex',
    justifyContent: 'center', // This will center the toggle buttons wrapper div
    alignItems: 'center',
    margin: '0 auto', // Centers the container itself if needed
    width: '100%', // Ensures the container takes the full width
    marginBottom: '2Rem',
    marginTop: '1.2Rem',
  },

  input: {
    flex: 1,
    margin: '8px',
  },
});

const StyledToggleButtonGroup = withStyles({
  grouped: {
    margin: '8px',
    border: 'none',
    '&:not(:first-child)': {
      borderRadius: '20px',
    },
    '&:first-child': {
      borderRadius: '20px',
    },
    // Flexbox properties to center the buttons
    display: 'flex', 
    justifyContent: 'center', // This centers the buttons horizontally in the container
    height: '2.4Rem',
    width: '18Rem'
  },
})(ToggleButtonGroup);

const StyledToggleButton = withStyles({
  root: {
    border: '1px solid #c4c4c4',
    '&.Mui-selected': {
      backgroundColor: '#000',
      color: '#fff',
      '&:hover': {
        backgroundColor: '#000',
      },
    },
    // Text alignment properties to center text inside the button
    textAlign: 'center', 
    lineHeight: '40px', // Adjust the line height to match your button's height
  },
})(ToggleButton);


const AskOrder = () => {
  const [alignment, setAlignment] = useState('left');
  const classes = useStyles();

  const handleAlignment = (event, newAlignment) => {
    setAlignment(newAlignment);
  };

  return (
    <Box className={classes.root}>
    <Box className={classes.container}>
      <Typography variant="subtitle1" gutterBottom>
        Inventory is High, Act Fast - There are 16 asks on this item.
      </Typography>
      <Typography variant="h6">Size: US XL</Typography>
      <div className={classes.toggleContainer}> {/* Wrap your StyledToggleButtonGroup with a div */}
      <StyledToggleButtonGroup
        size="large"
        value={alignment}
        exclusive
        onChange={handleAlignment}
        aria-label="text alignment"
      >
        <StyledToggleButton value="left" aria-label="left aligned">
          Place Ask
        </StyledToggleButton>
        <StyledToggleButton value="right" aria-label="right aligned">
          Sell Now
        </StyledToggleButton>
      </StyledToggleButtonGroup>
    </div>
      <FormControl fullWidth className={classes.input}>
        <InputLabel htmlFor="price">Price</InputLabel>
        <Input id="price" style={{marginBottom: '2Rem'}} startAdornment={<Typography variant="h6">$</Typography>} />
      </FormControl>
      <FormControl fullWidth className={classes.input}>
        <InputLabel id="ask-expiration-label">Ask Expiration</InputLabel>
        <Select
          labelId="ask-expiration-label"
          defaultValue={30}
        >
          <MenuItem value={30}>30 Days</MenuItem>
          <MenuItem value={60}>60 Days</MenuItem>
          <MenuItem value={90}>90 Days</MenuItem>
        </Select>
      </FormControl>
      <Box display="flex" justifyContent="space-between" my={2}>
        <Button variant="text" style={{color: 'black'}}>Cancel</Button>
        <Button variant="contained" color="grey">
          Submit
        </Button>
      </Box>
    </Box>
    </Box>
  );
};

export default AskOrder;
