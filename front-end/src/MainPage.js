import React from 'react'
import { Container, Row, Col, Button } from 'reactstrap';
import Image from 'react-bootstrap/Image';
import './style.css';
import ImageUploader from 'react-images-upload';
import Select from 'react-select';
import {
    useHistory,
    useLocation,
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
            selectedOption: null
        };
    
        this.onDrop = this.onDrop.bind(this);
        this.handleChange = this.handleChange.bind(this);
        this.handleButton = this.handleButton.bind(this);
    }

    handleChange = selectedOption => {
        this.setState(
            { selectedOption }

        );
    };

    handleButton = selectedOption => {
        this.props.history.push({ pathname: '/resultpage', 'state': {
            'from': {'pathname': this.props.location.pathname },
            'data': this.state.picture
        }
        });
    };

    onDrop(picture) {
        this.setState({
            picture
        });
    }

    render() {
        return (
            <Container>
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

                </Row>
                <Row>
                    <Button variant="primary" size="lg" block onClick={this.handleButton}>
                        Submit
</Button>
                </Row>
                

            </Container>

        );
    }
}

export default withRouter(MainPage);