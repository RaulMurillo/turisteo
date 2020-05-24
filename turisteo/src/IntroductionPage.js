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

                <Col xs='0' sm='0' md='3' className="side_col_l"></Col>
                <Col xs='12' sm='12' md='6'>
                    <Container>
                        <Row className="img_logo">
                            <Image className="image_logo" src="images/full_turisteo.png" width="100%" height="auto" rounded />
                        </Row>
                        <div>
                            <p className="introduction_text" style={{ textAlign: "center" }}>
                                Turisteo is a proyect for the subject "Tecnologías Multimedia e Interacción" (TMI) from Master in Computer Engineering at Complutense University of Madrid, course 2019-2020.
					</p>
                            <p className="introduction_text" style={{ textAlign: "center" }}>
                                This application is able to recognize artistic and cultural monuments in a photograph and display tourist information about them, either in text or audio format.
					</p>
                        </div>
                        <Row>
                            <Col sm={{ size: 'auto', offset: 5 }} xs={{ size: 'auto', offset: 5 }}>
                                <Button onClick={this.handleButton}>Start</Button>
                            </Col>


                        </Row>
                    </Container>
                </Col>
                <Col xs='0' sm='0' md='3' className="side_col_r"></Col>

            </Row>
        )
    }



}
export default Prueba;
