import React, { useState ,useEffect } from 'react';
import { Link } from 'react-router-dom';

const CharityPage = () => {
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [imageURL, setImageURL] = useState('');
  const [charityName, setCharityName] = useState('');
  const [charityDescription, setCharityDescription] = useState('');
  const [beneficiaries, setBeneficiaries] = useState([]);
  const [inventory, setInventory] = useState([]);

  useEffect(() => {
    // Fetch JWT token from localStorage (if stored after login)
    const jwtToken = localStorage.getItem('jwtToken');

    // Fetch beneficiaries from the Flask backend with JWT token
    fetch('http://127.0.0.1:5000/beneficiaries/stories', {
      headers: {
        Authorization: `Bearer ${jwtToken}`, // Include JWT token in the headers
      },
    })
      .then((response) => response.json())
      .then((data) => setBeneficiaries(data.beneficiaries))
      .catch((error) => {
        console.error('Error fetching beneficiaries:', error);
      });

    // Fetch inventory from the Flask backend with JWT token
    fetch('http://127.0.0.1:5000/admin/inventory', {
      headers: {
        Authorization: `Bearer ${jwtToken}`, // Include JWT token in the headers
      },
    })
      .then((response) => response.json())
      .then((data) => setInventory(data.inventory))
      .catch((error) => {
        console.error('Error fetching inventory:', error);
      });
  }, []);


  const handleSubmit = async () => {
    try {
      const data = {
        imageURL,
        name: charityName,
        description: charityDescription,
      };

      // Make a POST request to the server using fetch
      await fetch('http://127.0.0.1:5000/application', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
      });

      // Show the success alert
      alert('You have successfully applied for charity review. Please wait for approval');

      // Close the modal after successful submission
      setIsModalOpen(false);

      // Reset the form fields
      setImageURL('');
      setCharityName('');
      setCharityDescription('');
    } catch (error) {
      console.error('Error submitting charity application:', error);
    }
  };

  return (
    <div>
      <div className="flex md:flex-row flex-col-reverse justify-end mb-35 gap-6 text-white">
        <div className="sm:flex hidden flex-row justify-end gap-4 text-white">
          <div
            onClick={() => setIsModalOpen(true)}
            className="font-epilogue cursor-pointer mt-3 bg-white text-black py-2 px-4 rounded-[10px]"
          >
            Apply for Charity
          </div>
          <Link
            to="/login"
            className="font-epilogue cursor-pointer mt-3 bg-white text-black py-2 px-4 rounded-[10px]"
          >
            Logout
          </Link>
        </div>
      </div>
{/* 
      <h1 className="text-white font-epilogue font-bold">charity page</h1> */}

<div className="container mx-auto p-8 font-epilogue">
      <h1 className="font-epilogue font-semibold text-2xl text-white mt-6">
        Beneficiaries Stories
      </h1>
      <div className="grid grid-cols-3 gap-4 mt-6">
        {beneficiaries.map((beneficiary) => (
          <div key={beneficiary.beneficiary_id} className='sm:w-[288px] w-full rounded-[15px] bg-[#1c1c24] cursor-pointer  mb-[30px] ml-[20px]'>
            <h2 className="font-epilogue font-semibold text-lg text-gray-200">
              {beneficiary.beneficiary_name}
            </h2>
            <p className="text-gray-500">{beneficiary.story}</p>
          </div>
        ))}
      </div>

      <h1 className="font-epilogue font-semibold text-2xl text-white mt-12">
        Inventory sent to the beneficiaries
      </h1>
      <div className="grid grid-cols-3 gap-4 mt-6">
        {inventory.map((item) => (
          <div key={item.inventory_id} className="bg-white rounded-lg p-4 shadow-md">
            <h2 className="font-epilogue font-semibold text-lg text-gray-800">{item.item_name}</h2>
            <p className="text-gray-600">Quantity: {item.quantity}</p>
            <p className="text-gray-600">Date Sent: {item.date_sent}</p>
          </div>
        ))}
      </div>
    </div>

      {/* Modal */}
      {isModalOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-opacity-50 bg-gray-900">
          <div className="modal bg-white p-6 rounded-lg shadow-xl">
            <span
              className="close absolute top-0 right-0 mt-3 mr-3 text-gray-700 text-2xl cursor-pointer"
              onClick={() => setIsModalOpen(false)}
            >
              &times; x
            </span>
            <h2 className="text-2xl font-semibold mb-4 font-epilogue">Charity Application</h2>
            <div className="mb-4">
  <label htmlFor="imageURL" className="font-epilogue w-32">
    Image URL:
  </label>
  <input
    type="text"
    id="imageURL"
    value={imageURL}
    onChange={(e) => setImageURL(e.target.value)}
    className="ml-2 border border-gray-400 p-1 rounded"
  />
</div>
<div className="mb-4">
  <label htmlFor="charityName" className="font-epilogue w-32">
    Name of Charity:
  </label>
  <input
    type="text"
    id="charityName"
    value={charityName}
    onChange={(e) => setCharityName(e.target.value)}
    className="ml-2 border border-gray-400 p-1 rounded"
  />
</div>
<div className="mb-4">
  <label htmlFor="charityDescription" className="font-epilogue w-32">
    Description of Charity:
  </label>
  <textarea
    id="charityDescription"
    value={charityDescription}
    onChange={(e) => setCharityDescription(e.target.value)}
    className="ml-2 border border-gray-400 p-1 rounded"
  />
</div>


            <button
              onClick={handleSubmit}
              className="font-epilogue bg-blue-500 text-white py-2 px-4 rounded"
            >
              Submit
            </button>
            <button  
             onClick={() => setIsModalOpen(false)}
            className="bg-red-400 text-white px-4 py-2 mt-4 rounded-lg ml-4"
                >close</button>
          </div>
        </div>
      )}

    </div>
  );
};

export default CharityPage;
