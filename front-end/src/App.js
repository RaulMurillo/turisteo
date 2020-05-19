import React from 'react'
import {
	HashRouter as Router,
	Switch,
	Route,
	withRouter,
	Redirect
} from "react-router-dom"
import ResultPage from './ResultPage';
import MainFunc from './MainFunc';
import MainPage from './MainPage';
import IntroductionPage from './IntroductionPage';
import { Container, Row, Button } from 'reactstrap'
import Image from 'react-bootstrap/Image'




class App extends React.Component {
	// constructor(props) {
	// 	super(props);

	// 	this.state = {
	// 		redirect: false,
	// 	}
	// 	this.handleButton = this.handleButton.bind(this);


	// }

	// handleButton = selectedOption => {

	// 	this.setState({ redirect: true });

	// };
	// renderRedirect = () => {
	// 	if (this.state.redirect) {
	// 		return <Redirect to='/mainpage' />
	// 	} else {
	// 		return (

	// 			<Container style={{ width: '900px' }}>
	// 				<Row className="img_logo">
	// 					<Image className="image_logo" src="images/full_turisteo.png" rounded />
	// 				</Row>
	// 				<div>
	// 					<p style={{ textAlign: "center" }}>
	// 						Turisteo is a proyect for the subject "Tecnologías Multimedia e Interacción" (TMI) from Master in Computer Engineering at Complutense University of Madrid, course 2019-2020.
	// 				</p>
	// 					<p style={{ textAlign: "center" }}>
	// 						It consists of an App capable of recognizing artistic and cultural monuments and generating information of tourist interest in this regard.
	// 				</p>
	// 				</div>
	// 				<Row className="justify-content-md-center" xs lg="6">

	// 					<Button onClick={this.handleButton}>Start</Button>

	// 				</Row>

	// 			</Container>
	// 		)

	// 	}
	// }

	render() {


		return (

			<Router>
				{/* {this.renderRedirect()} */}
				{/* <Redirect to='/prueba' /> */}
				
				
				<Switch>
					
					<Route exact path="/">
						<MainFunc />
					</Route>
					<Route push path="/mainpage">
						<MainPage />
					</Route>
					<Route path="/resultpage">
						<ResultPage />
					</Route>
				</Switch>
			</Router>
		);
	}
}

export default App;
