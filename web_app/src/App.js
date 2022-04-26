import React from 'react';
import './App.css';
import {BrowserRouter, Route} from "react-router-dom";
import NewReminder from "./components/NewReminder";


function App() {
    return (
        <BrowserRouter>
            <Route path="/NewReminder">
                <NewReminder/>
            </Route>
        </BrowserRouter>
    );
}

export default App;