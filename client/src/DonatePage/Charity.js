import React, { useState, useEffect } from 'react';
import Modal from 'react-modal';

// Modal.setAppElement('#root');

function Charity() {
  const [charities, setCharities] = useState([]);
  const [selectedCharity, setSelectedCharity] = useState(null);
  const [modalIsOpen, setModalIsOpen] = useState(false); // Add this state variable



  const [donationAmount, setDonationAmount] = useState('');
  const [donationFrequency, setDonationFrequency] = useState('one-time');
  const [anonymousDonor, setAnonymousDonor] = useState(false);
  const [setReminder, setSetReminder] = useState(false);
  const [paymentOption, setPaymentOption] = useState('');



  useEffect(() => {
    // Fetch the JSON data using the fetch function
    fetch('http://localhost:5000/charities')
      .then((response) => response.json())
      .then((data) => setCharities(data)) // Assuming the API returns an array of charities directly
      .catch((error) => console.error('Error fetching data:', error));
  }, []);


  const handleDonateClick = (charity) => {
    setSelectedCharity(charity);
    setModalIsOpen(true);
  };

  const closeModal = () => {
    setModalIsOpen(false);
  };

  const handleDonation = () => {
    // Perform actions based on the donationAmount, donationFrequency, anonymousDonor, setReminder, and paymentOption
    // You can implement your payment processing logic here

    // Reset the form after donation
    setDonationAmount('');
    setDonationFrequency('one-time');
    setAnonymousDonor(false);
    setSetReminder(false);
    setPaymentOption('');

    // Close the modal
    closeModal();
  };

  return (
   <div className='text-white'>
    <h1 className='font-epilogue font-semibold text-[28px] text-white text-left mt-6'>All Charities ({charities.length})
    </h1>

    <div className='flex flex-wrap mt-[20px] gap-[260x]'>
    {charities.map((charity) => (
      <div className='sm:w-[288px] w-full rounded-[15px] bg-[#1c1c24] cursor-pointer  mb-[30px] ml-[20px]'>
         <img src={charity.logo} className='w-full h-[158px] object-cover rounded-[15px]'/>
         <div className='flex flex-col p-4'>
          <div className='flex flex-row items-center mb-[18px]'>
<h1 className=''>Total Donation</h1>
<p className='ml-[12px] mt-[6px] font-epilogue font-medium text-[18px] text-white'>${charity.total_amount_donated}</p>
         </div>
         <div className='block'>
          <h3 className='font-epilogue font-semibold text-[19px] text-left leading-[26px] '>{charity.name}</h3>
          <ul className='mt-4'>
              {charity.testimonials.map((testimonial, index) => (
                <li key={index}>
                  <strong className='text-[#808191] '>{testimonial.author}</strong>:
                   <p className='mt-[px] font-epilogue font-normal  text-[#808191] text-left leading-[18px] truncate'>
                    {testimonial.testimonial}</p>
                </li>
              ))}
            </ul>
         </div>

         <div
          onClick={() => handleDonateClick(charity)}
         className="inline-block rounded-[20px] shadow-md bg-green-600 hover:bg-blue-600 focus:bg-blue-700 px-3 py-1 text-white font-medium mt-4 transition-colors duration-300 ease-in-out">
  Donate
  </div>
         </div>
      </div> ))}



      <Modal
  isOpen={modalIsOpen}
  onRequestClose={closeModal}
  contentLabel="Donate Modal"
  className="modal w-[500px]"
  overlayClassName="modal-overlay fixed inset-0 flex justify-center items-center bg-black bg-opacity-60"
>
  {/* Modal Content */}
  {selectedCharity && (
  <div className="modal-content bg-white rounded-lg shadow-md p-4">
    <div className="modal-header flex justify-between items-center mb-4">
      <h2 className="text-xl font-semibold">
        Donate to {selectedCharity?.name}
      </h2>

      <button
        onClick={closeModal}
        className="text-gray-500 hover:text-gray-900 focus:outline-none"
      >
        Close
      </button>
    </div>
    <div className="modal-body">
      {/* Donation Form */}
      <form>
        <label className="block mb-2">Donation Amount:</label>
        <input
          type="number"
          value={donationAmount}
          onChange={(e) => setDonationAmount(e.target.value)}
          className="border border-gray-400 p-2 rounded mb-4"
          placeholder="Enter the amount you want to donate"
        />

        <label className="block mb-2">Donation Frequency:</label>
        <select
          value={donationFrequency}
          onChange={(e) => setDonationFrequency(e.target.value)}
          className="border border-gray-400 p-2 rounded mb-4"
        >
          <option value="one-time">One-time</option>
          <option value="monthly">Monthly</option>
          <option value="yearly">Yearly</option>
        </select>

        <label className="block mb-2">
          <input
            type="checkbox"
            checked={anonymousDonor}
            onChange={() => setAnonymousDonor(!anonymousDonor)}
            className="mr-2"
          />
          Anonymous Donor
        </label>

        <label className="block mb-2">
          <input
            type="checkbox"
            checked={setReminder}
            onChange={() => setSetReminder(!setReminder)}
            className="mr-2"
          />
          Set a Reminder
        </label>

        {/* Payment Options */}
        <h3 className="font-semibold mt-4">Payment Options:</h3>
        {/* Add your payment options elements here */}
        {/* For example, radio buttons or a select dropdown */}
        {/* Replace the placeholder options with your actual payment options */}

        <select
          value={paymentOption}
          onChange={(e) => setPaymentOption(e.target.value)}
          className="border border-gray-400 p-2 rounded mb-4"
        >
          <option value="" disabled>
            Choose Payment Option
          </option>
          <option value="credit-card">Credit Card</option>
          <option value="paypal">PayPal</option>
          <option value="bitcoin">Bitcoin</option>
        </select>

        <button
          type="button"
          onClick={handleDonation}
          className="bg-blue-600 text-white font-semibold px-4 py-2 rounded mt-4"
        >
          Donate Now
        </button>
      </form>
      <div className='text-black'>
        <h1>{selectedCharity.testimonial}</h1>
      </div>
    </div>
  </div>
  )}
</Modal>

    </div>


   




   </div>
  );
}

export default Charity;
