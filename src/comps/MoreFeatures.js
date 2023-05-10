import * as React from 'react';
import Title from './Title';
import { styled } from '@mui/material/styles';
import Box from '@mui/material/Box';
import Paper from '@mui/material/Paper';
import Grid from '@mui/material/Grid';
import { Link } from "react-router-dom";

const MoreFeatures = () => {

    const Item = styled(Paper)(({ theme }) => ({
        // backgroundColor: theme.palette.mode === 'dark' ? '#1A2027' : '#fff',
        ...theme.typography.body2,
        // padding: theme.spacing(2),
        padding: "30px",
        margin: "30px",
        textAlign: 'center',
        color: theme.palette.text.secondary,
        fontFamily: "Noto Serif",
        textDecoration: "none",
        backgroundColor: '#fff',
        borderRadius:"10px",
        boxShadow: "0 10px 20px rgba(0,0,0,0.1)",
        boxSizing: "border-box"

      }));


    //   width: 850px;
    //   padding: 30px 35px 35px;
    //   background: #fff;
    //   border-radius: 10px;
    //   box-shadow: 0 10px 20px rgba(0,0,0,0.1);
    // box-sizing: border-box;
    

    return (
        <div className='App' >
            
            <Box sx={{ width: '100%' , margin: '50px'}}>

                <Title title="More Features"/>
               
                <Grid container rowSpacing={1} columnSpacing={{ xs: 1, sm: 2, md: 3 }}>
                    <Grid item xs={6}>
                    <Item><h5><Link to="/text-extraction" style = {{textDecoration:"none"}}>Extract Text</Link></h5></Item>
                    </Grid>
                    <Grid item xs={6}>
                    <Item><h5><Link to="/emotion-detection" style = {{textDecoration:"none"}}>Emotion Detection</Link></h5></Item>
                    </Grid>
                    <Grid item xs={6}>
                    <Item><h5><Link to="/remove-background" style = {{textDecoration:"none"}}>Remove Background</Link></h5></Item>
                    </Grid>
                    <Grid item xs={6}>
                    <Item><h5><Link to="/cartoonify" style = {{textDecoration:"none"}}>Cartoonify</Link></h5></Item>
                    </Grid>
                    <Grid item xs={6}>
                    <Item><h5><Link to="/deblur-image" style = {{textDecoration:"none"}}>Deblur Image</Link></h5></Item>
                    </Grid>
                    <Grid item xs={6}>
                    <Item><h5><Link to="/image-sketch" style = {{textDecoration:"none"}}>Image Sketch</Link></h5></Item>
                    </Grid>
                    <Grid item xs={6}>
                    <Item><h5><Link to="/generate-image" style = {{textDecoration:"none"}}>Generate Image</Link></h5></Item>
                    </Grid>
                    <Grid item xs={6}>
                    <Item><h5><Link to="/image-filter" style = {{textDecoration:"none"}}>Image Filter</Link></h5></Item>
                    </Grid>
                </Grid>
            </Box>
        </div>
      );
}

export default MoreFeatures;