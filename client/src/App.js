import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { Sidebar, Navbar, Search, Charity } from './components';
import Login from './DonatePage/Login';
import CharityPage from './CharityPage/CharityPage';
import Admin from './AdminPage/Admin';
import Home from './DonatePage/Home';

const App = () => {
  const [isLoggedIn, setIsLoggedIn] = useState(false);

  // Function to handle login (you can customize this as needed)
  const handleLogin = (username, password) => {
    // Perform login logic here and set isLoggedIn to true if successful
    setIsLoggedIn(true);
  };

  return (
    <Router>
      <div className="relative sm:-8 p-4 bg-[#13131a] min-h-screen flex flex-row">
        {isLoggedIn && (
          <div className="sm:flex hidden mr-10 relative">
         
          </div>
        )}

        <div className="flex-1 max-sm:w-full max-w-[1280px] mx-auto sm:pr-5">
          <Routes>
            <Route path="/" element={isLoggedIn ? (
              <>
               
              </>
            ) : (
              <Login handleLogin={handleLogin} />
            )} />

            {/* Route for the CharityPage component */}
            <Route path="/Home" element={<Home />} />
            <Route path="/login" element={<Login />} />


            <Route path="/CharityPage" element={<CharityPage />} />

            {/* Route for the Admin component */}
            <Route path="/admin" element={<Admin />} />
          </Routes>
        </div>
      </div>
    </Router>
  );
};

export default App;
