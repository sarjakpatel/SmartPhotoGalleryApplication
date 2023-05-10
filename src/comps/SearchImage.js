import React, { useEffect, useState } from 'react';
import Title from './Title';
import axios from 'axios';
import ImageGrid from './ImageGrid';
import Modal from './Modal';
import { motion } from 'framer-motion';

const SearchImage = () => {

	const [selectedImg, setSelectedImg] = useState(null);
    const [docs, setDocs] = useState([]);

    const [file, setFile] = useState(null);
    const [error, setError] = useState(null);

    const [loading, setLoading] = useState(false);

    const types = ['image/png', 'image/jpeg'];
    
    const searchAPI = "/image-search";

    useEffect(() =>{

    }, []);

    const handleChange = (e) => {

        let selected = e.target.files[0];

        if (selected && types.includes(selected.type)) {
            
            setFile(selected);
            setError('');

            let formData = new FormData();
            formData.append('file', e.target.files[0]);
            formData.append('email', localStorage.getItem('email'))
            formData.append('token', localStorage.getItem('user-token'))

            setLoading(true);

            axios.post(searchAPI, formData)
            .then((response) => {

                if(response.status === 200){
                    const data = response.data;

                    // console.log(data['list of similar images']);

                    let temp = []
                    var i = 0;
                    data['list of similar images'].map(d=>{

                        d.map(e=>{
                            // console.log("Image Link: " +e);
                            temp.push({"id" : i, "url" : e});
                            i++;
                        })   
                    })
                    // console.log(temp);
                    setDocs(temp);
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
        <div className="App">
            <Title title="Upload a Person's Image that you want to Search"/>
            <form className='uploadImgForm'>
                <label className='uploadImgLabel'>
                    <input type="file" onChange={handleChange} />
                    <span>+</span>
                </label>
            </form>
            <div className="output">
                { error && <div className="error">{ error }</div>}
                { file && <div>{ file.name }</div> }
            </div>
            {/* { file && <ProgressBar key= "1" file={file} setFile={setFile} /> } */}

            {docs && <ImageGrid images = {docs} setSelectedImg={setSelectedImg} />}

            { selectedImg && (
				<Modal selectedImg={selectedImg} setSelectedImg={setSelectedImg} />
			)}

            {loading && <motion.div className="loader-container" initial={{ opacity: 0 }} animate={{ opacity: 3 }}>
                    <motion.div className="spinner"></motion.div>
                </motion.div>}
        </div>
      );
}

export default SearchImage;