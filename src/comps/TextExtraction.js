import React, { useState } from 'react';
import Title from './Title';
import axios from 'axios';
import { motion } from 'framer-motion';

const TextExtraction = () => {

    const [file, setFile] = useState(null);
    const [error, setError] = useState(null);
    const [text, setText] = useState(null);

    const [loading, setLoading] = useState(false);

    const types = ['image/png', 'image/jpeg'];
    
    const textExtractionAPI = "/text-extraction";

    const handleChange = (e) => {

        let selected = e.target.files[0];

        if (selected && types.includes(selected.type)) {
            setFile(selected);
            setError('');

            let formData = new FormData();
            formData.append('file', e.target.files[0]);
            formData.append('email', localStorage.getItem('email'));
            formData.append('token', localStorage.getItem('user-token'));

            setLoading(true);

            axios.post(textExtractionAPI, formData)
            .then((response) => {

                if(response.status === 200){
                    const data = response.data['ocr_text'];
                    console.log(data);
                    setText(data);

                    setFile(null);
                    setLoading(false);
                }
            });

        } else {
            setFile(null);
            setError('Please select an image file (png or jpg)');
        }
    };

    return (  
            <div className='App'>
            
                <Title title="Upload a Image from which you want to extract a text"/>
                <form className='uploadImgForm'>
                    <label className='uploadImgLabel'>
                        <input type="file" onChange={handleChange} />
                        <span>+</span>
                    </label>
                </form>

                <div className="output">
                    {error && <div className="error">{ error }</div>}
                    {file && <div>{ file.name }</div> }
                    {text && <div style = {{textAlign:"center", marginTop:"40px"}}><h4><b>Extracted Text</b></h4>:</div>}
                    {text && <div style = {{textAlign:"center"}}><h4>{text}</h4></div>}

                </div>

                {loading && <motion.div className="loader-container" initial={{ opacity: 0 }} animate={{ opacity: 3 }}>
                    <motion.div className="spinner"></motion.div>
                </motion.div>}
            </div>
      );
}

export default TextExtraction;