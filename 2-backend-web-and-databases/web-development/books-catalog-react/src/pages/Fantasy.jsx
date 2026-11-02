import React, { useEffect, useState } from 'react'
import { Book } from '../blocks/Book'
import axios from 'axios';

export const Fantasy = () => {
  const [books, setBooks] = useState([]);

  useEffect(() => {
    axios.get('http://localhost:3001/books')
    .then(response => {
      setBooks(response.data);
    })
    .catch(error => {
      console.error('Помилка отримання даних з API:', error);
    });
  }, []);

  return (
    <section id="fantasy">
      <h2>Fantasy</h2>
      <p>This section contains a collection of fantasy books.</p>
      <div className="books">
        {books.filter(book => book.type === 'Fantasy').map(book => {
          return <Book key={book.id} book={book} />
        })}
      </div>
    </section>
  )
}
