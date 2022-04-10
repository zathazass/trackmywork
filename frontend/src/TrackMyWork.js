import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import './App.css';
import App from './App';
import Navbar from './components/inc/Navbar';
import Home from './components/pages/Home';
import About from './components/pages/About';

function TrackMyWork() {
	return (
		<div>
			<Router>
				<Navbar />
				<Routes>
					<Route exact path="/" element={<App />} />
					<Route path="/home" element={<Home />} />
					<Route path="/about" element={<About />} />
				</Routes>
			</Router>
		</div>
	);
}

export default TrackMyWork;
