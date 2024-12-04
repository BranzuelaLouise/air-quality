import React, { useState, useMemo } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { 
  Card, 
  CardContent, 
  Typography, 
  Grid, 
  MenuItem, 
  Select, 
  FormControl, 
  InputLabel, 
  CircularProgress, 
  Alert,
  ToggleButton,
  ToggleButtonGroup
} from '@mui/material';
import { useAirQualityData } from '../hooks/useAirQualityData';

const cityColors = {
  Auckland: '#8884d8',
  Christchurch: '#82ca9d',
  Dunedin: '#ff7300',
  Wellington: '#ffc658',
  Hamilton: '#d0ed57',
};

const CustomTooltip = ({ active, payload, label }) => {
  if (active && payload && payload.length) {
    return (
      <div style={{ backgroundColor: 'white', padding: '10px', border: '1px solid #ccc' }}>
        <p>{`Date: ${label}`}</p>
        {payload.map((entry) => (
          <p key={entry.name} style={{ color: entry.color }}>
            {`${entry.name}: ${entry.value.toFixed(1)}`}
          </p>
        ))}
      </div>
    );
  }
  return null;
};

const AirQualityChart = () => {
  const { data, loading, error, years } = useAirQualityData();
  const [selectedYear, setSelectedYear] = useState(() => {
    const currentYear = new Date().getFullYear().toString();
    return years.includes(currentYear) ? currentYear : '2020';
  });

  const [visibleCities, setVisibleCities] = useState(Object.keys(cityColors));

  const handleCityToggle = (event, newVisibleCities) => {
    if (newVisibleCities.length) {
      setVisibleCities(newVisibleCities);
    }
  };

  const chartData = useMemo(() => {
    if (!data.length) return [];
    
    const dateMap = new Map();
    
    data.filter(item => item.year === selectedYear)
        .forEach(item => {
          if (!dateMap.has(item.date)) {
            dateMap.set(item.date, { date: item.date });
          }
          dateMap.get(item.date)[item.city] = item.aqi;
        });
    
    return Array.from(dateMap.values())
                .sort((a, b) => a.date.localeCompare(b.date));
  }, [data, selectedYear]);

  if (loading) {
    return (
      <Grid container justifyContent="center" alignItems="center" style={{ minHeight: '400px' }}>
        <CircularProgress />
      </Grid>
    );
  }

  if (error) {
    return (
      <Alert severity="error">
        Error loading air quality data: {error}
      </Alert>
    );
  }

  return (
    <Grid container spacing={2} justifyContent="center">
      <Grid item xs={12}>
        <Card>
          <CardContent>
            <Typography variant="h5" component="div" gutterBottom>
              Air Quality Over Time
            </Typography>

            <Grid container spacing={2} sx={{ mb: 3 }}>
              <Grid item xs={12} md={6}>
                <FormControl fullWidth>
                  <InputLabel id="year-select-label">Year</InputLabel>
                  <Select
                    labelId="year-select-label"
                    id="year-select"
                    value={selectedYear}
                    label="Year"
                    onChange={(e) => setSelectedYear(e.target.value)}
                  >
                    {years.map((year) => (
                      <MenuItem key={year} value={year}>
                        {year}
                      </MenuItem>
                    ))}
                  </Select>
                </FormControl>
              </Grid>
              <Grid item xs={12} md={6}>
                <Typography variant="subtitle2" gutterBottom>
                  Toggle Cities:
                </Typography>
                <ToggleButtonGroup
                  value={visibleCities}
                  onChange={handleCityToggle}
                  aria-label="city visibility"
                  size="small"
                  sx={{ 
                    flexWrap: 'wrap',
                    '& .MuiToggleButton-root': {
                      margin: '2px',
                      border: '1px solid rgba(0, 0, 0, 0.12)'
                    }
                  }}
                >
                  {Object.entries(cityColors).map(([city, color]) => (
                    <ToggleButton 
                      key={city} 
                      value={city}
                      sx={{
                        '&.Mui-selected': {
                          backgroundColor: `${color}40`,
                          '&:hover': {
                            backgroundColor: `${color}60`,
                          }
                        },
                        '&:hover': {
                          backgroundColor: `${color}20`,
                        }
                      }}
                    >
                      {city}
                    </ToggleButton>
                  ))}
                </ToggleButtonGroup>
              </Grid>
            </Grid>

            <ResponsiveContainer width="100%" height={400}>
              <LineChart
                data={chartData}
                margin={{ top: 5, right: 30, left: 20, bottom: 5 }}
              >
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis 
                  dataKey="date" 
                  tick={{ fontSize: 12 }}
                  interval="preserveStartEnd"
                />
                <YAxis 
                  domain={[0, 50]}
                  tick={{ fontSize: 12 }}
                  label={{ value: 'Air Quality Index', angle: -90, position: 'insideLeft' }}
                />
                <Tooltip content={<CustomTooltip />} />
                <Legend />
                {Object.keys(cityColors)
                  .filter(city => visibleCities.includes(city))
                  .map(city => (
                    <Line
                      key={city}
                      type="monotone"
                      dataKey={city}
                      name={city}
                      stroke={cityColors[city]}
                      dot={false}
                      strokeWidth={2}
                      connectNulls
                    />
                  ))}
              </LineChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>
      </Grid>
    </Grid>
  );
};

export default AirQualityChart;
