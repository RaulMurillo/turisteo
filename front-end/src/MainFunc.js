import React from 'react'
import {
	useHistory,
	useLocation,
	withRouter
} from 'react-router-dom'

import MainPage from './MainPage'


function MainFunc() {

	let history = useHistory();
	let location = useLocation();

	let { from } = location.state || { from: { pathname: "/" } };

	return (
		
		<MainPage from={from} history={history} />
						
	);
}

export default withRouter(MainFunc);