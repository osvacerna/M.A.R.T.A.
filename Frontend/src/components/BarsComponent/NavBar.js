import React from 'react';
import './NavBar.css';

function NavBar({ goToAgeSlider }) {
  return (
    <nav className="navbar fixed-top">
      <form className="container-fluid justify-content-start">
        <button type="button" className="btn btn-success m-1" onClick={goToAgeSlider}>Inicio</button>
        <a href="https://github.com/osvacerna/M.A.R.T.A.">
         <button type="button" class="habilidad_boton btn btn-lg px-4 me-md-2 text-white btn-sm btn-secondary m-1">Nosotros</button>
        </a>
      </form>
    </nav>
  );
}

export default NavBar;
