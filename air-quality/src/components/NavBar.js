import React from 'react';
import { Toolbar, Drawer, List, ListItem, ListItemText, Box } from '@mui/material';

const NavBar = () => (
    <Drawer
    variant="permanent"
    sx={{
      width: 240,
      flexShrink: 0,
      [`& .MuiDrawer-paper`]: { width: 240, boxSizing: 'border-box' },
    }}>
    <Toolbar />
    <Box sx={{ overflow: 'auto' }}>
      <List>
        <ListItem button>
          <ListItemText primary="Dashboard" />
        </ListItem>
      </List>
    </Box>
  </Drawer>
);

export default NavBar;