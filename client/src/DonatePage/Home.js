
import React, { useState } from 'react';

import { Charity, Navbar, Search } from '../components'





const Home = () => {
  const [charities, setCharities] = useState([]);



  const handleSearchResults = (results) => {
    setCharities(results);
  };


  return (
    <div>

{/* donor page is the home page */}
<Navbar />
      
      <Charity charities={charities} /> {/* Pass the charities list to the Charity component */}
    </div>
                
                
  
  )
}

export default Home