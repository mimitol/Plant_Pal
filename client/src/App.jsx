import { useState } from 'react'
import { createContext } from 'react'
import { Route, Router, Routes } from 'react-router-dom'

import './App.css'
import { LandingPage } from './components/first'
import { LoginPage } from './components/login'
import { RegisterPage } from './components/signUp'
import { PlantDetails } from './components/plant'
import { MyGarden } from './components/garden'
import { AddPlant } from './components/addPlant'
import { NotFound } from './components/NotFound'

export const UserContext = createContext();
export const ReRenderContext = createContext();
function App() {
  const [currentUser, setCurrentUser] = useState({});
  return (
    <UserContext.Provider value={{ currentUser, setCurrentUser }}>
        <Routes>
          <Route index element={<LandingPage />} />
          {/* <Route index element={<ShowMessage />} /> */}
          <Route path='/login' element={<LoginPage />} />
          <Route path='/register' element={<RegisterPage />} />
          <Route path='/users/:userId/garden' element={<MyGarden />} />
          <Route path='/users/:userId/garden/plant/:user_plant_id' element={<PlantDetails state={"plant"} />} />
          <Route path='/users/:userId/garden/newplant/:plant_name' element={<PlantDetails state={"newPlant"} />} />
          <Route path='/users/:userId/garden/addplant' element={<AddPlant />} />
          <Route path='*' element={<NotFound />} />
        </Routes>
    </UserContext.Provider >
  )
}

export default App
