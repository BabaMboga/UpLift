import React from 'react';
import { Link } from 'react-router-dom'; // Import the Link component

const Navbar = () => {


  return (
    <div className="flex md:flex-row flex-col-reverse justify-end mb-[35px] gap-6">
      <div className="sm:flex hidden flex-row justify-end gap-4 text-white">
        {/* Use Link component to navigate to the login page */}
        <Link to="/login" className="font-epilogue cursor-pointer mt-3 bg-white text-black py-2 px-4 rounded-[10px]">
          Logout
        </Link>
      </div>
    </div>
  );
};

export default Navbar;
