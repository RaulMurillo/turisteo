"use strict"
import React from 'react';

import { Container, Row, Col } from 'reactstrap';

import Image from 'react-bootstrap/Image'
import {
    withRouter
} from 'react-router-dom'
import { Map, GoogleApiWrapper, Marker, Listing, Text, View } from 'google-maps-react';
import ReactAudioPlayer from 'react-audio-player';
//import fs from 'fs'



class ResultPage extends React.Component {
    constructor(props) {
        super(props);
        // let obj = {
        //     filename: this.props.location.state.data.picture[0].name,
        //     language: this.props.location.state.data.selectedOption,
        //     image_rect: this.props.location.state.data.image_rect,
        //     title: this.props.location.state.data.title,
        //     landmark: this.props.location.state.data.landmark,
        //     latitud: this.props.location.state.data.latitud,
        //     longitud: this.props.location.state.data.longitud
        // };
        
        // let fs = require('fs'),
        //     jsonData = JSON.stringify(obj);
        
        // fs.writeFile("./props.json", jsonData, err => {
        //     if (err) {
        //         console.log('Error writing file', err)
        //     } else {
        //         console.log('Successfully wrote file')
        //     }
        // })
        
   
        this.state = {
            text: undefined,
            places: [],
            audio: undefined,
            // filename: this.props.location.state.data.picture[0].name || {},
            // language: this.props.location.state.data.selectedOption || {},
            // image_rect: this.props.location.state.data.image_rect || {},
            // title: this.props.location.state.data.title || {},
            // landmark: this.props.location.state.data.landmark || {},
            // latitud: this.props.location.state.data.latitud || {},
            // longitud: this.props.location.state.data.longitud || {}

        }
        if(typeof this.props.location.state !== 'undefined'){
            localStorage.setItem('filename', this.props.location.state.data.picture[0].name);
            localStorage.setItem('language', this.props.location.state.data.selectedOption.value);
            localStorage.setItem('image_rect', this.props.location.state.data.image_rect);
            localStorage.setItem('title', this.props.location.state.data.title);
            localStorage.setItem('landmark', this.props.location.state.data.landmark);
            localStorage.setItem('latitud', this.props.location.state.data.latitud);
            localStorage.setItem('longitud', this.props.location.state.data.longitud);
            localStorage.setItem('audio_check', this.props.location.state.data.audio);
        }
        this.filename = localStorage.getItem('filename')
        this.language = localStorage.getItem('language')
        this.image_rect = localStorage.getItem('image_rect')
        this.title = localStorage.getItem('title')
        this.landmark = localStorage.getItem('landmark')
        this.latitud = localStorage.getItem('latitud')
        this.longitud = localStorage.getItem('longitud')
        this.audio_check = localStorage.getItem('audio_check')
        //this.text = localStorage.getItem('text')
    

        
        
        this.fetchPlaces = this.fetchPlaces.bind(this);
        this.crearMarcador = this.crearMarcador.bind(this)
        this.audio = null
        // this.initMap = this.initMap.bind(this);
        // this.crearMarcador = this.crearMarcador.bind(this);




    }



    componentDidMount() {
        //fetch('pruebaCeca.html').then(data => data.text()).then(html=> document.getElementById('elementID').innerHTML = html);
        if(typeof this.props.location.state !== 'undefined'){
            if (this.landmark != undefined) {
                fetch('/text/' + this.landmark + '/' + this.language).then(res => res.json()).then(data => {
                    this.setState({ text: data.text });
                    localStorage.setItem('text', data.text);
                    console.log(localStorage.getItem('text'));
                   // this.text = this.state.text
                   console.log(this.audio_check)
                    if(this.audio_check === 'true'){
                        console.log(this.audio_check)
                        fetch('/speech/' + this.state.text + '/' + this.language).then(res => res.json()).then(data => {
                            localStorage.setItem('audio', data.audio);
                            this.setState({ audio: data.audio });
                            
                        });
                    }
                    
                });
    
            }
        }else{
            this.setState({text: localStorage.getItem('text')});
            this.setState({audio: localStorage.getItem('audio')});

        }
        


    }
  
    fetchPlaces(mapProps, map) {
        const { google } = mapProps;
        const service = new google.maps.places.PlacesService(map);
        var latLng = new google.maps.LatLng(this.latitud, this.longitud);
        var request = {
            location: latLng,
            radius: 5000,
            //openNow: true, si los queremos abiertos ahora
            types: ['cafe', 'health']
        };
        service.nearbySearch(request, (results, status) => {
            if (status === google.maps.places.PlacesServiceStatus.OK) {
                for (var i = 0; i < results.length; i++) {
                    //var place = results[i];
                    this.crearMarcador(results[i], mapProps, map);
                }
            }


        });

    }
    crearMarcador(place, mapProps, map) { //var image =dir 
        // Creamos un marcador
        const { google } = mapProps;
        var infowindow = new google.maps.InfoWindow();
        var marker = new google.maps.Marker({
            map: map,
            animation: google.maps.Animation.DROP,
            position: place.geometry.location,
            icon: "http://maps.google.com/mapfiles/ms/icons/red-dot.png",

            //icon:image para cambiar el icono
        });
        google.maps.event.addListener(marker, 'click', function () {
            infowindow.setContent(place.name + JSON.stringify(place.plus_code) + "" + place.rating + " " + JSON.stringify(place.formatted_phone_number));
            //infowindow.setContent("hola");
            infowindow.open(map, this);
        });

    }


    render() {

        const mapStyles = {
            width: '500px',
            height: '500px',

        };
        if (this.image_rect !== 'undefined') {
            console.log(this.image_rect)
            if (this.state.audio !== undefined) {
                this.audio = <ReactAudioPlayer
                    src={require('./instance/audios/' + this.state.audio)}
                    autoPlay
                    controls
                    currentTime
                />
            }

            return (

                <Container>
                    <h1>{this.title}</h1>
                    <Row>
                        <Col>
                            <Image className="image" src={require('./instance/images/' + this.image_rect)} style={{ width: 500, height: 350 }} rounded />
                            <Map
                                google={this.props.google}
                                zoom={15}
                                onReady={this.fetchPlaces}
                                style={mapStyles}
                                initialCenter={{ lat: this.latitud, lng: this.longitud }}
                            >
                                <Marker position={{ lat: this.latitud, lng: this.longitud }} icon={"http://maps.google.com/mapfiles/ms/icons/blue-dot.png"} />

                            </Map>
                        </Col>
                        <Col>
                            {/* <MDBContainer>
                                <div className="scrollbar scrollbar-primary  mt-5 mx-auto" style={{ width: "300px", maxHeight: "50px" }}>
                                    <p>{this.state.text}</p>
                                </div>

                            </MDBContainer> */}
                            <Container className="scroll_text">
                                {this.state.text}
                            </Container>
                            {this.audio}
                        </Col>
                    </Row>
                </Container>

            );
        } else {
            return (

                <Container>
                    <h1>Error</h1>
                    <p>No se ha podido detectar la imagen</p>
                </Container>
            );
        }


    }
}

export default GoogleApiWrapper({
    apiKey: 'AIzaSyC-hTIvFx317AdIgrB9NewMDbU1WhSB4rY',

})(withRouter(ResultPage));
//export default withRouter(ResultPage);