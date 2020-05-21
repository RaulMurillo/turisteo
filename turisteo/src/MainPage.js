import React from 'react'
import { Container, Row, Col, Button, Alert } from 'reactstrap';
import Image from 'react-bootstrap/Image';
import './style.css';
import ImageUploader from 'react-images-upload';
import Select from 'react-select';
import Form from 'react-bootstrap/Form'
import {

    withRouter
} from 'react-router-dom'

const options = [
    { value: 'de', label: <div><img src={"images/german.png"} height="30px" width="30px"/>German</div> }, { value: 'en', label: <div><img src={"images/english.png"} height="30px" width="30px"/>English</div> }, { value: 'es', label: <div><img src={"images/spanish.png"} height="30px" width="30px"/>Spanish</div> },
    { value: 'fr', label: <div><img src={"images/french.png"} height="30px" width="30px"/>French</div> }, { value: 'it', label: <div><img src={"images/italian.png"} height="30px" width="30px"/>Italian</div> }, { value: 'pt', label: <div><img src={"images/portuguese.png"} height="30px" width="30px"/>Portuguese</div> }

];

class MainPage extends React.Component {

    constructor(props) {
        super(props);


        this.state = {
            picture: null,
            selectedOption: null,
            errorAlert: false,
            audio: false,
            title: undefined,
            image_rect: undefined,
            landmark: undefined,
            latitud: undefined,
            longitud: undefined,
            butonAct: false
        };
        localStorage.removeItem('text')
        localStorage.removeItem("audio")

        this.onDrop = this.onDrop.bind(this);
        this.handleChange = this.handleChange.bind(this);
        this.handleButton = this.handleButton.bind(this);
        this.onDismiss = this.onDismiss.bind(this);
    }



    handleChange = selectedOption => {
        this.setState(
            { selectedOption }

        );
    };

    handleButton = selectedOption => {
        let {
            audio
        } = this.refs
        // this.state.audio = audio.checked;
        this.setState({ audio: audio.checked });
        if (this.state.picture !== null && this.state.selectedOption !== null) {
            if (this.state.landmark !== undefined) {
                fetch('/title/' + this.state.landmark + '/' + this.state.selectedOption.value).then(res => res.json()).then(data => {
                    this.setState({ title: data.title });
                    this.props.history.push({
                        pathname: '/resultpage', 'state': {
                            'from': { 'pathname': this.props.location.pathname },
                            'data': this.state

                        }
                    });
                });
            } else {
                this.props.history.push({
                    pathname: '/resultpage', 'state': {
                        'from': { 'pathname': this.props.location.pathname },
                        'data': this.state

                    }
                });
            }



        } else {
            this.setState({ errorAlert: true })
        }


    };


    onDrop(picture) {
        if (picture.length !== 0) {
            this.setState({ picture });
            const data = new FormData();
            data.append('file', picture[0]);
            fetch('/detect', {
                method: 'POST',
                body: data,
            }).then(res => res.json()).then(data => {
                this.setState({ image_rect: data.image_rect, landmark: data.landmark, latitud: data.latitud, longitud: data.longitud });

            }).catch(error => { this.setState({ butonAct: true }) });
        } else {
            this.setState({ picture: undefined, image_rect: undefined });
        }

    }

    onDismiss = selectedOption => {
        this.setState({ errorAlert: false });
    }

    render() {
        return (
            <Row>
                <Col xs='0' sm='0' md='3' className="side_col_l"></Col>
                <Col xs='12' sm='12' md='6'>
                    <Container>

                    

                        <Row className="img_logo">
                            <Image className="image_logo" src="images/full_turisteo.png" width="100%" height="auto" rounded />
                        </Row>

                        <Alert color="danger" isOpen={this.state.errorAlert} toggle={this.onDismiss}>
                                Please, select a language
                            </Alert>
                        <Row>
                            <ImageUploader
                                withIcon={true}
                                singleImage={true}
                                withPreview={true}
                                buttonText='Upload image'
                                onChange={this.onDrop}
                                label= {<div><p><b>Max. size 20MB</b> [.jpg, .jpeg, .png]</p></div>}
                                
                                imgExtension={['.jpeg', '.jpg', '.png']}
                                maxFileSize={20971520}
                            />
                        </Row>
                        <Row>

                            <Button disabled={this.state.image_rect === undefined && this.state.butonAct === false} variant="primary" block onClick={this.handleButton}>Submit</Button>
                        
                        </Row>

                        <Row className="row_language">

                            <Col lg={{ offset: 3 }} md={{ offset: 1 }} sm={{ offset: 4 }} xs={{ offset: 4 }}>
                                <Select className="lang"

                                    value={this.selectedOption}
                                    onChange={this.handleChange}
                                    options={options}
                                    placeholder="Language"
                                />


                            </Col>
                            <Col lg ={{ offset: 1 }} md={{ offset: 2 }} sm={{ offset: 5 }} xs={{ offset: 5 }}>
                                <Form.Group controlId="formBasicCheckbox" >
                                    <Form.Check type="checkbox" className="audio" ref="audio" label="Audio" />
                                </Form.Group>
                            </Col>

                        </Row>



                    </Container>

                </Col>
                <Col xs='0' sm='0' md='3' className="side_col_r"></Col>
            </Row>


        );
    }
}

export default withRouter(MainPage);