import React, { useEffect, useState } from 'react';
import { Food } from '../blocks/Food';
import axios from 'axios';

export const Fruit = () => {
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

  const fruitItems = food.filter(item => item.type === 'Fruit');

  return (
    <section id="Fruit">
      <h2>Fruit</h2>
      <p>Fruit section.</p>
      <div className="food-container">
        {fruitItems.map(item => (
          <Food key={item.id} food={item} />
        ))}
      </div>
    </section>
  );
};
