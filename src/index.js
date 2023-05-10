import React from 'react';
import ReactDOM from 'react-dom/client';
import 'bootstrap/dist/css/bootstrap.min.css';
import './index.css';
import reportWebVitals from './reportWebVitals';
import { BrowserRouter, Route, Routes } from 'react-router-dom';
import Login from './auth/login/Login';
import Auth from './auth/Auth';
import App from './App';
import ProtectedRoute from './util/ProtectedRoute';
import SignUp from './auth/login/SignUp';
import { ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import Home from './comps/Home';
import SearchImage from './comps/SearchImage';
import TextExtraction from './comps/TextExtraction';
import EmotionDetection from './comps/EmotionDetection';
import Classify from './comps/Classify';
import MoreFeatures from './comps/MoreFeatures';
import RemoveBackground from './comps/RemoveBackground';
import Cartoonify from './comps/Cartoonify';
import DeblurImage from './comps/DeblurImage';
import ImageSketch from './comps/ImageSketch';
import GenerateImage from './comps/GenerateImage';
import ImageFilter from './comps/ImageFilter';

const root = ReactDOM.createRoot(document.getElementById('root'));

root.render(
		<BrowserRouter basename={'/'}>
			<Routes>
				<Route path='/auth' element={<Auth />}>
					<Route path='login' element={<Login />} />
					<Route path='signup' element={<SignUp />} />
				</Route>
				
				<Route path="/" element={<App />}>
					<Route path='' element={
						<ProtectedRoute>
							<Home />
						</ProtectedRoute>
					} />
					<Route path='classify' element={
						<ProtectedRoute>
							<Classify />
						</ProtectedRoute>
					} />
					<Route path='search' element={
						<ProtectedRoute>
							<SearchImage />
						</ProtectedRoute>
					} />
					<Route path='emotion-detection' element={
						<ProtectedRoute>
							<EmotionDetection />
						</ProtectedRoute>
					} />
					<Route path='text-extraction' element={
						<ProtectedRoute>
							<TextExtraction />
						</ProtectedRoute>
					} />

					<Route path='more-features' element={
						<ProtectedRoute>
							<MoreFeatures />
						</ProtectedRoute>
					} />

					<Route path='remove-background' element={
						<ProtectedRoute>
							<RemoveBackground />
						</ProtectedRoute>
					} />

					<Route path='cartoonify' element={
						<ProtectedRoute>
							<Cartoonify />
						</ProtectedRoute>
					} />
					
					<Route path='deblur-image' element={
						<ProtectedRoute>
							<DeblurImage />
						</ProtectedRoute>
					} />

					<Route path='image-sketch' element={
						<ProtectedRoute>
							<ImageSketch />
						</ProtectedRoute>
					} />

					<Route path='generate-image' element={
						<ProtectedRoute>
							<GenerateImage />
						</ProtectedRoute>
					} />

					<Route path='image-filter' element={
						<ProtectedRoute>
							<ImageFilter />
						</ProtectedRoute>
					} />

				</Route>
			</Routes>
			<ToastContainer
				position="top-center"
				autoClose={5000}
				hideProgressBar
				newestOnTop={false}
				closeOnClick
				rtl={false}
				pauseOnFocusLoss
				draggable
				pauseOnHover
				theme="colored"
				/>
		</BrowserRouter>
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
