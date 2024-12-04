import React from 'react';
import { AppBar, Toolbar, Typography } from '@mui/material';

const Header = () => (
    <AppBar position="fixed" sx={{ zIndex: (theme) => theme.zIndex.drawer + 1 }}>
        <Toolbar>
            <Typography variant="h6" noWrap component="div">
                Air Quality Dashboard
            </Typography>
        </Toolbar>
    </AppBar>
);

export default Header;