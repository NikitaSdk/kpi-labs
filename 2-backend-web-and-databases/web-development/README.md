# Web Development

Two single-page apps built with React and a mock REST API (`json-server` with `db.json`).

| App | What it is |
| --- | --- |
| [food-catalog-react](food-catalog-react) | Food catalog with categories: bakery, drinks, fast food, fruit, seafood, sweets, vegetables |
| [books-catalog-react](books-catalog-react) | Book catalog with genre pages: fantasy, fiction, poetry, romance, science fiction |

Run either app:

```bash
npm install
npx json-server --watch db.json --port 3001   # mock API
npm start
```
