import React, { useState } from 'react';
import axios from 'axios';

function ReminderEmailButton() {
  const [email, setEmail] = useState('');
  const [loading, setLoading] = useState(false);
  const [responseMessage, setResponseMessage] = useState('');

  const handleSendReminder = async () => {
    setLoading(true);
    setResponseMessage('');

    try {
      const response = await axios.post('/send-reminder-email', { email });
      setResponseMessage(response.data.message);
    } catch (error) {
      setResponseMessage('Failed to send reminder email.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <h2>Send Reminder Email</h2>
      <input
        type="email"
        placeholder="Recipient Email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
      />
      <button onClick={handleSendReminder} disabled={loading}>
        {loading ? 'Sending...' : 'Send Reminder Email'}
      </button>
      {responseMessage && <p>{responseMessage}</p>}
    </div>
  );
}

export default ReminderEmailButton;
