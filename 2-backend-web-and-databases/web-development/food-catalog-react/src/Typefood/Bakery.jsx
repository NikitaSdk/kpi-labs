import React, { useEffect, useState } from 'react';
import { Food } from '../blocks/Food';
import axios from 'axios';

export const Bakery = () => {
  const [food, setFood] = useState([]);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get('http://localhost:3001/food');
        setFood(response.data);
      } catch (error) {
        console.error('Помилка отримання даних:', error);
      }
    };

    fetchData();
  }, []);

  const bakeryItems = food.filter(item => item.type === 'Bakery');

  return (
    <section id="Bakery">
      <h2>Bakery</h2>
      <p>Bakery section.</p>
      <div className="food-container">
        {bakeryItems.map(item => (
          <Food key={item.id} food={item} />
        ))}
      </div>
    </section>
  );
};
