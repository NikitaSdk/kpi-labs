import { HashRouter as Router, Routes, Route } from 'react-router-dom';
import { Poetry } from './pages/Poetry';
import { Header } from './blocks/Header';
import { Fiction } from './pages/Fiction';
import { Romance } from './pages/Romance';
import { Fantasy } from './pages/Fantasy';
import { AllBooks } from './pages/AllBooks';
import { ScienceFiction } from './pages/ScienceFiction';
import './App.css'

export const App = () => {
  return (
    <Router>
      <Header />
      <Routes>
        <Route path="/" element={<AllBooks />} />
        <Route path="/fiction" element={<Fiction />} />
        <Route path="/poetry" element={<Poetry />} />
        <Route path="/romance" element={<Romance />} />
        <Route path="/fantasy" element={<Fantasy />} />
        <Route path="/science-fiction" element={<ScienceFiction />} />
      </Routes>
    </Router>
  )
}
