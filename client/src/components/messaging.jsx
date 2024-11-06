
import {useState} from 'react';
import { fetchToken, onMessageListener } from '../firebase/firebaseConfig';
import {Button, Toast} from 'react-bootstrap';
import 'bootstrap/dist/css/bootstrap.min.css';

  const GetToken=(setTokenForUser)=>{
  const getToken=()=>{
  const [show, setShow] = useState(false);
  const [notification, setNotification] = useState({title: '', body: ''});
  const [isTokenFound, setTokenFound] = useState(false);
  fetchToken(setTokenFound,setTokenForUser);
  
  onMessageListener().then(payload => {
    setNotification({title: payload.notification.title, body: payload.notification.body})
    setShow(true);
    console.log(payload);
  }).catch(err => console.log('failed: ', err));}
  return (
    <div >
    </div>
  );
}

