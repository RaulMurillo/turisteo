import React from 'react'
import {
	HashRouter as Router,
	Switch,
	Route,
	Redirect
} from "react-router-dom"
import ResultPage from './ResultPage';
import MainFunc from './MainFunc';




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
				</Switch>
			</Router>
		);
	}
}

export default App;
