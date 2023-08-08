import React, { useState } from 'react';
import { search } from '../assets';

const Search = ({ charities, onSearchResults }) => {
  const [searchQuery, setSearchQuery] = useState('');

  const handleSearch = () => {
    const filteredCharities = charities.filter(charity =>
      charity.name.toLowerCase().includes(searchQuery.toLowerCase())
    );

    onSearchResults(filteredCharities);
  };

  return (
    <div className="lg:flex-1 flex flex-row max-w-[458px] py-2 pl-4 pr-2 h-[52px] bg-[#1c1c24] rounded-[100px] mt-4 mb-4">
      <input
        type="text"
        placeholder="Search for charities"
        className="flex w-full font-epilogue font-normal text-[14px] placeholder:text-[#696f82] text-white bg-transparent outline-none"
        value={searchQuery}
        onChange={e => setSearchQuery(e.target.value)}
      />
        
      <div
        className="w-[72px] h-full rounded-[20px] bg-[#4acd8d] flex justify-center items-center cursor-pointer"
        onClick={handleSearch}
      >
        <img src={search} alt="search" className="w-[15px] h-[15px] object-contain"/>
      </div>
    </div>
  );
};

export default Search;
