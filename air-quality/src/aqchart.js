import React from 'react';
import {
  LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer,
} from 'recharts';
import { Card, CardContent, Typography, Grid } from '@mui/material';
import moment from 'moment';

const data = [
  [1546214400000, "Auckland", 9], [1546214400000, "Christchurch", 19], [1546214400000, "Wellington", 10],
  [1546300800000, "Auckland", 12], [1546300800000, "Christchurch", 8], [1546300800000, "Wellington", 9],
  [1546387200000, "Auckland", 8], [1546387200000, "Christchurch", 11], [1546387200000, "Wellington", 12],
  [1546473600000, "Auckland", 10], [1546473600000, "Christchurch", 17], [1546473600000, "Wellington", 18],
  [1546560000000, "Auckland", 13], [1546560000000, "Christchurch", 19], [1546560000000, "Wellington", 12],
  [1546646400000, "Auckland", 21], [1546646400000, "Christchurch", 15], [1546646400000, "Wellington", 14],
];

// Helper function to format data
const formatData = (data) => {
  return data.map(item => ({
    date: moment(item[0]).format('YYYY-MM-DD'), // Convert timestamp to date
    city: item[1],
    aqi: item[2]
  }));
};

// Organize data by city
const organizeByCity = (data) => {
  const cities = {};
  data.forEach(item => {
    const { date, city, aqi } = item;
    if (!cities[city]) {
      cities[city] = [];
    }
    cities[city].push({ date, aqi });
  });
  return cities;
};

const AirQualityChart = () => {
  const formattedData = formatData(data);
  const cityData = organizeByCity(formattedData);

  return (
    <Grid container spacing={2} justifyContent="center">
      <Grid item xs={12} md={8}>
        <Card>
          <CardContent>
            <Typography variant="h5" component="div" gutterBottom>
              Air Quality Over Time
            </Typography>
            <ResponsiveContainer width="100%" height={400}>
              <LineChart>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="date" />
                <YAxis />
                <Tooltip />
                <Legend />
                {Object.keys(cityData).map(city => (
                  <Line
                    key={city}
                    type="monotone"
                    dataKey="aqi"
                    data={cityData[city]}
                    name={city}
                    stroke={city === 'Auckland' ? '#8884d8' : city === 'Christchurch' ? '#82ca9d' : '#ff7300'}
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
