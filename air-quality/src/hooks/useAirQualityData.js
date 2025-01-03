import { useState, useEffect } from 'react';
import moment from 'moment';

export const useAirQualityData = () => {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [years, setYears] = useState([]);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const apiUrl = 'http://localhost:5000/';
        const response = await fetch(`${apiUrl}/api/air-quality`);
        if (!response.ok) {
          throw new Error(`Failed to fetch data: ${response.status}`);
        }
        const result = await response.json();
        
        // Process the data once during fetching
        const processedData = result.reduce((acc, item) => {
          const date = moment(item.time);
          const year = date.format('YYYY');
          const formattedDate = date.format('YYYY-MM-DD');
          
          if (!acc.years.includes(year)) {
            acc.years.push(year);
          }
          
          acc.data.push({
            date: formattedDate,
            year,
            city: item.station,
            aqi: item.aqi,
          });
          
          return acc;
        }, { data: [], years: [] });

        setData(processedData.data);
        setYears(processedData.years.sort());
        setError(null);
      } catch (err) {
        console.error('Fetch error:', err);
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  return { data, loading, error, years };
}; 