import { useState, useEffect } from 'react';
import { projectStorage, projectFirestore, timestamp } from '../firebase/config';
import globalVariable from '../globalVariable';

const useStorage = (file) => {
  const [progress, setProgress] = useState(0);
  const [error, setError] = useState(null);
  const [url, setUrl] = useState(null);
  console.log("defg");
  useEffect(() => {
    // references
    console.log("useEffect", file);
    const storageRef = projectStorage.ref(file.name);
    const collectionRef = projectFirestore.collection('userDetails/'+globalVariable.email+'/children');
    
    storageRef.put(file).on('state_changed', (snap) => {
      let percentage = (snap.bytesTransferred / snap.totalBytes) * 100;
      setProgress(percentage);
    }, (err) => {
      setError(err);
    }, async () => {
        
      const url = await storageRef.getDownloadURL();
      console.log(url);
      const createdAt = timestamp();

      await collectionRef.add({ url, createdAt });
      setUrl(url);
    });
  }, [file]);

  return { progress, url, error };
}

export default useStorage;