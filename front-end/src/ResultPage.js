import React from 'react';
import fs from "fs";
import { Container, Row, Col } from 'reactstrap';

import Image from 'react-bootstrap/Image'
import {
    withRouter
} from 'react-router-dom'




class ResultPage extends React.Component {
    constructor(props) {
        super(props);
        this.picture = {}
        this.language = {}
        this.state = {
            text: undefined,

        }
        let prev = this.props.location.state || { from: {} }
        this.picture = prev.data.picture || {}
        this.language = prev.data.selectedOption
        this.filename = this.picture[0].name
        this.imag = null
        this.image_rect = prev.data.image_rect
        this.title = prev.data.title
        this.landmark = prev.data.landmark


    }


    componentWillMount() {
        if(this.landmark!=undefined){
            fetch('/text/' + this.landmark + '/' + this.language.value).then(res => res.json()).then(data => {
                this.setState({ text: data.text });
            });
        }
      
    }


    render() {

        /* if(this.state.image_render){
             this.imag = <Image src= {require ('./instance/images/' + this.state.image_rect)} style={ {width: 500, height: 500}} rounded/> 
             //this.setState({image_render: false})
             
         }*/
        if (this.image_rect != undefined) {
            return (

                <Container>
                    <h1>{this.title}</h1>
                    <Row>
                        <Col>

                            <Image src={require('./instance/images/' + this.image_rect)} style={{ width: 500, height: 500 }} rounded />
                        </Col>
                        <Col>
                            <p>{this.state.text}</p>
                        </Col>


                    </Row>


                </Container>

            );
        } else {
            return (

                <Container>
                    <h1>Error</h1>
                    <p>No se ha podido detectar la imagen</p>
                </Container>
            );
        }


    }
}

export default withRouter(ResultPage);