import React from 'react';
import { Toolbar, Typography, CssBaseline, Container, Box} from '@mui/material';
import AirQualityChart from './components/aqchart.js';
import Header from './components/Header.js';
import NavBar from './components/NavBar.js';

function App() {
  return (
    <Box sx={{ display: 'flex' }}>
      <CssBaseline />

      <Header />

      <NavBar />

      {/* Main Content */}
      <Box
        component="main"
        sx={{ flexGrow: 1, bgcolor: 'background.default', p: 3 }}
      >
        <Toolbar />
        <Container>
          <Typography variant="h4" gutterBottom>
            Welcome to the Air Quality Dashboard
          </Typography>
              <div className="App">
                <AirQualityChart />
              </div>
        </Container>
      </Box>
    </Box>
  );
}

export default App;
