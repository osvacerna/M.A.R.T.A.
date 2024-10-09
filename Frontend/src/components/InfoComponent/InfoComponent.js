import React from 'react';

function InfoComponent({data, age }) {
  // Crear un arreglo de atributos a partir de data
  const dataAttributes = data ? Object.entries(data) : [];
  console.log('edad' + (age))

  return (
    <>
      <div className="d-flex flex-column align-items-center w-100">
        <div className="card text-center shadow-lg p-3 mb-3 w-100">
          <h2 className="card-title">Panel de Información</h2>
        </div>
        
        {dataAttributes.length > 0 ? (
          dataAttributes.map(([key, value], index) => (
            <div className="card text-center shadow-lg p-3 mb-3 w-100" key={index}>
              <div className="card-body">
                <div className="card-text">
                  <p><strong>{key.charAt(0).toUpperCase() + key.slice(1)}:</strong> {value}</p>
                </div>
              </div>
            </div>
          ))
        ) : (
          <div className="card text-center shadow-lg p-3 mb-3 w-100">
            <div className="card-body">
              <div className="card-text">
                <p className="text-muted">Selecciona un lugar en el mapa.</p>
              </div>
            </div>
          </div>
        )}

        
      </div>
    </>
  );
}


export default InfoComponent;
