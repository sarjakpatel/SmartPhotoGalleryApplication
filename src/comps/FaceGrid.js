import React from 'react';
import { motion } from 'framer-motion';

const FaceGrid = ({images, setSelectedFaceIndex}) => {
  
  const docs = images;


  return (
    <div className="img-grid">
      
      {docs && docs.map(doc => (
        <motion.div className="img-wrap" key={doc.id} 
          layout
          whileHover={{ opacity: 1 }}s
          onClick={() => setSelectedFaceIndex(doc.id)}
        >
          <motion.img src={doc.url} alt="uploaded pic"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 1 }}
          />
        </motion.div>
      ))
      }
    </div>
  )
}

export default FaceGrid;