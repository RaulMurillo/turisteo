import React from 'react'
import {
	HashRouter as Router,
	Switch,
	Route,
	Redirect
} from "react-router-dom"
import { Container, Row, Col } from 'reactstrap';
import ResultPage from './ResultPage';
import Image from 'react-bootstrap/Image';
import './style.css';
import ImageUploader from 'react-images-upload';
import ListGroup from 'react-bootstrap/ListGroup';

class App extends React.Component {
	constructor(props) {
        super(props);
         this.state = { pictures: [] };
         this.onDrop = this.onDrop.bind(this);
    }
 
    onDrop(picture) {
        this.setState({
            pictures: this.state.pictures.concat(picture)
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
						imgExtension={['.jpg', '.gif', '.png', '.gif']}
						maxFileSize={20971520}
					/>
				</Row>
				<Row className="justify-content-md-center">
					<Col className="text_lan" sm={4}>
					Select language:
					</Col>
					<Col sm={6}>
					<ListGroup as="ul" horizontal>
						<ListGroup.Item as="li" active>
							English
  </ListGroup.Item>
						<ListGroup.Item as="li">
							Spanish
						</ListGroup.Item>
						<ListGroup.Item as="li">
							Italian
  </ListGroup.Item>
						<ListGroup.Item as="li">
							French
						</ListGroup.Item>
						<ListGroup.Item as="li">
							German
						</ListGroup.Item>
					</ListGroup>
					</Col>
				</Row>
				<Router>
					<Switch>
						<Route path="/resultpage">
							<ResultPage />
						</Route>
					</Switch>
				</Router>
			</Container>

		);
	}
}

export default App;
