import React, { useState, useContext, useEffect } from 'react';
import ClipLoader from 'react-spinners/ClipLoader';
import logo from '../logo.png';
import '../css/addPlant.css';
import { useNavigate } from 'react-router-dom';
import { UserContext } from '../App';
import { format } from 'date-fns';

export const AddPlant = () => {
  const [imagesArray, setImagesArray] = useState([]);
  const [identified, setIdentified] = useState(false);
  const [predictedPlants, setPredictedPlants] = useState([]);
  const [uploadedPhotos, setUploadedPhotos] = useState();
  const [selectedCategory, setSelectedCategory] = useState(-1);
  const { currentUser, setCurrentUser } = useContext(UserContext);
  const [uploadedPhotoLocationInServer, setUploadedPhotoLocationInServer] = useState('');
  const navigate = useNavigate();
  const [selected_plant_index, setSelected_plant_index] = useState(-1);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (uploadedPhotoLocationInServer) {
      handleAddPlant();
    }
  }, [uploadedPhotoLocationInServer]);

  const handleImageChange = (event) => {
    const files = Array.from(event.target.files);
    if (files.length <= 3) {
      setImagesArray(files);
    } else {
      alert("Please upload only up to 3 images.");
      event.target.value = null;
    }
  };

  const sendImages = () => {
    fetch(`http://127.0.0.1:8000/plantpal/plant/images/${selectedCategory}`, { method: 'PUT', headers: { 'Content-Type': 'application/json', }, body: JSON.stringify(uploadedPhotos), })
      .then((response) => {
        console.log(response);
        if (response.ok) {
          return response.json();
        } else {
          alert("Internal server error, check your connection and try again");
        }
      })
      .then((data) => {
        setUploadedPhotoLocationInServer(data);
      })
      .catch((error) => {
        console.log(error);
        alert("There was a problem calling the server.");
      });
  }

  const handleAddPlant = () => {
    const currentDate = new Date();
    const formattedDate = format(currentDate, 'yyyy-MM-dd');
    let newUsersPlant = {
      user_id: currentUser.user_id,
      plant_id: predictedPlants[selected_plant_index].plant_id,
      date_added: formattedDate,
      plant_status: 1,
      last_watering_reminder: formattedDate,
      uploaded_photo: uploadedPhotoLocationInServer
    }
    fetch(`http://127.0.0.1:8000/plantpal/user/plant`, { method: 'POST', headers: { 'Content-Type': 'application/json', }, body: JSON.stringify(newUsersPlant), })
      .then((response) => {
        response.ok ? navigate(`/users/${currentUser.user_id}/garden/newplant/${predictedPlants[selected_plant_index].plant_name}`) :
          alert("Internal server error, check your connection and try again");
      })
      .catch((error) => {
        console.error(error);
        alert("There was a problem calling the server, please try again later.");
      });
  }

  const handleIdentify = () => {
    const formData = new FormData();
    for (let i = 0; i < imagesArray.length; i++) {
      formData.append('images', imagesArray[i]);
    }

    setLoading(true);

    fetch('http://localhost:8000/plantpal/plant/identify/', {
      method: 'POST',
      body: formData,
    })
      .then((response) => {
        setLoading(false);
        if (response.ok) {
          return response.json();
        } else {
          alert("Internal server error, check your connection and try again");
        }
      })
      .then((data) => {
        setIdentified(true);
        setPredictedPlants(data.categories);
        setUploadedPhotos(data.uploaded_photos);
      })
      .catch((error) => {
        setLoading(false);
        console.error(error);
        alert("There was a problem calling the server, please try again later.");
      });
  };

  return (
    <div className="upload-plant-container">
      <img src={logo} alt="Logo" className="logo" />
      <div className="instructions">Please upload or take 3 pictures:</div>
      <div className="upload-buttons">
        <input
          id="upload"
          type="file"
          accept="image/*"
          capture="camera"
          multiple
          onChange={handleImageChange}
        />
        <label htmlFor="upload">Upload or Take Pictures</label>
      </div>
      <div className="preview-images">
        {imagesArray.map((image, index) => (
          <img key={index} src={URL.createObjectURL(image)} alt={`Upload ${index + 1}`} />
        ))}
      </div>
      {imagesArray.length > 0 && (
        <button
          className="identify-button"
          onClick={handleIdentify}
          disabled={imagesArray.length !== 3 || loading}
        >
          Identify
        </button>
      )}
      {loading && (
        <div className="loading-indicator">
          <ClipLoader size={50} color={"#123abc"} loading={loading} />
        </div>
      )}
      {identified && (
        <div className="result-section">
          <h3>Your plant identified as one of the plants below,</h3>
          <p>Choose the picture that looks most similar to your plant. </p>
          <div className="result-images">
            <div>
              <img
                src={predictedPlants[0].picture}
                alt="predictedPlants1"
                className={selectedCategory === predictedPlants[0].plant_name ? 'selected-image' : 'first'}
                onClick={() => { setSelected_plant_index(0); setSelectedCategory(predictedPlants[0].id_in_model) }}
              />
              <p>{predictedPlants[0].plant_name}</p>
            </div>
            <div>
              <img
                src={predictedPlants[1].picture}
                alt="predictedPlants2"
                className={selectedCategory === predictedPlants[1].plant_name ? 'selected-image' : 'second'}
                onClick={() => { setSelected_plant_index(1); setSelectedCategory(predictedPlants[1].id_in_model) }}
              />
              <p>{predictedPlants[1].plant_name}</p>
            </div>
            <div>
              <img
                src={predictedPlants[2].picture}
                alt="predictedPlants3"
                className={selectedCategory === predictedPlants[2].plant_name ? 'selected-image' : 'third'}
                onClick={() => { setSelected_plant_index(2); setSelectedCategory(predictedPlants[2].id_in_model) }}
              />
              <p>{predictedPlants[2].plant_name}</p>
            </div>
          </div>
        </div>
      )}
      {selected_plant_index >= 0 && (<button onClick={sendImages} className='anotherbuttons'>add to my garden</button>)}
    </div>
  );
};
