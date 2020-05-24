import React from 'react'
import {
	HashRouter as Router,
	Switch,
	Route,
} from "react-router-dom"
import ResultPage from './ResultPage';
import MainFunc from './MainFunc';
import MainPage from './MainPage';





class App extends React.Component {

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
