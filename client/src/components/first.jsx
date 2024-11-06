import React, { useState} from 'react';
import { useNavigate } from 'react-router-dom';
import '../css/first.css'; // כאן נייבא את קובץ ה-CSS
import logo from '../logo.png'; // Update the path based on your file structure

export const LandingPage = () => {
  const navigate = useNavigate()
  return (
    <div className="landing-page">
    <img src={logo} alt="Logo" className="logo" />
    

      <div className="buttons-container">
        <button onClick={() =>navigate('/login') }>Registered User</button>
        <button onClick={() => navigate('/register')}>New User</button>
      </div>
      
    </div>
  );
};



