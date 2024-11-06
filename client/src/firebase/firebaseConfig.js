// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getMessaging, getToken, onMessage } from "firebase/messaging";

// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
  apiKey: "AIzaSyBr7xWaObcrrap6ZetZU5wRaCQxeHwczAc",
  authDomain: "plants-fire-base.firebaseapp.com",
  projectId: "plants-fire-base",
  storageBucket: "plants-fire-base.appspot.com",
  messagingSenderId: "222374400767",
  appId: "1:222374400767:web:23e5fffff48fe70df1b2ca",
  measurementId: "G-EWGDB63QC3"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const messaging = getMessaging(app);

export const fetchToken = (setTokenFound,setTokenForUser) => {
    return getToken(messaging, {vapidKey: 'BPt65DkAC_Nifm3C_syno7IMa62QEZ3cgi6zOZLjcga2iZuc4qmMlF0-I5sv2pS9MPXc8_kYfSzaKVr8_sg8oOg'}).then((currentToken) => {
      if (currentToken) {
        console.log('current token for client: ', currentToken);
        setTokenForUser(currentToken)
        setTokenFound(true);
        // Track the token -> client mapping, by sending to backend server
        // show on the UI that permission is secured
      } else {
        console.log('No registration token available. Request permission to generate one.');
        setTokenFound(false);
        // shows on the UI that permission is required 
      }
    }).catch((err) => {
      console.log('An error occurred while retrieving token. ', err);
      // catch error while creating client token
    });
  }
  
  export const onMessageListener = () =>
    new Promise((resolve) => {
      onMessage(messaging, (payload) => {
        resolve(payload);
      });
  });