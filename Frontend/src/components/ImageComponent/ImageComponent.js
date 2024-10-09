import React from 'react';

function ImageComponent (){
  return (
    <div className="d-flex flex-column align-items-start w-100  h-95">
      <div className="card text-center shadow-lg p-3 mb-3 w-100">
        <div className="card-title">
          <h2 className="card-title">Propuesta de áreas verdes</h2>
        </div>
      </div>
      <div className="card text-center shadow-lg p-3 mb-3 w-100">
        <div className="card-body">
          <img src="http://127.0.0.1:5000/getImage" alt="Propuesta" width="550" height="450"></img>
        </div>
      </div>
    </div>
  );
}

export default ImageComponent;
