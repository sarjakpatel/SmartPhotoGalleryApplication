import React, { useState } from 'react';
import Title from './Title';
import ImageGrid from './ImageGrid';
import Modal from './Modal';
import UploadForm from './UploadForm';
import useFirestore from '../hooks/useFirestore';

const Home = () => {

	const [selectedImg, setSelectedImg] = useState(null);

	const { docs } = useFirestore('userDetails/'+localStorage.getItem('email') + '/children');


	return (
		<div className="App">
			<Title title="Your Pictures"/>
			<UploadForm />
			<ImageGrid images = {docs} setSelectedImg={setSelectedImg} />
			{ selectedImg && (
				<Modal selectedImg={selectedImg} setSelectedImg={setSelectedImg} />
			)}
		</div>
	)
}

export default Home;