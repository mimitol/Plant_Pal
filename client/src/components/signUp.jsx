import React, { useState, useContext } from 'react';
import { useNavigate } from 'react-router-dom';
import logo from '../logo.png';
import morning from '../pics/morning.webp';
import afternoon from '../pics/afternoon.webp';
import night from '../pics/night.webp';
import '../css/signUp.css';
import { UserContext } from '../App';


import { fetchToken, onMessageListener } from '../firebase/firebaseConfig';
import { Button, Toast } from 'react-bootstrap';
import 'bootstrap/dist/css/bootstrap.min.css';
export const RegisterPage = () => {
  const [show, setShow] = useState(false);
  const [notification, setNotification] = useState({ title: '', body: '' });
  const [isTokenFound, setTokenFound] = useState(false);
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [email, setEmail] = useState('');
  const [interestedInRemainers, setInterestedInRemainers] = useState(false);
  const [selectedImage, setSelectedImage] = useState(null);
  const [tokenForReminders, setTokenForReminders] = useState('');
  const [buttonState,setButtonState]=useState("none");

  const { currentUser, setCurrentUser } = useContext(UserContext)
  const navigate = useNavigate()

  const getToken = () => {
    console.log("im in bh");

    fetchToken(setTokenFound, setTokenForReminders);
    onMessageListener().then(payload => {
      setNotification({ title: payload.notification.title, body: payload.notification.body })
      setShow(true);
      console.log(payload);
    }).catch(err => console.log('failed: ', err));
  }

  const handleRegister = () => {
    let newUser = { user_name: username, password: password, email: email, interested_in_reminders: interestedInRemainers, watering_hours: selectedImage, token_for_reminders: tokenForReminders }
    fetch(`http://localhost:8000/plantpal/user`, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(newUser) })
      .then((response) => {
        return (
          response.ok ? response.json() : response.json().then(data => { throw data; })
        );
      })
      .then((data) => {

        setCurrentUser({ userName: data[0].user_name, user_id: data[0].user_id })
        navigate(`/users/${data[0].user_id}/garden`)
      })
      .catch((error) => {
        console.error('Error:', error); // הדפס את השגיאה בקונסול
        alert(`Error : ${error.error_code}\n ${error.message}`); // הצג את קוד השגיאה והודעת השגיאה);
        setButtonState('block')

      });
  }

  return (
    <div className="login-page">
      <img src={logo} alt="Logo" className="logo" />

      <div className="login-form">
        <input
          type="text"
          placeholder="user name"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
        />
        <input
          type="password"
          placeholder="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
        <input
          type="email"
          placeholder="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />
        <label className="checkbox-label">
          <input
            type="checkbox"
            checked={interestedInRemainers}
            onChange={(e) => {
              setInterestedInRemainers(e.target.checked);
              setTokenForReminders(getToken());
            }}
          />
          <p>Interested in Remainders</p>
        </label>
        {interestedInRemainers && (
          <div>
            <h3>Choose time for reminders:</h3>
            <div className="image-container">
              <img
                src={morning}
                alt="morning"
                className={selectedImage === "morning" ? 'selected-image' : ''}
                onClick={() => setSelectedImage("morning")}
              />

              <img
                src={afternoon}
                alt="afternoon"
                className={selectedImage === "afternoon" ? 'selected-image' : ''}
                onClick={() => setSelectedImage("afternoon")}
              />

              <img
                src={night}
                alt="night"
                className={selectedImage === "night" ? 'selected-image' : ''}
                onClick={() => setSelectedImage("night")}
              />
            </div>
          </div>
        )}
        <button onClick={handleRegister}>Register</button>
        <button onClick={() => { navigate('/login') }} style={{display:buttonState}}>move to login page</button>
        <p>*I agree to the terms of the site.</p>

      </div>
    </div>
  );
}

