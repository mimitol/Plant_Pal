import React, { useState, useContext } from 'react';
import logo from '../logo.png'; // ניתן לשנות את הנתיב בהתאם למיקום של הלוגו בפרוייקט
import '../css/login.css'; // כאן נייבא את קובץ ה-CSS
import { useNavigate } from 'react-router-dom';
import { UserContext } from '../App';

export const LoginPage = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [buttonState,setButtonState]=useState("none");
  const { currentUser, setCurrentUser } = useContext(UserContext)
  const navigate = useNavigate()
  const handleLogin = () => {
    let user = { password: password, email: email };
    fetch(`http://localhost:8000/plantpal/user/login/${user.email}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(user)
    })
      .then(response => {
        if (response.ok) {
          return response.json(); // אם התקבלה תגובה בהצלחה, קרא את ה-JSON
        } else {
          return response.json().then(data => { throw data; }); // אחרת, הטול יזרוק את התגובה המבנית בתוך JSON
        }
      })
      .then(data => {
        setCurrentUser({ userName: data[0].user_name, user_id: data[0].user_id });
        navigate(`/users/${data[0].user_id}/garden`);
      })
      .catch(error => {
        console.error('Server Error:', error); // הדפס את השגיאה בקונסול
        alert(`Error : ${error.error_code}\n${error.message}`); // הצג את קוד השגיאה והודעת השגיאה
        setButtonState('block')

      });

  };

  return (
    <div className="login-page">
      <img src={logo} alt="Logo" className="logo" />

      <div className="login-form">
        <input
          type="text"
          placeholder="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />
        <input
          type="password"
          placeholder="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
        <button onClick={handleLogin}>login</button>
        <button onClick={() => { navigate('/register') }} style={{display:buttonState}}>move to register page</button>

      </div>
    </div>
  );
};
