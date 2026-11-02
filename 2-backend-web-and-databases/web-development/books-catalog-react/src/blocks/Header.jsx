import React from 'react';
import { Link } from 'react-router-dom';

export const Header = () => {
  return (
    <header>
      <nav>
        <ul>
          <li><Link to="/">All Books</Link></li>
          <li><Link to="/poetry">Poetry</Link></li>
          <li><Link to="/fiction">Fiction</Link></li>
          <li><Link to="/science-fiction">Science Fiction</Link></li>
          <li><Link to="/romance">Romance</Link></li>
          <li><Link to="/fantasy">Fantasy</Link></li>
        </ul>
      </nav>
    </header>
  );
};
