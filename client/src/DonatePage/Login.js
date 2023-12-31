import React, { useState } from 'react';

import { charity } from '../assets';
import Typed from 'react-typed';

const Login = () => {
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [selectedUserType, setSelectedUserType] = useState(null);
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [ setErrorMessage] = useState('');
  const [selectedRole, setSelectedRole] = useState('donor'); // Initialize with a default role


// sign up states
  const [showModal, setShowModal] = useState(false);
  const [signemail, setsignEmail] = useState('');
  const [signpassword, setsignPassword] = useState('');

  const handleSignUpClick = () => {
    setShowModal(true);
  };

  const handleModalClose = () => {
    setShowModal(false);
  };

  const handleSignUp = () => {
    const formData = { email: signemail, password: signpassword, role: selectedRole }; // Include selected role
  
    // Replace 'https://example.com/api/signup' with your actual backend API URL
    fetch('http://127.0.0.1:5000/api/signup', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(formData),
    })
      .then((response) => response.json())
      .then((data) => {
        console.log('Sign-up data saved:', data);
        handleModalClose();
      })
      .catch((error) => {
        console.error('Error saving sign-up data:', error);
      });
  };
  

  const handleLogin = async () => {
    const response = await fetch('http://127.0.0.1:5000/login', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ email, password }),
    });

    const data = await response.json();

    if (response.ok) {
      // Store user information in localStorage
      localStorage.setItem('access_token', data.access_token);
      localStorage.setItem('user_id', data.user_id);
      localStorage.setItem('role', data.role);
    
      // Redirect users based on their role
      switch (data.role) {
        case 'donor':
          window.location.href = '/Home';  // Make sure this route exists
          break;
        case 'charity':
          window.location.href = '/CharityPage';  // Make sure this route exists
          break;
        case 'admin':
          window.location.href = '/admin';  // Make sure this route exists
          break;
        default:
          // Handle unknown role or redirect to a default route
          console.error('Unknown role:', data.role);
          // You might want to redirect to a default route here
          break;
      }
    } else {
      setErrorMessage(data.message); // Display error message
    }
  };
    
  const handleLoginClick = () => {
    setIsModalOpen(true);
  };

  const handleCloseModal = () => {
    setIsModalOpen(false);
  };

  const handleLoginOptionClick = (userType) => {
    setSelectedUserType(userType);
  };

  const renderLoginForm = () => {
    switch (selectedUserType) {
      case 'donor':
        return (
          <form>
            {/* Donor Login Form */}
            <div className="mb-4 font-epilogue">
              <label htmlFor="donor-username" className="block font-medium mb-1" >
                Donor email:
              </label>
              <input
            type='text'
            placeholder='email'
            className='bg-gray-600 text-white px-4 py-2 rounded'
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />
            </div>
            <div className="mb-4 font-epilogue">
              <label htmlFor="donor-password" className="block font-medium mb-1">
                Donor Password:
              </label>
              <input
            type='password'
            placeholder='Password'
            className='bg-gray-600 text-white px-4 py-2 rounded'
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
            </div>
            <button type="submit"  className='bg-[#82cfb7] hover:bg-green-200 px-4 py-2 rounded' onClick={handleLogin}>
              Login as donor
            </button>
          </form>
        );
      case 'charity':
        return (
          <form>
            {/* Charity Login Form */}
            <div className="mb-4 font-epilogue">
              <label htmlFor="charity-username" className="block font-medium mb-1">
                Charity email:
              </label>
              <input
            type='text'
            placeholder='email'
            className='bg-gray-600 text-white px-4 py-2 rounded'
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />
            </div>
            <div className="mb-4 font-epilogue">
              <label htmlFor="charity-password" className="block font-medium mb-1">
                Charity Password:
              </label>
              <input
            type='password'
            placeholder='Password'
            className='bg-gray-600 text-white px-4 py-2 rounded'
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
            </div>
            <button
            className='bg-[#82cfb7] hover:bg-green-200 px-4 py-2 rounded'
            onClick={handleLogin}
          >
            Login as charity
          </button>
          </form>
        );
      case 'admin':
        return (
          <form>
            {/* Admin Login Form */}
            <div className="mb-4">
              <label htmlFor="admin-username" className="block font-medium mb-1">
                Admin email:
              </label>
              <input
            type='text'
            placeholder='email'
            className='bg-gray-600 text-white px-4 py-2 rounded'
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />
            </div>
            <div className="mb-4">
              <label htmlFor="admin-password" className="font-epilogue block font-medium mb-1">
                Admin Password:
              </label>
              <input
            type='password'
            placeholder='Password'
            className='bg-gray-600 text-white px-4 py-2 rounded'
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
            </div>
            <button type="submit"  className='bg-[#82cfb7] hover:bg-green-200 px-4 py-2 rounded' onClick={handleLogin}>
              Login as Admin
            </button>
          </form>
        );
        
      default:
        return null;
    }
  };


  return (
    <div className="flex flex-col min-h-screen">
      {/* Navbar */}

      <div className=" p-4 text-white flex justify-end gap-6 mt-4">
      <h1 className='font-epilogue w-full text-4xl font-bold text-[#00df9a] mt-1' >Uplift.</h1>
        <h1 className="cursor-pointer mt-3 bg-white text-black py-2 px-4 rounded-[10px]" onClick={handleLoginClick}>
          Login
        </h1>
        <h1 className="cursor-pointer mt-3 bg-white text-black py-2 px-2 rounded-[10px]" onClick={handleSignUpClick}>
          Signup
        </h1>
      </div>

      {/* Modal */}
      {isModalOpen && (
        <div className="fixed top-0 left-0 w-full h-full flex items-center justify-center bg-black bg-opacity-75">
          <div className="bg-white p-4 rounded shadow-md">
            {/* Display login options */}
            <h2 className="font-epilogue text-2xl font-semibold mb-4">Login</h2>
            <div className="grid gap-4 grid-cols-3">
              <div
                className="cursor-pointer  font-epilogue mb-2 text-center border border-green-700 p-2 rounded"
                onClick={() => handleLoginOptionClick('donor')}
              >
                Donor
              </div>
              <div
                className="cursor-pointer font-epilogue mb-2 text-center border border-green-700 p-2 rounded"
                onClick={() => handleLoginOptionClick('charity')}
              >
                Charity
              </div>
              <div
                className="cursor-pointer font-epilogue mb-2 text-center border border-green-700 p-2 rounded"
                onClick={() => handleLoginOptionClick('admin')}
              >
                Admin
              </div>
            </div>

            {/* Render the appropriate login form based on the selected user type */}
            {renderLoginForm()}
            <button onClick={handleCloseModal} className="bg-red-400 text-white rounded px-4 py-2 mt-4">
              Close
            </button>
          </div>
        </div>
      )}



    {/* modal for signup */}
{showModal && (
  <div className="fixed inset-0 z-10 flex items-center justify-center bg-black bg-opacity-50">
    <div className="bg-white p-6 rounded shadow-md">
      <h2 className="text-2xl font-bold mb-4 font-epilogue">Sign Up</h2>
      <div className="mb-4">
        <label className="block text-gray-700 font-bold mb-2 font-epilogue">Email</label>
        <input
          type="email"
          className="border rounded w-full py-2 px-3 focus:outline-none focus:shadow-outline"
          value={signemail}
          onChange={(e) => setsignEmail(e.target.value)}
        />
      </div>
      <div className="mb-4">
        <label className="block text-gray-700 font-bold mb-2 font-epilogue">Password</label>
        <input
          type="password"
          className="border rounded w-full py-2 px-3 focus:outline-none focus:shadow-outline"
          value={signpassword}
          onChange={(e) => setsignPassword(e.target.value)}
        />
      </div>
      <div className="mb-4">
        <label className="block text-gray-700 font-bold mb-2 font-epilogue">Role</label>
        <select
          className="border rounded w-full py-2 px-3 focus:outline-none focus:shadow-outline"
          value={selectedRole}
          onChange={(e) => setSelectedRole(e.target.value)}
        >
          <option value="charity">Charity</option>
          <option value="admin">Admin</option>
          <option value="donor">Donor</option>
        </select>
      </div>
      <div className="flex justify-end">
        <button
          className="bg-[#82cfb7] text-black font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline mr-2 font-epilogue"
          onClick={handleSignUp}
        >
          Sign Up
        </button>
        <button
          className="bg-red-400 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline font-epilogue"
          onClick={handleModalClose}
        >
          Cancel
        </button>
      </div>
    </div>
  </div>
)}


      <div className="w-full flex flex-grow items-center justify-center px-8 mb-20">
        <div className="flex flex-col items-center justify-center text-center w-1/2">
          <h1 className="font-epilogue text-6xl font-bold text-[#00df9a]">Charity</h1>
          <p className="font-epilogue font-semibold text-xl mt-4 text-white">Join us in making a difference.</p>
          <Typed 
          className='text-white font-epilogue'
          strings={['We are a non-profit organization that aims to help those in need.']}
          typeSpeed={120}
          backSpeed={140}
          loop
          
          
          />

        </div>

        <div className="w-1/2">
          <img src={charity} alt="Charity" className="w-full h-full object-cover rounded-[16px]" />
        </div>
      </div>
    </div>


  );
};

export default Login;