
import React from 'react';

import { Charity, Navbar } from '../components'





const Home = () => {






  return (
    <div>

{/* donor page is the home page */}
<Navbar />
      
      <Charity  /> {/* Pass the charities list to the Charity component */}
    </div>
                
                
  
  )
}

export default Home