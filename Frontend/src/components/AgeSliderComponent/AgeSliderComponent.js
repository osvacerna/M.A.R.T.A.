import React, { useState } from 'react';
import './AgeSliderComponent.css';

function AgeSliderComponent({ onConfirm }) {
  const [age, setAge] = useState(50);

  const handleAgeChange = (event) => {
    setAge(event.target.value);
  };

  const confirmAge = () => {
    onConfirm(age);
  };

  return (
    <div className="ageslider-background d-flex justify-content-center align-items-center min-vh-100">
      <div className="card text-center shadow-lg" style={{ width: '18rem' }}>
        <div className="card-body">
          <h5 className="card-title">¿Cuál es tu edad?</h5>
          <input
            type="range"
            min="1"
            max="100"
            value={age}
            className="form-range mt-4 dot-color" 
            onChange={handleAgeChange}
          />
          <p className="mt-3">{age} años</p>
          <button className="btn btn-primary btn-color" onClick={confirmAge}>Confirmar</button>
        </div>
      </div>
    </div>
  );
}

export default AgeSliderComponent;