import React from "react";
import { Button, Nav } from "react-bootstrap";
import Container from 'react-bootstrap/Container';
import Navbar from 'react-bootstrap/Navbar';
import { useNavigate } from "react-router-dom";

const PortalNavbar = () => {

    const navigate = useNavigate();

    const logout = () => {
        localStorage.clear();
        navigate('/auth/login');
    }

    return (
        <React.Fragment>
            <Navbar bg="dark" expand="lg" className="navbar-dark">
                <Container>
                    <Navbar.Brand>Smart Photo Gallery Application</Navbar.Brand>
                    
                    <Nav className="me-auto">
                    <Nav.Link href="home">Home</Nav.Link>
                    <Nav.Link href="about">About</Nav.Link>
                    <Nav.Link href="#pricing">Pricing</Nav.Link>
                    </Nav>
                    
                    <Navbar.Toggle aria-controls="basic-navbar-nav" />
                    <Navbar.Collapse id="basic-navbar-nav">
                        <Nav className="ms-auto">
                            <Nav.Link>
                                <Button className="btn-warning" onClick={logout}>Logout</Button>
                            </Nav.Link>
                        </Nav>
                    </Navbar.Collapse>
                </Container>
            </Navbar>
        </React.Fragment>
    );
}

export default PortalNavbar;