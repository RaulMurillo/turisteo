import React from 'react';
import { Container } from 'reactstrap';
import {
    withRouter
} from 'react-router-dom'

class ResultPage extends React.Component {
    constructor(props) {
        super(props);
		let state = this.props.location.state || {from: {}}
        this.picture = state.data.picture || {}
        this.language = state.data.language
		console.log(state)
    }
    render() {
        
        return (
            <Container>Adiós</Container>
        );
    }
}

export default withRouter(ResultPage);