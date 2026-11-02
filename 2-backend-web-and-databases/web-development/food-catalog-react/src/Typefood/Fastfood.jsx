import React, { useEffect, useState } from 'react';
import { Food } from '../blocks/Food';
import axios from 'axios';

export const FastFood = () => {
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

  const fastFoodItems = food.filter(item => item.type === 'Fast food');

  return (
    <section id="FastFood">
      <h2>Fast Food</h2>
      <p>Fast food section.</p>
      <div className="food-container">
        {fastFoodItems.map(item => (
          <Food key={item.id} food={item} />
        ))}
      </div>
    </section>
  );
};
