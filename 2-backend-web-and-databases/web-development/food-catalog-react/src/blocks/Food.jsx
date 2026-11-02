import React from 'react';
export const Food = ({ food }) => {
  const { name, weight, price } = food;
  return (
    <div className="card">
      <div className="food-name">{name}</div>
      <div className="food-details">
        <span>Weight: {weight} g </span>
        <span>Price: {price} uah</span>
      </div>
    </div>
  );
}
