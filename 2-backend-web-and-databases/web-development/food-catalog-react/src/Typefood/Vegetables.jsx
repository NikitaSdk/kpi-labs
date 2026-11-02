import React, { useEffect, useState } from 'react';
import { Food } from '../blocks/Food';
import axios from 'axios';

export const Vegetables = () => {
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

  const vegetableItems = food.filter(item => item.type === 'Vegetables');

  return (
    <section id="Vegetables">
      <h2>Vegetables</h2>
      <p>Vegetables section.</p>
      <div className="food-container">
        {vegetableItems.map(item => (
          <Food key={item.id} food={item} />
        ))}
      </div>
    </section>
  );
};
