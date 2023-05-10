import React, { useState } from 'react';
import {toast } from 'react-toastify';

const ImageFilter = () => {

    const [file, setFile] = useState(null);
    
    const [originalImage, setOriginalImage]  = useState(null);

    const types = ['image/png', 'image/jpeg'];
    
    const imageFilterAPI = "/image-filter";

    const [brightness, setBrightness] = useState(10);
    const [contrast, setContrast] = useState(10);
    const [hue, setHue] = useState(10);
    const [saturation, setSaturation] = useState(10);
    const [sharpen, setSharpen] = useState(10);
    const [vignette, setVignette] = useState(10);
    const [effect, setEffect] = useState(null);
    
    const changeBrightness = (event) => {
        setBrightness(event.target.value);
      };

    const changeSaturation = (event) => {
        setSaturation(event.target.value);
    };

    const changeContrast = (event) => {
        setContrast(event.target.value);
    };

    const changeHue = (event) => {
        setHue(event.target.value);
    };

    const changeVignette = (event) => {
        setVignette(event.target.value);
    };

    const changeSharpen = (event) => {
        setSharpen(event.target.value);
    };

    const changeEffect = (event) => {
        setEffect(event.target.value);
    };

    const resetFilter = () =>{
        
        if(originalImage){
            document.querySelector(".preview-img img").src = URL.createObjectURL(originalImage);
            setFile(originalImage);
        }
    }

    const applyFilter = () => {

        // let selected = e.target.files[0];
        console.log("File: ", file);
        
        if (file && types.includes(file.type)) {
           
            console.log("Applying Filters....");

            let formData = new FormData();
            formData.append('file', file);
            formData.append('email', localStorage.getItem('email'));
            formData.append('token', localStorage.getItem('user-token'));
            formData.append('brightness_control', brightness);
            formData.append('contrast_control', contrast);
            formData.append('saturation_control', saturation);
            formData.append('hue_control', hue);
            formData.append('vignette_control', vignette);
            formData.append('sharpen_control', sharpen);
            formData.append('effect_control', effect);


            const options = {
                method: 'POST',
                body: formData,
                // If you add this, upload won't work
                // headers: {
                //   'Content-Type': 'multipart/form-data',
                //
            }

            const fetchImage = async () => {
                const res = await fetch(imageFilterAPI, options);;
                const imageBlob = await res.blob();
                // setFile(imageBlob)
                const imageObjectURL = URL.createObjectURL(imageBlob);
                //console.log(imageBlob);
                
                console.log(imageObjectURL);
                document.querySelector(".preview-img img").src = imageObjectURL;
          
              };

            fetchImage();
        }
        else{
            toast.error('Please select an image file (png or jpg)', {
                position: "top-center",
                autoClose: 5000,
                hideProgressBar: true,
                closeOnClick: true,
                pauseOnHover: true,
                draggable: true,
                progress: undefined,
                theme: "colored",
                });
        }
    };

    const loadImage = (e) => {

        let selected = e.target.files[0];
        
        if(!selected) return;

        setFile(selected);
        setOriginalImage(selected);
        console.log("Setting File...");
        document.querySelector(".preview-img img").src = URL.createObjectURL(selected) ;
        document.querySelector(".filterContainer").classList.remove("disable");
        // previewImg.addEventListener("load", () => {
        //     resetFilterBtn.click();
        //     document.querySelector(".filterContainer").classList.remove("disable");
        // });
    }


    const download = async() => {
        
        const imageURL = document.querySelector(".preview-img img").src;
        const nameSplit=imageURL.split("/");
        const  duplicateName=nameSplit.pop();
        const link = document.createElement('a')
        link.href = imageURL;
        link.download = ""+duplicateName+"";
        document.body.appendChild(link)
        link.click()
        document.body.removeChild(link)  
    };

  
    return (
        
            // <Title title="Image Filtering"/>
            <div className = "filterBody">
                <div className="filterContainer disable">
                    <h2>Filters</h2>
                    <div className="filterWrapper">   
                        <div className="editor-panel">
                            <div className="filter">
                               
                                <div className="slider">
                                    <div className="filter-info">
                                        <p className="name">Brighteness</p>
                                        <p className="value">{brightness}</p>
                                    </div>
                                    <input type="range"  min={0} max={100} step={1} onChange={changeBrightness} value={brightness}/>
                                </div>
                                <div className="slider">
                                    <div className="filter-info">
                                        <p className="name">Saturation</p>
                                        <p className="value">{saturation}</p>
                                    </div>
                                    <input type="range"  min={0} max={100} step={1} onChange={changeSaturation} value={saturation} />
                                </div>
                                <div className="slider">
                                    <div className="filter-info">
                                        <p className="name">Contrast</p>
                                        <p className="value">{contrast}</p>
                                    </div>
                                    <input type="range"  min={0} max={100} step={1} onChange={changeContrast} value={contrast} />
                                </div>
                                <div className="slider">
                                    <div className="filter-info">
                                        <p className="name">Hue</p>
                                        <p className="value">{hue}</p>
                                    </div>
                                    <input type="range"  min={0} max={100} step={1} onChange={changeHue} value={hue} />
                                </div>
                                <div className="slider">
                                    <div className="filter-info">
                                        <p className="name">Vignette</p>
                                        <p className="value">{vignette}</p>
                                    </div>
                                    <input type="range"  min={0} max={100} step={1} onChange={changeVignette} value={vignette} />
                                </div>
                                <div className="slider">
                                    <div className="filter-info">
                                        <p className="name">Sharpen</p>
                                        <p className="value">{sharpen}</p>
                                    </div>
                                    <input type="range"  min={0} max={100} step={1} onChange={changeSharpen} value={sharpen} />
                                </div>
                                <div className="slider">
                                    <div className="filter-info">
                                        <p className="name">Effect</p>
                                    </div>
                                    <select value={effect} onChange={changeEffect}>
                                        <option value={null}>None</option>
                                        <option value="Cartoon">Cartoon</option>
                                        <option value="Edge">Edge</option>
                                        <option value="Vintage">Vintage</option>
                                        <option value="Blur">Blur</option>
                                        <option value="BlackWhite">Black & White</option>
                                        <option value="Monochrome">Monochrome</option>
                                    </select>
                                </div>
                            </div>
                        </div>
                        <div className="preview-img">
                            <img src="" alt="preview-img" />
                        </div>
                    </div>
                    <div className="filterControls">
                        
                        <div className="filterRow">
                            <input type="file" className="file-input" accept="image/*" hidden  onChange={loadImage}/>
                            <button className="choose-img" onClick={() => document.querySelector(".file-input").click()}>Choose Image</button>
                            <button className="apply-filter" onClick={applyFilter}>Apply Filters</button>
                            <button className="reset-filter" onClick={resetFilter}>Reset Filters</button>
                        
                            <button className="save-img" onClick={download}>Download Image</button>
                        </div>
                    </div>
                </div>
            </div>
      );
}

export default ImageFilter;