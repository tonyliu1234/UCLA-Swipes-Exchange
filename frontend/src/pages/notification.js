import React, { useState, useEffect } from "react";
import {
  List,
  ListItem,
  ListItemText,
  Divider,
  Typography,
  ListItemSecondaryAction,
  IconButton,
} from "@mui/material";
import PhoneIcon from "@mui/icons-material/Phone";
import EmailIcon from "@mui/icons-material/Email";
import axios from "axios";
import { useHistory } from "react-router-dom";
import { Button } from "@mui/material";

function NotificationsPage() {
  const [notifications, setNotifications] = useState([]);
  const useMockData = true; // Set to false to fetch data from the API
  const history = useHistory();
  const handleCancelClick = () => {
    history.push("/userProfile");
  };

  useEffect(() => {
    if (useMockData) {
      // Mock data
      const mockNotifications = [
        {
          side: "BUY",
          client: "Alice Johnson",
          client_phone: "123-456-7890",
          client_email: "alice@example.com",
        },
        {
          side: "SELL",
          client: "Bob Smith",
          client_phone: "987-654-3210",
          client_email: "bob@example.com",
        },
        // ... more mock notifications
      ];
      setNotifications(mockNotifications);
    } else {
      // Fetch notifications from the API
      axios
        .get("/user/notifications")
        .then((response) => {
          setNotifications(response.data);
        })
        .catch((error) => {
          console.error("Error fetching notifications:", error);
        });
    }
  }, [useMockData]);

  return (
    <div style={{ margin: "20px" }}>
      <Typography variant="h4" gutterBottom>
        Notifications
      </Typography>
      <Button variant="outlined" color="primary" onClick={handleCancelClick}>
        Back to Profile
      </Button>
      <List>
        {notifications.length === 0 ? (
          <ListItem>
            <ListItemText primary="No new notifications." />
          </ListItem>
        ) : (
          notifications.map((notification, index) => (
            <React.Fragment key={index}>
              <ListItem>
                <ListItemText
                  primary={`${notification.side} - ${notification.client}`}
                  secondary={`Phone: ${notification.client_phone} | Email: ${notification.client_email}`}
                />
                <ListItemSecondaryAction>
                  <IconButton edge="end" aria-label="phone">
                    <PhoneIcon />
                  </IconButton>
                  <IconButton edge="end" aria-label="email">
                    <EmailIcon />
                  </IconButton>
                </ListItemSecondaryAction>
              </ListItem>
              {index < notifications.length - 1 && <Divider />}
            </React.Fragment>
          ))
        )}
      </List>
    </div>
  );
}

export default NotificationsPage;
