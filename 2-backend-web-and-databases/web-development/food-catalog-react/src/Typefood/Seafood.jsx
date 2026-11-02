import React, { useEffect, useState } from 'react';
import { Food } from '../blocks/Food';
import axios from 'axios';

export const Seafood = () => {
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

  const seafoodItems = food.filter(item => item.type === 'Seafood');

  return (
    <section id="Seafood">
      <h2>Seafood</h2>
      <p>Seafood section.</p>
      <div className="food-container">
        {seafoodItems.map(item => (
          <Food key={item.id} food={item} />
        ))}
      </div>
    </section>
  );
};

