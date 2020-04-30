import React from 'react'
import {
	HashRouter as Router,
	Switch,
	Route,
	Redirect
} from "react-router-dom"
import ResultPage from './ResultPage';
import MainFunc from './MainFunc';
import Map from './Map'
import MapP from './MapP'



class App extends React.Component {
	render() {
		return (
			<Router>
				<Switch>
					<Route path="/mainpage">
						<MainFunc />
					</Route>
					<Route path="/resultpage">
						<ResultPage />
					</Route>
					<Route path="/Map">
						<Map />
					</Route>
					<Route path="/MapP">
						<MapP />
					</Route>
				</Switch>
			</Router>
		);
	}
}

export default App;
