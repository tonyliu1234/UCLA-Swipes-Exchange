import React, { useState, useEffect } from "react";
import {
  List,
  ListItem,
  ListItemText,
  Divider,
  Typography,
} from "@mui/material";
import axios from "axios";

function NotificationsPage() {
  const [notifications, setNotifications] = useState([]);

  useEffect(() => {
    // Fetch notifications
    axios
      .get("/notifications")
      .then((response) => {
        setNotifications(response.data);
      })
      .catch((error) => {
        console.error("Error fetching notifications:", error);
      });
  }, []);

  return (
    <div style={{ margin: "20px" }}>
      <Typography variant="h4" gutterBottom>
        Notifications
      </Typography>
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
                  primary={notification.title}
                  secondary={notification.message}
                />
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
