import React from 'react'
import { Container, Row, Col, Button,Alert  } from 'reactstrap';
import Image from 'react-bootstrap/Image';
import './style.css';
import ImageUploader from 'react-images-upload';
import Select from 'react-select';
import Form from 'react-bootstrap/Form'
import {

    withRouter
} from 'react-router-dom'

const options = [
	{ value: 'ar', label: 'Arabic' }, { value: 'en', label: 'English' }, { value: 'es', label: 'Spanish' }

];

class MainPage extends React.Component {

    constructor(props) {
        super(props);
        
        this.state = {
            picture: null,
            selectedOption: null,
            errorAlert: false,
            audio: false
        };
        
    
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
        this.state.audio = audio.checked;
        if(this.state.picture != null && this.state.selectedOption != null){
            this.props.history.push({ pathname: '/resultpage', 'state': {
                'from': {'pathname': this.props.location.pathname },
                'data': this.state

            }
            });
        }else{
            this.setState({errorAlert:true})
        }
        
        
    };
    

    onDrop(picture) {
        this.setState({
            picture
        });
    }

    onDismiss = selectedOption =>{
        this.setState({errorAlert:false});
    }

    render() {
        return (
            <Container>
                 <Alert color="danger" isOpen={this.state.errorAlert} toggle={this.onDismiss}>
                                   Introduce una imágen y un idioma
                </Alert>
                <Row className="justify-content-md-center">

                    <Col md="auto">
                        <Image className="logo" src="images/logo_turisteo.png" roundedCircle />
                    </Col>

                </Row>
                <Row>
                    <ImageUploader
                        withIcon={true}
                        singleImage={true}
                        withPreview={true}
                        buttonText='Upload image'
                        onChange={this.onDrop}
                        label="max size 20MB"
                        withIcon={true}
                        imgExtension={['.jpg', '.gif', '.png', '.gif']}
                        maxFileSize={20971520}
                    />
                </Row>
                <Row className="justify-content-md-center" xs lg="6">

                    <Col>
                        <Select className="lang"

                            value={this.selectedOption}
                            onChange={this.handleChange}
                            options={options}
                            placeholder="Select language"
                        />


                    </Col>
                    <Col>
                        <Form.Group controlId="formBasicCheckbox" >
                            <Form.Check type="checkbox" className="audio" ref="audio" label="Audio" />
                            
                        </Form.Group>
                    </Col>

                </Row>
                <Row className="justify-content-md-center" xs lg="6">

                    <Button variant="primary" size="lg" block onClick={this.handleButton}>Submit</Button>
   
                </Row>
                

            </Container>

        );
    }
}

export default withRouter(MainPage);