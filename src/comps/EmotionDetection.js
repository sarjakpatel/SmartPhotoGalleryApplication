import React, { useState } from 'react';
import Title from './Title';
import axios from 'axios';

const EmotionDetection = () => {

    const [file, setFile] = useState(null);
    const [error, setError] = useState(null);

    const types = ['image/png', 'image/jpeg'];
    
    const emotionDetectionAPI = "/emotion-detection";

    const handleChange = (e) => {

        let selected = e.target.files[0];

        if (selected && types.includes(selected.type)) {
            setFile(selected);
            setError('');

            let d = new FormData();
            d.append('file', e.target.files[0]);
            d.append('email', localStorage.getItem('email'))
            d.append('token', localStorage.getItem('user-token'))

            axios.post(emotionDetectionAPI, d)
            .then((response) => {

                if(response.status == 200){
                    const data = response.data;
                    console.log(data);
                    setFile(null);
                }
            });

        } else {
            setFile(null);
            setError('Please select an image file (png or jpg)');
        }
    };

    return (
        <div className="App">
            <Title title="Upload a Person's Image that you want to detect the emotion"/>
            <form>
            
                <label>
                    <input type="file" onChange={handleChange} />
                    <span>+</span>
                </label>
                
            </form>
            <div className="output">
                { error && <div className="error">{ error }</div>}
                { file && <div>{ file.name }</div> }

            </div>
        </div>
      );
}

export default EmotionDetection;