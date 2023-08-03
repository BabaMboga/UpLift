import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';

const Admin = () => {
  const [showModal, setShowModal] = useState(false);
  const [charities, setCharities] = useState([]);
  const [charityApplications, setCharityApplications] = useState([]);
  const [approvedCharities, setApprovedCharities] = useState([]);

  const [currentApplicationIndex, setCurrentApplicationIndex] = useState(0);

  const handleApprove = () => {
    const approvedCharity = charityApplications[currentApplicationIndex];
    setApprovedCharities((prevCharities) => [...prevCharities, approvedCharity]);

    // Remove the approved charity application from the list
    setCharityApplications((prevApplications) =>
      prevApplications.filter((_, index) => index !== currentApplicationIndex)
    );

    // Show an alert message
    alert(`You have successfully approved ${approvedCharity.name} on the uplift platform`);
  };

  const handleReject = () => {
    // Remove the rejected charity application from the list
    setCharityApplications((prevApplications) =>
      prevApplications.filter((_, index) => index !== currentApplicationIndex)
    );

    // Show an alert message
    alert('You have been denied access to uplift platform. Try again later.');
  };

  const handleNextApplication = () => {
    if (currentApplicationIndex < charityApplications.length - 1) {
      setCurrentApplicationIndex((prevIndex) => prevIndex + 1);
    } else {
      setShowModal(false);
    }
  };

  useEffect(() => {
    fetch('http://localhost:4000/application')
      .then((response) => response.json())
      .then((data) => setCharityApplications(data))
      .catch((error) => console.error('Error fetching charity applications:', error));

    fetch('http://localhost:5000/charities')
      .then((response) => response.json())
      .then((data) => setCharities(data))
      .catch((error) => console.error('Error fetching charities:', error));

    // Retrieve approved charities from local storage on page load
    const storedApprovedCharities = JSON.parse(localStorage.getItem('approvedCharities'));
    if (storedApprovedCharities) {
      setApprovedCharities(storedApprovedCharities);
    }
  }, []);

  useEffect(() => {
    // Store approved charities in local storage whenever the approvedCharities state changes
    localStorage.setItem('approvedCharities', JSON.stringify(approvedCharities));
  }, [approvedCharities]);

  const handleDeleteCharity = (charityId) => {
    fetch(`http://localhost:5000/charities/${charityId}`, {
      method: 'DELETE',
    })
      .then((response) => response.json())
      .then(() => {
        // Update the state to remove the deleted charity from the list
        setCharities((prevCharities) =>
          prevCharities.filter((charity) => charity.id !== charityId)
        );
      })
      .catch((error) => console.error('Error deleting charity:', error));
  };

  return (
    <div>
      <div className="flex md:flex-row flex-col-reverse justify-end mb-[35px] gap-6">
        <div className="sm:flex hidden flex-row justify-end gap-4 text-white">
          <div
            to="/login"
            className="font-epilogue cursor-pointer mt-3 bg-white text-black py-2 px-4 rounded-[10px]"
            onClick={() => setShowModal(true)}
          >
            Approve
          </div>
          <Link
            to="/login"
            className="font-epilogue cursor-pointer mt-3 bg-white text-black py-2 px-4 rounded-[10px]"
          >
            Logout
          </Link>
        </div>
      </div>

      {showModal && (
        <div className="fixed inset-0 flex items-center justify-center bg-opacity-50 bg-gray-700 font-epilogue">
          <div className="bg-white p-4 rounded-lg">
            {/* Modal content */}
            <button
              className="absolute top-2 right-2 text-whitehover:text-gray-800"
              onClick={() => setShowModal(false)}
            >
              X
            </button>
            <h2 className="text-xl font-epilogue font-semibold mb-2">
              Review All Charity Application
            </h2>
            {charityApplications.length > 0 ? (
              <>
                <p className="mb-4 font-epilogue">
                  Application for: {charityApplications[currentApplicationIndex].name}
                </p>
                <p className="font-epilogue text-black "> Description:
                  {charityApplications[currentApplicationIndex].description}
                </p>
                <div className="flex space-x-4 mt-4">
                  <button
                    onClick={handleApprove}
                    className="bg-green-500 text-white px-4 py-2 rounded-lg"
                  >
                    Approve
                  </button>
                  <button
                    onClick={handleReject}
                    className="bg-red-500 text-white px-4 py-2 rounded-lg"
                  >
                    Reject
                  </button>
                </div>
                <button
                  onClick={handleNextApplication}
                  className="bg-gray-500 text-white px-4 py-2 mt-4 rounded-lg"
                >
                  Next Application
                </button>
              </>
            ) : (
              <p>No charity applications to review.</p>
            )}
          </div>
        </div>
      )}

      <h1 className="font-epilogue font-semibold text-[28px] text-white text-left mt-6">
        Admin page
      </h1>
      <ul className="mt-8">
        {charities.map((charity) => (
          <li key={charity.id} className="text-white font-epilogue font-semibold flex items-center space-x-4">
            <img
              src={charity.logo}
              alt={charity.name}
              className="w-20 h-20 object-cover rounded-full"
            />
            <span>{charity.name}</span>
            <button
              onClick={() => handleDeleteCharity(charity.id)}
              className="ml-2 bg-red-500 text-white px-4 py-1 rounded"
            >
              Delete
            </button>
          </li>
        ))}
      </ul>
      <div>
        <h1 className="font-epilogue font-semibold text-[28px] text-white text-left mt-6">
          Approved charities
        </h1>
        {/* Display the approved charities */}
        <ul>
          {approvedCharities.map((charity) => (
            <li key={charity.id}>
              <div>
                <img
                  src={charity.imageURL} // Make sure to use the appropriate property for the image URL
                  alt={charity.name}
                  className="w-20 h-20 object-cover rounded-full"
                />
                <h3 className='text-white'>{charity.name}</h3>
                <p>{charity.description}</p>
              </div>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
};

export default Admin;
