import axios from "axios";
import React from "react";
import {Button, Col, Container, Form, FormGroup, FormLabel, Row } from "react-bootstrap";
import {Link, useNavigate } from "react-router-dom";
import {toast } from 'react-toastify';
import { projectFirestore } from "../../firebase/config";
import { doc, setDoc } from "firebase/firestore"; 

const SignUp = () => {

    const signUpAPI = '/signup';
    const navigate = useNavigate();

    const submitSignUpForm = (event) => {
        
        event.preventDefault();
        
        const formElement = document.querySelector('#signUpForm');
        const formData = new FormData(formElement);
        const formDataJSON = Object.fromEntries(formData);
        const btnPointer = document.querySelector('#signup-btn');
        btnPointer.innerHTML = 'Please wait..';
        btnPointer.setAttribute('disabled', true);
        
        axios.post(signUpAPI, formDataJSON)
        .then((response) => {
            
            btnPointer.innerHTML = 'Register';
            btnPointer.removeAttribute('disabled');
            const data = response.data;
            const token = data.idToken;
            
            if (!token) {
               
                toast.error('Unable to create a User, Please try again after some time!!', {
                    position: "top-center",
                    autoClose: 5000,
                    hideProgressBar: true,
                    closeOnClick: true,
                    pauseOnHover: true,
                    draggable: true,
                    progress: undefined,
                    theme: "colored",
                    });
                return;
            }
            
            setTimeout(async () => {

                toast.success('Please verify your email!!',{
                    position: "top-center",
                    autoClose: 5000,
                    hideProgressBar: true,
                    closeOnClick: true,
                    pauseOnHover: true,
                    draggable: true,
                    progress: undefined,
                    theme: "colored",
                });

                await setDoc(doc(projectFirestore, "userDetails", formDataJSON.email), {
                    "email": formDataJSON.email, 
                    "firstName": formDataJSON.firstName,
                    "lastName": formDataJSON.lastName  
                });

                navigate('/auth/login');
            
            }, 500);

        }).catch((error) => {
            btnPointer.innerHTML = 'Register';
            btnPointer.removeAttribute('disabled');
            
            if(error.response.status == 400){

                toast.info('User Already Exists!!', {
                    position: "top-center",
                    autoClose: 5000,
                    hideProgressBar: true,
                    closeOnClick: true,
                    pauseOnHover: true,
                    draggable: true,
                    progress: undefined,
                    theme: "colored",
                    });
                return;
            }
            else{
                toast.error('Error Creating in User', {
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
        });
    }

    return (
        <React.Fragment>
            <Container className="my-5">
                <h2 className="fw-normal mb-5">Register</h2>
                <Row>
                    <Col md={{span: 6}}>
                        <Form id="signUpForm" onSubmit={submitSignUpForm}>
                            <FormGroup className="mb-3">
                                <FormLabel htmlFor={'signup-firstName'}>First Name:</FormLabel>
                                <input type={'text'} className="form-control" id={'signup-firstName'} name="firstName" required />
                            </FormGroup>
                            <FormGroup className="mb-3">
                                <FormLabel htmlFor={'signup-lastName'}>Last Name:</FormLabel>
                                <input type={'text'} className="form-control" id={'signup-lastName'} name="lastName" required />
                            </FormGroup>
                            <FormGroup className="mb-3">
                                <FormLabel htmlFor={'signup-username'}>Email</FormLabel>
                                <input type={'text'} className="form-control" id={'signup-username'} name="email" required />
                            </FormGroup>
                            <FormGroup className="mb-3">
                                <FormLabel htmlFor={'signup-password'}>Password</FormLabel>
                                <input type={'password'} className="form-control" id={'signup-password'} name="password" required />
                            </FormGroup>
                            <Button type="submit" className="btn-success mt-2" id="signup-btn">Register</Button>
                        </Form>
                        <Link to="/auth/login">Login</Link>
                    </Col>
                </Row>
            </Container>
        </React.Fragment>
    );
}

export default SignUp;