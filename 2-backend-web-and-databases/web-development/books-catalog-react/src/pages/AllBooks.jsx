import React, { useEffect, useState } from 'react'
import { Book } from '../blocks/Book';
import axios from 'axios';

export const AllBooks = () => {
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
    <section id="all-books">
      <h2>All Books</h2>
      <p>This section contains all available books in the shop.</p>
      <div className="books">
        {books.map(book => {
          return <Book key={book.id} book={book} />
        })}
      </div>
    </section>
  )
}
