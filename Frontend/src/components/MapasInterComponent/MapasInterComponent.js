import React, { useState, useEffect } from 'react';
import axios from 'axios';

const MapasInterComponent = ({age}) => {
  const [apiParquesResponse, setApiParquesResponse] = useState('');
  const [apiIndustriaResponse, setApiIndustriaResponse] = useState('');
  const [apiHospitalesResponse, setApiHospitalesResponse] = useState('');

  const handleButtonClick = async (url) => {
    try {
      const response = await axios.get(url);
      const { url: redirectUrl } = response.data;
      window.open(redirectUrl, '_blank');
    } catch (error) {
      console.error('Error fetching data:', error);
      alert('Hubo un error al obtener la URL');
    }
  };

  const fetchData = async () => {
    const fetchResponses = async (value) => {
      try {
        const response = await axios.post('http://127.0.0.1:5000/postGeminiPrompt', {
          prompt: value,
          max_tokens: 150,
        }, {
          headers: {
            'Content-Type': 'application/json',
          },
        });
        return response.data; // Asumiendo que la respuesta es directamente lo que necesitas
      } catch (error) {
        console.error('Error al hacer la solicitud POST:', error);
        return 'Hubo un error al obtener la respuesta.';
      }
    };

    const parqueResponse = await fetchResponses(`Explica en dos oraciones la importancia de tener parques y areas verdes cerca del hogar a una persona de edad ${age}`);
    setApiParquesResponse(parqueResponse.message || parqueResponse);

    const industriaResponse = await fetchResponses(`Explica en dos oraciones como puede afectar vivir cerca de industrias a una persona de edad ${age}`);
    setApiIndustriaResponse(industriaResponse.message || industriaResponse);

    const hospitalResponse = await fetchResponses(`Explica en dos oraciones porque es importante tener servicios de salud disponibles a una persona de edad ${age}`);
    setApiHospitalesResponse(hospitalResponse.message || hospitalResponse);
  };

  useEffect(() => {
    fetchData();
  }, [age]);

  return (
    <>
      <div className="d-flex flex-column align-items-center fixed-center w-100 mt-5">
        <div className="card text-center shadow-lg p-3 mb-3 w-100 mt-4">
          <h2 className="card-title">Mapas Informativos</h2>
        </div>
        <div className="card text-center shadow-lg p-3 mb-3 w-100">
          <div className="card-body">
            <div className="card-text">
              <h5>Parques</h5>
              { apiParquesResponse === 'Hubo un error al obtener la respuesta.' ? (
                <p></p>
              ) : (
                <p>{apiParquesResponse}</p>
              )}
              <button
                className="btn btn-primary"
                onClick={() => handleButtonClick('http://127.0.0.1:5000/getParques')}
              >
                Ver mapa interactivo
              </button>
            </div>
          </div>
        </div>  
        <div className="card text-center shadow-lg p-3 mb-3 w-100">
          <div className="card-body">
            <div className="card-text">
              <h5>Industriales</h5>
              { apiIndustriaResponse === 'Hubo un error al obtener la respuesta.' ? (
                <p></p>
              ) : (
                <p>{apiIndustriaResponse}</p>
              )}
              <button
                className="btn btn-primary"
                onClick={() => handleButtonClick('http://127.0.0.1:5000/getIndustrial')}
              >
                Ver mapa interactivo
              </button>
            </div>
          </div>
        </div>

        <div className="card text-center shadow-lg p-3 mb-3 w-100">
          <div className="card-body">
            <div className="card-text">
              <h5>Hospitales</h5>
                { apiHospitalesResponse === 'Hubo un error al obtener la respuesta.' ? (
                <p></p>
              ) : (
                <p>{apiHospitalesResponse}</p>
              )}
              <button
                className="btn btn-primary"
                onClick={() => handleButtonClick('http://127.0.0.1:5000/getHospitales')}>
                Ver mapa interactivo
              </button>
            </div>
          </div>
        </div>
      </div>
    </>
  );
};

export default MapasInterComponent;
