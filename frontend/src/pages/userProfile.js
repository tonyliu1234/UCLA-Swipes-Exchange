import React from "react";
import {
  Box,
  Grid,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  Divider,
  Typography,
  Card,
  CardContent,
  TextField,
  Button,
} from "@mui/material";
import AccountCircleIcon from "@mui/icons-material/AccountCircle";
import ShoppingCartIcon from "@mui/icons-material/ShoppingCart";
import SellIcon from "@mui/icons-material/Sell";
import ExitToAppIcon from "@mui/icons-material/ExitToApp";
import EditIcon from "@mui/icons-material/Edit"; // import Edit icon
import { useHistory } from "react-router-dom";

export default function UserProfile() {
  let history = useHistory();

  const handleEditProfileClick = () => {
    // Use the correct path to your "changeUserProfile" page
    history.push("./changeUserProfile");
  };
  return (
    <Box sx={{ display: "flex", p: 2 }}>
      <Grid container spacing={2} sx={{ height: "100vh" }}>
        {/* Left part */}
        <Grid
          item
          xs={12}
          sm={3}
          sx={{
            bgcolor: "grey.200",
            display: "flex",
            flexDirection: "column",
            // justifyContent: "center",
          }}
        >
          <Typography variant="h3" component="div" sx={{ pt: 4, pb: 4, pl: 2 }}>
            User Profile
          </Typography>
          <Divider />
          <List>
            <ListItem button>
              <ListItemIcon>
                <AccountCircleIcon />
              </ListItemIcon>
              <ListItemText primary="Profile" />
            </ListItem>
            <ListItem button>
              <ListItemIcon>
                <ShoppingCartIcon />
              </ListItemIcon>
              <ListItemText
                primary="Buying"
                secondary="Active Bids, In-Progress, Completed Orders"
              />
            </ListItem>
            <ListItem button>
              <ListItemIcon>
                <SellIcon />
              </ListItemIcon>
              <ListItemText
                primary="Selling"
                secondary="Active Asks, In-Progress, Completed Sales"
              />
            </ListItem>
            {/* Add an edit profile button */}
            <ListItem button onClick={handleEditProfileClick}>
              <ListItemIcon>
                <EditIcon />
              </ListItemIcon>
              <ListItemText
                primary="Edit Profile"
                secondary="Change Profile Details"
              />
            </ListItem>
            <ListItem button>
              <ListItemIcon>
                <ExitToAppIcon />
              </ListItemIcon>
              <ListItemText primary="Logout" />
            </ListItem>
          </List>
        </Grid>

        {/* Right part */}
        <Grid item xs={12} sm={9}>
          <Card
            variant="outlined"
            sx={{ minWidth: 275, boxShadow: "none", border: "none", ml: 8 }}
          >
            <CardContent>
              <Typography
                variant="h6"
                component="div"
                gutterBottom
                sx={{ mt: 12, mb: 4 }}
              >
                <strong>Profile Details</strong>
              </Typography>
              <Grid container spacing={6}>
                <Grid item xs={6}>
                  <Typography variant="body1">
                    <strong>Name</strong>
                  </Typography>
                  <Typography variant="body2">Jeffrey Yu</Typography>
                </Grid>
                <Grid item xs={6}>
                  <Typography variant="body1">
                    <strong>UCLA ID</strong>
                  </Typography>
                  <Typography variant="body2">000000000</Typography>
                </Grid>
                <Grid item xs={6}>
                  <Typography variant="body1">
                    <strong>Username</strong>
                  </Typography>
                  <Typography variant="body2">sneakerhead6321!</Typography>
                </Grid>
                <Grid item xs={6}>
                  <Typography variant="body1">
                    <strong>Phone Number</strong>
                  </Typography>
                  <Typography variant="body2">(213) 468-2703</Typography>
                </Grid>
                <Grid item xs={12}>
                  <Typography variant="body1">
                    <strong>Email Address</strong>
                  </Typography>
                  <Typography variant="body2">y239781702@gmail.com</Typography>
                </Grid>
              </Grid>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Box>
  );
}
