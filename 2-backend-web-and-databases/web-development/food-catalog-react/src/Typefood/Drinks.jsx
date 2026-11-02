import React, { useEffect, useState } from 'react';
import { Food } from '../blocks/Food';
import axios from 'axios';

export const Drinks = () => {
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

  const drinksItems = food.filter(item => item.type === 'Drinks');

  return (
    <section id="Drinks">
      <h2>Drinks</h2>
      <p>Drinks section.</p>
      <div className="food-container">
        {drinksItems.map(item => (
          <Food key={item.id} food={item} />
        ))}
      </div>
    </section>
  );
};
