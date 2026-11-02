import React from 'react';
import './Home.css'; 

export const Home = () => {
  return (
    <section id="Home">
      <h2>Welcome to the Food Market</h2>
      <p>Explore various types of food available.</p>
      <div className="images-container">
        <img src="images/seafood.jpg" alt="Seafood" className="home-image" />
        <img src="images/drinks.jpg" alt="Drinks" className="home-image" />
        <img src="images/fastfood.jpg" alt="Fast Food" className="home-image" />
      </div>
    </section>
  );
}
