import React from 'react';
import './Footer.css';

function Footer() {
  return (
    <footer id="fondo" className="container-fluid text-body-secondary" data-bs-theme="dark">
        <div className="py-3">
            <h5 id="frase" className="text-center text-body-secondary mt-3 mb-5">"Para mejorar tu comunidad primero debes conocerla."</h5>
            <p className="text-center text-body-secondary">© 2024 Climate Alchemists for NASA Space Apps Guanajuato</p>
        </div>
    </footer>
  );
}

export default Footer;
