import { HashRouter as Router, Routes, Route } from 'react-router-dom';
import { Seafood } from './Typefood/Seafood';
import { FastFood } from './Typefood/Fastfood';
import { Vegetables } from './Typefood/Vegetables';
import { Fruit } from './Typefood/Fruit';
import { Drinks } from './Typefood/Drinks';
import { Sweets } from './Typefood/Sweets';
import { Bakery } from './Typefood/Bakery';
import { Home } from './blocks/Home'; // Імпорт компоненту Home з папки blocks
import './App.css';
import { Header } from './blocks/Header';

export const App = () => {
  return (
    <Router>
      <Header />
      <main>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/Seafood" element={<Seafood />} />
          <Route path="/Fast-food" element={<FastFood />} />
          <Route path="/Vegetables" element={<Vegetables />} />
          <Route path="/Fruit" element={<Fruit />} />
          <Route path="/Drinks" element={<Drinks />} />
          <Route path="/Sweets" element={<Sweets />} />
          <Route path="/Bakery" element={<Bakery />} />
        </Routes>
      </main>
    </Router>
  );
}
