import React from 'react';
import { Container } from 'reactstrap';
import {
    useHistory,
    useLocation,
    withRouter
} from 'react-router-dom'

class ResultPage extends React.Component {
    constructor(props) {
        super(props);
        this.picture = {}
		let state = this.props.location.state || {from: {}}
        this.picture = state.data || {}
		console.log(state)
    }
    render() {
        
        return (
            <Container>Adiós</Container>
        );
    }
}

export default withRouter(ResultPage);