import React from 'react';
import fs from "fs";
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
        this.state = {
            //imagen: undefined,
            text: undefined,
            title: undefined,
            image: undefined
            //title: undefined,
            //image_rect: undefined,
            //image_render: false,
            //landmark: undefined

        }
        let prev = this.props.location.state || { from: {} }
        this.picture = prev.data.picture || {}
        this.language = prev.data.selectedOption
        this.filename = this.picture[0].name
        this.imag = null
        this.image_rect = prev.data.image_rect
        this.title = prev.data.title
        this.landmark = prev.data.landmark


    }


    componentWillMount() {
        //let state = this.props.location.state || {from: {}}
        /*const data = new FormData();
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
          }); */

        // var fs = require("fs"); // Or `import fs from "fs";` with ESM
        // console.log(fs);


        //if require('./instance/images/' + this.image_rect) ==
        this.setState({ image: require('./instance/images/' + this.image_rect) })
        // fs.stat('./instance/images/' + this.image_rect, function(err) {
        //     if (!err) {
        //         console.log('file or directory exists');
        //     }
        //     else if (err.code === 'ENOENT') {
        //         console.log('file or directory does not exist');
        //     }
        // });
        // if (fs.existsSync('./instance/images/' + this.image_rect)) {
        //     this.setState({ image: require('./instance/images/' + this.image_rect) })
        // }
        fetch('/text/' + this.landmark + '/' + this.language.value).then(res => res.json()).then(data => {
            this.setState({ text: data.text });
        });




        //this.setState({image_render: true, image_rect: 'alhambra-top_square.jpg'})
        /*fetch('/detect/'+ this.filename + '/' + this.language.value).then(res => res.json()).then(data => {
            this.setState({title: data.title, image_rect: data.image_rect, image_render: true});
          });   */




    }








    render() {

        /* if(this.state.image_render){
             this.imag = <Image src= {require ('./instance/images/' + this.state.image_rect)} style={ {width: 500, height: 500}} rounded/> 
             //this.setState({image_render: false})
             
         }*/
        if (this.state.image != undefined) {
            return (

                <Container>
                    <h1>{this.title}</h1>
                    <Row>
                        <Col>

                            <Image src={require('./instance/images/' + this.image_rect)} style={{ width: 500, height: 500 }} rounded />
                        </Col>
                        <Col>
                            <p>{this.state.text}</p>
                        </Col>


                    </Row>


                </Container>

            );
        } else {
            return (

                <Container>
                    <h1>Error</h1>
                </Container>
            );
        }


    }
}

export default withRouter(ResultPage);