import React from 'react';
import { Container, Row, Col } from 'reactstrap';
import Image from 'react-bootstrap/Image'
import {
    withRouter
} from 'react-router-dom'

class ResultPage extends React.Component {
    constructor(props) {
        super(props);
        this.picture = {}
        this.language = {}
        console.log(this.props);
		this.state = {
            imagen: undefined,
            text: this.props.location.data.text,
            title: this.props.location.data.title

        }
        /*let prev = this.props.location.state || {from: {}}
        this.picture = prev.data.picture || {}
        this.language = prev.data.selectedOption
        this.filename = this.picture[0].name*/

       
    }


    componentDidMount() {
        //let state = this.props.location.state || {from: {}}
        /*const data = new FormData();
        data.append('file', this.picture[0]);
        data.getAll('file')
        fetch('/save',  {
            method: 'POST',
            body: data,
          });
        fetch('/detect/'+ this.filename + '/' + this.language.value).then(res => res.json()).then(data => {
            this.setState({text: data.text, title: data.title});
          });*/
        


        
     

    }

    
  


       


    render() {
        
        return (
            <Container>
                <h1>{this.state.title}</h1>
                <Row>
                    <Col xs={6} md={4}>
                        <Image src="/images/alhambra-top_square.jpg" rounded />
                    </Col>
                </Row>
                
                <p>{this.state.text}</p>
                
            </Container>
            
        );
    }
}

export default withRouter(ResultPage);