import React, { useState } from 'react';
import Title from './Title';
import ImageGrid from './ImageGrid';
import Modal from './Modal';
import { motion } from 'framer-motion';

const Cartoonify = () => {

    const [file, setFile] = useState(null);
    const [error, setError] = useState(null);
    const [docs, setDocs] = useState([]);
    const [selectedImg, setSelectedImg] = useState(null);
    const [loading, setLoading] = useState(false);

    const types = ['image/png', 'image/jpeg'];
    
    const cartoonifyAPI = "/image-cartoonify";

    const handleChange = (e) => {

        let selected = e.target.files[0];

        if (selected && types.includes(selected.type)) {
            setFile(selected);
            setError('');

            let formData = new FormData();
            formData.append('file', e.target.files[0]);
            formData.append('email', localStorage.getItem('email'));
            formData.append('token', localStorage.getItem('user-token'));

            const options = {
                method: 'POST',
                body: formData,
                // If you add this, upload won't work
                // headers: {
                //   'Content-Type': 'multipart/form-data',
                //
            }

            setLoading(true);

            const fetchImage = async () => {
                const res = await fetch(cartoonifyAPI, options);;
                const imageBlob = await res.blob();
                const imageObjectURL = URL.createObjectURL(imageBlob);
                //console.log(imageBlob);
                
                console.log(imageObjectURL);
                setFile(null);

                let document = []
                document.push({ "id" : 0, "url" : imageObjectURL});
                setDocs(document);
                setLoading(false);
              };

            fetchImage();
            

        } else {
            setFile(null);
            setError('Please select an image file (png or jpg)');
        }
    };

    return (
        <div className="App">
            <Title title="Upload a Image that you want to cartoonify"/>
            <form className='uploadImgForm'>
                <label className='uploadImgLabel'>
                    <input type="file" onChange={handleChange} />
                    <span>+</span>
                </label>
                
            </form>
            <div className="output">
                { error && <div className="error">{ error }</div>}
                { file && <div style = {{textAlign:"center"}}>{ file.name }</div> }
                
                {docs && <ImageGrid images = {docs} setSelectedImg={setSelectedImg} />}
                { selectedImg && (
				<Modal selectedImg={selectedImg} setSelectedImg={setSelectedImg} />
			    )}
            </div>
            {loading && <motion.div className="loader-container" initial={{ opacity: 0 }} animate={{ opacity: 3 }}>
                    <motion.div className="spinner"></motion.div>
            </motion.div>}
        </div>
      );
}

export default Cartoonify;