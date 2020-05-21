import React from 'react'
import { Container, Row, Button, Col } from 'reactstrap'
import Image from 'react-bootstrap/Image'




class Prueba extends React.Component {

    constructor(props) {
        super(props);

        this.handleButton = this.handleButton.bind(this);


    }

    handleButton = selectedOption => {

        this.props.history.push({
            pathname: '/mainpage', 'state': {
                'from': { 'pathname': this.props.from.pathname },

            }
        });


    };



    render() {

        return (
            <Row>

                <Col xs='3' className="side_col_l"></Col>
                <Col xs='6'>
                    <Container>
                        <Row className="img_logo">
                            <Image className="image_logo" src="images/full_turisteo.png" width="100%" height="auto" rounded />
                        </Row>
                        <div>
                            <p className="introduction_text" style={{ textAlign: "center" }}>
                                Turisteo is a proyect for the subject "Tecnologías Multimedia e Interacción" (TMI) from Master in Computer Engineering at Complutense University of Madrid, course 2019-2020.
					</p>
                            <p className="introduction_text" style={{ textAlign: "center" }}>
                                It consists of an App capable of recognizing artistic and cultural monuments and generating information of tourist interest in this regard.
					</p>
                        </div>
                        <Row className="justify-content-md-center" xs lg="6">

                            <Button onClick={this.handleButton}>Start</Button>

                        </Row>
                    </Container>
                </Col>
                <Col xs='3' className="side_col_r"></Col>

            </Row>
        )
    }



}
export default Prueba;