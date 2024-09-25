import React, { useEffect, useState } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { Card, CardContent, Typography, Grid, MenuItem, Select, FormControl, InputLabel } from '@mui/material';
import moment from 'moment';

const AirQualityChart = () => {
  const [data, setData] = useState([]);
  const [selectedYear, setSelectedYear] = useState('2020'); // Default year
  const [years, setYears] = useState([]);  // List of available years

  // Fetch data from API
  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch('http://192.168.1.12:5000/api/air-quality');
        const result = await response.json();
        const formattedData = formatData(result);
        setData(formattedData);
        setYears(getUniqueYears(formattedData));  // Get the list of unique years
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    };

    fetchData();
  }, []);

  // Helper function to format the API data
  const formatData = (data) => {
    return data.map(item => ({
      date: moment(item.time).format('YYYY-MM-DD'),  // Convert timestamp to date
      year: moment(item.time).format('YYYY'),  // Extract the year
      city: item.station,
      aqi: item.aqi,
    }));
  };

  // Get unique years from the data
  const getUniqueYears = (data) => {
    const allYears = data.map(item => item.year);
    return [...new Set(allYears)]; // Return unique years
  };

  // Organize data by city and filter by year
  const organizeByCityAndYear = (data, year) => {
    const filteredData = data.filter(item => item.year === year);
    const cities = {};
    filteredData.forEach(item => {
      const { date, city, aqi } = item;
      if (!cities[city]) {
        cities[city] = [];
      }
      cities[city].push({ date, aqi });
    });
    return cities;
  };

  // Handle year selection change
  const handleYearChange = (event) => {
    setSelectedYear(event.target.value);
  };

  const cityData = organizeByCityAndYear(data, selectedYear);

  const cityColors = {
    Auckland: '#8884d8',
    Christchurch: '#82ca9d',
    Dunedin: '#ff7300',
    Wellington: '#ffc658',
    Hamilton: '#d0ed57',
  };

  return (
    <Grid container spacing={2} justifyContent="center">
      <Grid item xs={12}>
        <Card>
          <CardContent>
            <Typography variant="h5" component="div" gutterBottom>
              Air Quality Over Time
            </Typography>

            {/* Dropdown for selecting year */}
            <FormControl fullWidth>
              <InputLabel id="year-select-label">Year</InputLabel>
              <Select
                labelId="year-select-label"
                id="year-select"
                value={selectedYear}
                label="Year"
                onChange={handleYearChange}
              >
                {years.map((year) => (
                  <MenuItem key={year} value={year}>
                    {year}
                  </MenuItem>
                ))}
              </Select>
            </FormControl>

            <ResponsiveContainer width="100%" height={400}>
              <LineChart>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="date" allowDuplicatedCategory={false}/>
                <YAxis domain={[0, 50]}/>
                <Tooltip />
                <Legend />
                {Object.keys(cityData).map(city => (
                  <Line
                    key={city}
                    type="monotone"
                    dataKey="aqi"
                    data={cityData[city]}
                    name={city}
                    stroke={cityColors[city]}
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
