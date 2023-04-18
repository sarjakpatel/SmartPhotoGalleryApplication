import React, { useState } from 'react';
import { useEffect } from 'react';
import { Button } from 'react-bootstrap';
import { projectStorage, projectFirestore, timestamp } from '../firebase/config';
import FaceGrid from './FaceGrid';
import ImageGrid from './ImageGrid';
import Modal from './Modal';

const Classify = () => {

    const [docs, setDocs] = useState([]);
    const [selectedFaceIndex, setSelectedFaceIndex] = useState(null);
    const [image, setImage] = useState(null);
    const [selectedImg, setSelectedImg] = useState(null);

    useEffect(() => {
        
        console.log("Getting cropped picures from firebase");

        projectFirestore.collection('userDetails/'+localStorage.getItem('email') + '/data').doc('cropped_face_url').get()
        .then((snapshot) => {
         
            const data = snapshot.data();
            // console.log(data);
            let document = [];
      
            Object.keys(data).forEach( function(key){

                document.push({ "id" : key, "url" : data[key]});
            })
            setDocs(document);
          })
        
      }, []);

      
    useEffect(() => {
        
        if(selectedFaceIndex !== undefined){
            console.log("Getting cropped picures from firebase");

            projectFirestore.collection('userDetails/'+localStorage.getItem('email') + '/data').doc('image_urls').get()
            .then((snapshot) => {
                // console.log(snapshot.data()[selectedFaceIndex]);
                const data = snapshot.data()[selectedFaceIndex];

                var document = data.map((e, index) => ({'id': index, "url": e}));
                setImage(document);
              })
            }
      }, [selectedFaceIndex]);


    return (
        <div className="App">
            {docs && !image && <FaceGrid images = {docs} setSelectedFaceIndex= {setSelectedFaceIndex}/>}
            {image && <Button type="submit" className="btn-primary mt-2" id="login-btn" onClick={() => setImage(null)}>Back</Button>}

            {image && <ImageGrid images = {image} setSelectedImg={setSelectedImg} />}
			{ selectedImg && (
				<Modal selectedImg={selectedImg} setSelectedImg={setSelectedImg} />
			)}
        </div>
      );
}

export default Classify;