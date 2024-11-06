import { React, useContext, useState, useEffect } from 'react';
import { PlantItem } from '../components/plantInList.jsx';
import logo from '../logo.png';
import { useNavigate } from "react-router-dom";
import { UserContext } from '../App';
import '../css/garden.css';
export const MyGarden = () => {
  const [plantsArray, setPlantsArray] = useState([]);
  const { currentUser, setCurrentUser } = useContext(UserContext)
  const navigate = useNavigate()
  useEffect(() => {
    fetch(`http://localhost:8000/plantpal/user/plants/${currentUser.user_id}`)
      .then((response) => {
        return (
          response.ok?  response.json():  response.json().then(data => { throw data; }) 
        );
      })
      .then((data) => {
        setPlantsArray(data);
      })
      .catch((error) => {
        console.error('Error:', error); // הדפס את השגיאה בקונסול
      alert(`Error : ${error.error_code}\n ${error.message}`); // הצג את קוד השגיאה והודעת השגיאה);
      });
  }, [currentUser]);
  const handleWatchPlantDetails=(user_plant_id)=>{
    navigate(`/users/${currentUser.user_id}/garden/plant/${user_plant_id}`)
  }
  return (
    <div className="my-garden">
      <img src={logo} alt="Garden Logo" className="garden-logo" />
      <h1>My Garden...</h1>
      {plantsArray.length > 0 ?
        (
          <div className="plants-list">
            {plantsArray.map((plant, index) => (<PlantItem key={index} plant={plant} handleWatchPlantDetails={handleWatchPlantDetails}/>))}
          </div>)
        :
        (<h2>you dont have any plants, add one now!</h2>)}

      <button className="add-plant-button" onClick={() => { navigate(`/users/${currentUser.user_id}/garden/addplant`) }}>
        Add Plant
      </button>
    </div>
  );
};
