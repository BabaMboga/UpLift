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
    fetch('http://127.0.0.1:5000/applications')
      .then((response) => response.json())
      .then((data) => setCharityApplications(data))
      .catch((error) => console.error('Error fetching charity applications:', error))

    fetch('http://127.0.0.1:5000/charities')
      .then((response) => response.json())
      .then((data) => setCharities(data.charities))
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


  const handleDelete = (charityId) => {
    fetch(`http://127.0.0.1:5000/api/charities/${charityId}`, {
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json',
        // You might need to include authentication headers if your API requires them
      },
    })
      .then((response) => response.json())
      .then((data) => {
        console.log(data); // You can customize this based on your needs
        // Remove the deleted charity from the list
        setCharities((prevCharities) =>
          prevCharities.filter((charity) => charity.charity_id !== charityId)
        );
      })
      .catch((error) => {
        console.error('Error deleting charity:', error);
      });
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
              className="absolute top-2 right-2 text-white text-[28px] font-bold"
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

                <button
                   onClick={() => setShowModal(false)}
                  className="bg-red-400 text-white px-4 py-2 mt-4 rounded-lg ml-4"
                >
                  close
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
      <div className="mt-8 grid grid-cols-2 gap-4">
  {charities.map((charity) => (
    <div key={charity.id} className="text-white font-epilogue font-semibold flex items-center space-x-4">
      <img
        src={charity.image_url}
        alt={charity.name}
        className="w-20 h-20 object-cover rounded-full"
      />
      <span>{charity.name}</span>
      <button
 onClick={() => handleDelete(charity.charity_id)}// Use charity.charity_id
  className="ml-2 bg-red-500 text-white px-4 py-1 rounded"
>
  Delete
</button>
    </div>
  ))}
</div>


      <div>
        <h1 className="font-epilogue font-semibold text-[28px] text-white text-left mt-6">
          Approved charities
        </h1>
        {/* Display the approved charities */}
        {approvedCharities.length > 0 ? (
  <div className="grid grid-cols-2 gap-4">
  {approvedCharities.map((charity) => (
    <div key={charity.id} className="text-white">
      <img
        src={charity.imageURL}
        className="w-20 h-20 object-cover rounded-full"
        alt=''
      />
      <h3 className='text-white'>{charity.name}</h3>
      <p className='text-white'>{charity.description}</p>
    </div>
  ))}
</div>

) : (
  <p className="font-epilogue font-semibold text-[12px] text-white text-left mt-6">No approved charities found.</p>
)}
      </div>
    </div>
  );
};

export default Admin;
