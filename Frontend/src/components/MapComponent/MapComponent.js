import React, {useCallback } from 'react';
import {GoogleMap, useLoadScript } from '@react-google-maps/api';
import { environment } from '../../environments/environment.ts';


const libraries = ['places'];
const mapContainerStyle = {
  width: '100%',
  height: '100vh',
};

const center = {
  lat: 21.01656,
  lng: -101.253353, // Guanajuato como centro
};

const options = {
  disableDefaultUI: false,
  zoomControl: true,
};

let GoogleMapsApiKey = environment.GoogleMapsApiKey;

function MapComponent({onMapClick}) {

  const { isLoaded, loadError } = useLoadScript({
    googleMapsApiKey: GoogleMapsApiKey,
    libraries,
  });

  const handleClick = useCallback((event) => {
    // Capturamos las coordenadas cuando el usuario hace clic en el mapa
    const coords = {
      lat: event.latLng.lat(),
      lng: event.latLng.lng(),
    };

  onMapClick(coords);
  }, [onMapClick]);

  if (loadError) return <div>Error al cargar el mapa</div>;
  if (!isLoaded) return <div>Cargando mapa...</div>;

  return (
      <GoogleMap
        mapContainerStyle={mapContainerStyle}
        zoom={8}
        center={center}
        options={options}
        onClick={handleClick}
      >
      </GoogleMap>  
  );
}

export default MapComponent;