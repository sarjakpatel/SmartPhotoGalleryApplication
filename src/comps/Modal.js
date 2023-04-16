import React from 'react';
import { motion } from 'framer-motion';

const Modal = ({ setSelectedImg, selectedImg }) => {

  const handleClick = (e) => {
    if (e.target.classList.contains('backdrop')) {
      setSelectedImg(null);
    }
  }

  const download = async() => {
    const originalImage= selectedImg;
    const image = await fetch(originalImage);
   
    //Split image name
    const nameSplit=originalImage.split("/");
    const  duplicateName=nameSplit.pop();
   
    const imageBlog = await image.blob()
    const imageURL = URL.createObjectURL(imageBlog)
    const link = document.createElement('a')
    link.href = imageURL;
    link.download = ""+duplicateName+"";
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)  
   };




  return (
    <motion.div className="backdrop" onClick={handleClick}
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
    >
      <motion.img src={selectedImg} alt="enlarged pic" 
        initial={{ y: "-100vh" }}
        animate={{ y: 0 }}
      />
      <div style = {
        {display:"flex", flexDirection: "row",
          margin: 'auto',
          justifyContent: "center",
          alignContent: "center"}}>
        <button className="btn btn-primary" onClick = {download} style = {{width:"200px"}}>Download</button>
        </div>
      
    </motion.div>
  )
}

export default Modal;