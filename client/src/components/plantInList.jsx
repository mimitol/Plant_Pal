 import '../css/plantInList.css';
import React from 'react';

export const PlantItem = ({ plant,handleWatchPlantDetails }) => {
  return (
    <div className="plant-item" onClick={()=>handleWatchPlantDetails(plant.id)}>
      <img src={plant.uploaded_photo} alt={plant.plant_name} className="plant-image" />
      <h2 className="plant-name">{plant.plant_name}</h2>
    </div>
  );
};


