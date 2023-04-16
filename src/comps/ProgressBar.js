import React, { useEffect } from 'react';
import useStorage from '../hooks/useStorage';
import { motion } from 'framer-motion';
import axios from 'axios';

const ProgressBar = ({ file, setFile }) => {
  const { progress, url } = useStorage(file);
  const uploadAPI = '/store-encodings';
  // console.log("abcd");

  useEffect(() => {
    if (url) {
      setFile(null);

      axios.post(uploadAPI, {"email": localStorage.getItem('email'), "image_url": url, "user-token": localStorage.getItem('user-token')})
    }
  }, [url, setFile]);

  return (
    <motion.div className="progress-bar"
      initial={{ width: 0 }}
      animate={{ width: progress + '%' }}
    ></motion.div>
  );
} 

export default ProgressBar;