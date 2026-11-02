import React, { useEffect, useState } from 'react'
import { Book } from '../blocks/Book';
import axios from 'axios';

export const Fiction = () => {
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
    <section id="fiction">
      <h2>Fiction</h2>
      <p>This section contains a collection of fiction books.</p>
      <div className="books">
        {books.filter(book => book.type === 'Fiction').map(book => {
          return <Book key={book.id} book={book} />
        })}
      </div>
    </section>
  )
}
