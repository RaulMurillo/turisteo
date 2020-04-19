import React from 'react';
import { Container, Row } from 'reactstrap';
import Image from 'react-bootstrap/Image'
import {
    withRouter
} from 'react-router-dom'

class ResultPage extends React.Component {
    constructor(props) {
        super(props);
        this.picture = {}
        this.language = {}
		this.state = {
            imagen: undefined,
            text: undefined,
            title: undefined,
            image_rect: undefined,
            image_render: false,
            landmark: undefined

        }
        let prev = this.props.location.state || {from: {}}
        this.picture = prev.data.picture || {}
        this.language = prev.data.selectedOption
        this.filename = this.picture[0].name
        this.imag = null

       
    }


    componentWillMount() {
        //let state = this.props.location.state || {from: {}}
        const data = new FormData();
        data.append('file', this.picture[0]);
        data.append('language', this.language.value);
        //data.getAll('file')
        fetch('/save',  {
            method: 'POST',
            body: data,
          }).then(res => res.json()).then(data => {
            this.setState({title: data.title, image_rect: data.image_rect, image_render: true, landmark: data.landmark});
            fetch('/text/'+ this.state.landmark + '/' + this.language.value).then(res => res.json()).then(data => {
                this.setState({text: data.text});
                });
            console.log(this.state.text)
          }); 
       
           

        
       
        //this.setState({image_render: true, image_rect: 'alhambra-top_square.jpg'})
        /*fetch('/detect/'+ this.filename + '/' + this.language.value).then(res => res.json()).then(data => {
            this.setState({title: data.title, image_rect: data.image_rect, image_render: true});
          });   */     

        
     

    }

    
  


       


    render() {

        if(this.state.image_render){
            this.imag = <Image src= {require ('./instance/images/' + this.state.image_rect)} rounded/> 
            //this.setState({image_render: false})
            
        }
        
        return (
           
            <Container>
                <h1>{this.state.title}</h1>
                <Row>
                    {this.imag}
                </Row>
                <p>{this.state.text}</p>
                
            </Container>
            
        );
    }
}

export default withRouter(ResultPage);