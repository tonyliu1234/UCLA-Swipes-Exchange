// changeUserProfile.js
import React from "react";
import {
  Box,
  Container,
  TextField,
  Button,
  Typography,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
} from "@mui/material";
import { useHistory } from "react-router-dom";

const ChangeUserProfile = () => {
  // You would also include state management and event handlers here
  // For example, using useState for form fields and a submit handler
  console.log("ChangeUserProfile is rendered");
  let history = useHistory();

  const handleCancelClick = () => {
    history.push("./userProfile");
  };

  return (
    <Container component="main" maxWidth="sm">
      <Box
        sx={{
          marginTop: 8,
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
        }}
      >
        <Typography component="h1" variant="h5">
          Profile
        </Typography>
        <Typography variant="subtitle1" sx={{ mt: 2 }}>
          Change your profile settings
        </Typography>
        <Box component="form" noValidate sx={{ mt: 1 }}>
          <TextField
            margin="normal"
            required
            fullWidth
            id="firstName"
            label="First Name"
            name="firstName"
            autoComplete="given-name"
            autoFocus
          />
          <TextField
            margin="normal"
            required
            fullWidth
            id="lastName"
            label="Last Name"
            name="lastName"
            autoComplete="family-name"
          />
          <TextField
            margin="normal"
            required
            fullWidth
            id="username"
            label="Username"
            name="username"
          />
          <TextField
            margin="normal"
            required
            fullWidth
            id="phone"
            label="Phone Number"
            name="phone"
            type="tel"
          />
          <TextField
            margin="normal"
            required
            fullWidth
            id="uid"
            label="UCLA ID"
            name="uid"
            type="uid"
          />
          <TextField
            margin="normal"
            required
            fullWidth
            id="email"
            label="Email Address"
            name="email"
            type="enauk"
          />

          <Box
            sx={{
              display: "flex",
              justifyContent: "space-between",
              mt: 3,
              mb: 2,
            }}
          >
            <Button
              type="button"
              variant="outlined"
              sx={{ mt: 3, mb: 2 }}
              // Here you would handle the cancel action
              onClick={handleCancelClick}
            >
              Cancel
            </Button>
            <Button
              type="submit"
              variant="contained"
              sx={{ mt: 3, mb: 2 }}
              // Here you would handle the submit action
            >
              Submit
            </Button>
          </Box>
        </Box>
      </Box>
    </Container>
  );
};

export default ChangeUserProfile;
