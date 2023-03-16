import React, { useState } from 'react';
import Title from './Title';
import ImageGrid from './ImageGrid';
import Modal from './Modal';
import UploadForm from './UploadForm';

const Home = () => {

	const [selectedImg, setSelectedImg] = useState(null);

	return (
		<div className="App">
			<Title/>
			<UploadForm />
			<ImageGrid setSelectedImg={setSelectedImg} />
			{ selectedImg && (
				<Modal selectedImg={selectedImg} setSelectedImg={setSelectedImg} />
			)}
		</div>
	)
}

export default Home;