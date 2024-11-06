import React, { useState, useEffect,useContext } from 'react';
import logo from '../logo.png';
import '../css/plant.css';
import { useParams,useNavigate } from 'react-router-dom';
import { UserContext } from '../App';

export const PlantDetails = ({ state }) => {
  const { plant_name } = useParams();
  const [plant, setPlant] = useState(null);
  const {currentUser}  = useContext(UserContext)
  const { user_plant_id } = useParams();

  const navigate=useNavigate();
  useEffect(() => {
    if (state === 'newPlant') {
      fetch(`http://localhost:8000/plantpal/plant/${plant_name}`)
        .then((response) => {
          return response.ok
            ? response.json()
            : alert("500 err, internal server error, try again later.");
        })
        .then((data) => {
          setPlant(data[0]);
        })
        .catch((error) => {
          console.error(error);
          alert("There was a problem calling the server, please try again later.");
        });
    }
    else{
      fetch(`http://localhost:8000/plantpal/user/plant/${user_plant_id}`)
        .then((response) => {
          return (response.ok?  response.json():  response.json().then(data => { throw data; }) )
        })
        .then((data) => {
          setPlant(data[0]);
        })
        .catch((error) => {
          cconsole.error('Error:', error); // הדפס את השגיאה בקונסול
          alert(`Error : ${error.error_code}\n ${error.message}`); // הצג את קוד השגיאה והודעת השגיאה);
        });
    }
  }, [user_plant_id, state,plant_name]);
  const handleRemove=()=>{
    fetch(`http://localhost:8000/plantpal/user/plant/${user_plant_id}`, {method: 'DELETE',headers: {'Content-Type': 'application/json',},
    })
      .then(response => {
        response.ok?  response.json():  response.json().then(data => { throw data; }) 
      })
      .then(data => {
        alert("plant was deleted")
        navigate(`/users/${currentUser.user_id}/garden`)
      })
      .catch((error) => {
        console.error('Error:', error); // הדפס את השגיאה בקונסול
      alert(`Error : ${error.error_code}\n ${error.message}`); // הצג את קוד השגיאה והודעת השגיאה);
      });
  }
  if (!plant) {
    return <div>Loading...</div>;
  }

  return (
    <div className="plant-details">
      <img src={logo} alt="Logo" className="logo" />
      <h2>your plant: {plant.plant_name}</h2>
      <img src={plant.picture} alt={plant.plant_name} className="plantimage" />
      <div className="plant-info">
        <div>
          <h3>General Info:</h3>
          <p>{plant.general_info}</p>
        </div>
        <div>
          <h3>Treatment:</h3>
          <p>{plant.treatment}</p>
        </div>
      </div>
      {state !== "newPlant" && (
        <div >
          <div>
            <h3>Last Watering Reminder:</h3>
            <p>{plant.last_watering_reminder}</p>
          </div>
          <button onClick={handleRemove}  className='anotherbuttons'>Remove from my garden</button>
        </div>
      )}
      <button onClick={()=>navigate(`/users/${currentUser.user_id}/garden`)} className='anotherbuttons'>back to my garden</button>
    </div>
  );
};
