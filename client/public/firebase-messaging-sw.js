// Scripts for firebase and firebase messaging
importScripts('https://www.gstatic.com/firebasejs/9.0.0/firebase-app-compat.js');
importScripts('https://www.gstatic.com/firebasejs/9.0.0/firebase-messaging-compat.js');

// Initialize the Firebase app in the service worker by passing the generated config
const firebaseConfig = {
    apiKey: "AIzaSyBr7xWaObcrrap6ZetZU5wRaCQxeHwczAc",
    authDomain: "plants-fire-base.firebaseapp.com",
    projectId: "plants-fire-base",
    storageBucket: "plants-fire-base.appspot.com",
    messagingSenderId: "222374400767",
    appId: "1:222374400767:web:23e5fffff48fe70df1b2ca",
    measurementId: "G-EWGDB63QC3"
};

firebase.initializeApp(firebaseConfig);

// Retrieve firebase messaging
const messaging = firebase.messaging();

messaging.onBackgroundMessage(function(payload) {
  console.log('Received background message ', payload);

  const notificationTitle = payload.notification.title;
  const notificationOptions = {
    body: payload.notification.body,
  };

  self.registration.showNotification(notificationTitle,
    notificationOptions);
});