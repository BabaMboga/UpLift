import React, { useState } from 'react';
import axios from 'axios';

function DonationForm() {
  const [donationAmount, setDonationAmount] = useState('');
  const [isRecurring, setIsRecurring] = useState(false);
  const [startDate, setStartDate] = useState('');
  const [endDate, setEndDate] = useState('');

  const handleDonation = async () => {
    const donationData = {
      amount: donationAmount,
      isRecurring,
      startDate: isRecurring ? startDate : null,
      endDate: isRecurring ? endDate : null
    };

    try {
      const response = await axios.post('/api/donate', donationData);
      console.log(response.data.message);
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <div>
      <input
        type="number"
        placeholder="Donation Amount"
        value={donationAmount}
        onChange={(e) => setDonationAmount(e.target.value)}
      />
      <label>
        <input
          type="checkbox"
          checked={isRecurring}
          onChange={() => setIsRecurring(!isRecurring)}
        />
        Recurring Donation
      </label>
      {isRecurring && (
        <div>
          <input
            type="date"
            placeholder="Start Date"
            value={startDate}
            onChange={(e) => setStartDate(e.target.value)}
          />
          <input
            type="date"
            placeholder="End Date"
            value={endDate}
            onChange={(e) => setEndDate(e.target.value)}
          />
        </div>
      )}
      <button onClick={handleDonation}>Donate</button>
    </div>
  );
}

export default DonationForm;
