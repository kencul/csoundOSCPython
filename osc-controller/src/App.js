import React, { useState } from 'react';
import axios from 'axios';

function App() {
  const [ip, setIp] = useState("127.0.0.1");
  const [port, setPort] = useState(9000);
  const [status, setStatus] = useState("stopped");

  const startOsc = async () => {
    try {
      await axios.post('http://localhost:8000/start-osc', { ip, port });
      setStatus("running");
    } catch (error) {
      console.error("Error starting OSC:", error);
    }
  };

  const stopOsc = async () => {
    try {
      await axios.post('http://localhost:8000/stop-osc');
      setStatus("stopped");
    } catch (error) {
      console.error("Error stopping OSC:", error);
    }
  };

  return (
    <div style={{ padding: '20px', maxWidth: '500px' }}>
      <h1>OSC Script Controller</h1>
      
      <div style={{ marginBottom: '15px' }}>
        <label>IP: </label>
        <input 
          type="text" 
          value={ip} 
          onChange={(e) => setIp(e.target.value)} 
        />
      </div>
      
      <div style={{ marginBottom: '15px' }}>
        <label>Port: </label>
        <input 
          type="number" 
          value={port} 
          onChange={(e) => setPort(parseInt(e.target.value))} 
        />
      </div>
      
      <button onClick={startOsc} disabled={status === "running"}>
        Start OSC
      </button>
      <button onClick={stopOsc} disabled={status === "stopped"}>
        Stop OSC
      </button>
      
      <p>Status: <strong>{status}</strong></p>
    </div>
  );
}

export default App;