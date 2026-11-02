import React from 'react';
import { Link } from 'react-router-dom';

export const Header = () => {
  return (
    <header>
      <nav>
        <ul>
          <li><Link to="/">Home</Link></li>
          <li><Link to="/Seafood">Sea food</Link></li>
          <li><Link to="/Fast-food">Fast food</Link></li>
          <li><Link to="/Vegetables">Vegetables</Link></li>
          <li><Link to="/Fruit">Fruit</Link></li>
          <li><Link to="/Drinks">Drinks</Link></li>
          <li><Link to="/Sweets">Sweets</Link></li>
          <li><Link to="/Bakery">Bakery</Link></li>
        </ul>
      </nav>
    </header>
  );
};
