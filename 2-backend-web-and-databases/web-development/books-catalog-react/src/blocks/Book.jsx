import React from 'react'

export const Book = ({ book }) => {
  const { title, description, author } = book;

  return (
    <div class="card">
      <h3>{title}</h3>
      <p>{description}</p>
      <quote>{author}</quote>
    </div>
  )
}
