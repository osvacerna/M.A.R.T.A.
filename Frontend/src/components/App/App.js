import React, { useState} from 'react';
import './App.css';
import AgeSliderComponent from '../AgeSliderComponent/AgeSliderComponent.js';
import Footer from '../BarsComponent/Footer.js';
import ImageComponent from '../ImageComponent/ImageComponent.js';
import InfoComponent from '../InfoComponent/InfoComponent.js';
import MapComponent from '../MapComponent/MapComponent.js';
import MapasInterComponent from '../MapasInterComponent/MapasInterComponent.js';
import NavBar from '../BarsComponent/NavBar.js';

function App() {
  const [age, setAge] = useState(null);
  const [coords, setCoords] = useState(null);
  const [responseMessage, setResponseMessage] = useState('');

  const handleAgeConfirm = (userAge) => {
    setAge(userAge);
  };

  const handleMapClick = async (coords) => {
    setCoords(coords);
    try {
      const response = await fetch('http://localhost:5000/process_coordinates', {
          method: 'POST',
          headers: {
          'Content-Type': 'application/json',
          },
          body: JSON.stringify(coords),
      });

      const data = await response.json();
      setResponseMessage(data);   
    } catch (error) {
        console.error('Error al enviar coordenadas:', error);
        setResponseMessage('Error al enviar coordenadas.');
    }
  };

  // Función para regresar a la pantalla de selección de edad
  const goToAgeSlider = () => {
    setAge(null);
    setCoords(null);
  };

  return (
    <>
    <main class>
    <div className="main-background full-height p-0">
      <NavBar goToAgeSlider={goToAgeSlider} />
      
      {age === null ? (
        <>
        <AgeSliderComponent onConfirm={handleAgeConfirm} />
        </>
      ) : (
        <div className="row full-height justify-content-center">
          {coords === null ? (
            <>
            <div className="col-md-6 d-flex full-height">
              <MapComponent onMapClick={handleMapClick}/>
            </div>
            <div className="col-md-6 d-flex align-items-center justify-content-center full-height">
              <InfoComponent data={responseMessage} age={age}/>
            </div>
            </>
          ) : (
            <>
            <div className="col-md-6 d-flex full-height">
              <MapasInterComponent age={age} />
            </div>
            <div className="col-md-6 d-flex align-items-center justify-content-center full-height">
              <ImageComponent/>
            </div>
            </>
          )}
        </div>
      
      )}
    </div>
    </main>
    <Footer />
    </>
  );
}

export default App;