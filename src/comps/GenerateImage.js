import React, { useState } from 'react';
import Title from './Title';
import ImageGrid from './ImageGrid';
import Modal from './Modal';
import { motion } from 'framer-motion';

import { Button, Form, FormGroup} from "react-bootstrap";

const GenerateImage = () => {
    
    const [docs, setDocs] = useState([]);
    const [selectedImg, setSelectedImg] = useState(null);
    const [loading, setLoading] = useState(false);
    
    const generateImageAPI = "/generate-image";

    const generateImageForm = (event) => {

        event.preventDefault();
        const formElement = document.querySelector('#generateImageForm');
        const formData = new FormData(formElement);
      
        const btnPointer = document.querySelector('#generate-btn');
        btnPointer.innerHTML = 'Please wait..';
        btnPointer.setAttribute('disabled', true);


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
            
            const res = await fetch(generateImageAPI, options);;
            const imageBlob = await res.blob();
            const imageObjectURL = URL.createObjectURL(imageBlob);
            //console.log(imageBlob);
            
            console.log(imageObjectURL);

            let document = []
            document.push({ "id" : 0, "url" : imageObjectURL});
            setDocs(document);
            btnPointer.innerHTML = 'Generate Image';
            btnPointer.removeAttribute('disabled');
          };

        fetchImage();
        setLoading(false);
    };

    return (
        <div className="App">
            <Title title="Generate Image from a Text"/>

            <Form id="generateImageForm" onSubmit={generateImageForm}>
                
                <FormGroup className="mb-3">
                        <label>Enter a Text: </label>
                        <input type={'text'} className="form-control" name="text" required />
                </FormGroup>
                <Button type="submit" className="btn-success mt-2" id="generate-btn">Generate Image</Button>
            </Form>


            <div className="output">
                
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

export default GenerateImage;