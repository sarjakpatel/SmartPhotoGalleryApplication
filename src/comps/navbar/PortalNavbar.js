import React from "react";
import { Button, Nav } from "react-bootstrap";
import Container from 'react-bootstrap/Container';
import Navbar from 'react-bootstrap/Navbar';
import { Link, useNavigate } from "react-router-dom";

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
                    <Nav className="me-auto">
                    <Link to="/" className="me-3 abc">Smart Photo Gallery Application</Link>
                    <Link to="/home" className="me-3 abc">Home</Link>
                    <Link to="/about" className="me-3 abc">About</Link>
                    <Link to="/pricing" className="me-3 abc">Price</Link>
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