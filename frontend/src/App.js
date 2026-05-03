import React, { useState } from 'react';
import axios from 'axios';
import { Line } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
);

function App() {
  const [ticker, setTicker] = useState('AAPL');
  const [data, setData] = useState([]);
  const [predictions, setPredictions] = useState([]);
  const [loading, setLoading] = useState(false);

  const fetchData = async () => {
    setLoading(true);
    try {
      const { data: historical } = await axios.get(`http://localhost:8000/data/${ticker}`);
      const { data: predData } = await axios.post('http://localhost:8000/predict/', { ticker, days: 30 });
      
      setData(historical);
      setPredictions(predData.predictions);
    } catch (error) {
      alert('Error fetching data. Run backend first!');
    }
    setLoading(false);
  };

  const chartData = {
    labels: data.slice(-30).map(d => new Date(d.date).toLocaleDateString()).concat(
      Array.from({length: predictions.length}, (_, i) => `+Day ${i+1}`)
    ),
    datasets: [
      {
        label: 'Historical Close',
        data: data.slice(-30).map(d => d.close),
        borderColor: 'rgb(75, 192, 192)',
        backgroundColor: 'rgba(75, 192, 192, 0.2)',
        tension: 0.1
      },
      {
        label: 'AI Prediction (30 days)',
        data: [null, null, null, null, null, null, null, null, null, null, predictions],  // Pad to align
        borderColor: 'rgb(255, 99, 132)',
        backgroundColor: 'rgba(255, 99, 132, 0.2)',
        borderDash: [5, 5],
        tension: 0.1,
        fill: false
      }
    ]
  };

  return (
    <div style={{ padding: '20px', maxWidth: '1200px', margin: '0 auto' }}>
      <h1>AI Stock Market Prediction</h1>
      <div style={{ marginBottom: '20px' }}>
        <input 
          value={ticker} 
          onChange={(e) => setTicker(e.target.value.toUpperCase())} 
          placeholder="Enter ticker (AAPL, TSLA)"
          style={{ padding: '10px', marginRight: '10px', width: '200px' }}
        />
        <button onClick={fetchData} disabled={loading}>
          {loading ? 'Loading...' : 'Analyze Stock'}
        </button>
      </div>
      {data.length > 0 && (
        <div>
          <h3>{ticker} - Historical & Predicted Prices</h3>
          <Line data={chartData} />
          <p><strong>AI Suggestion:</strong> {predictions[predictions.length-1] > data[data.length-1].Close ? 'BUY' : 'SELL'}</p>
        </div>
      )}
    </div>
  );
}

export default App;
