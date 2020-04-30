import React from 'react';

import { Container, Row, Col, TextArea } from 'reactstrap';

import Image from 'react-bootstrap/Image'
import {
    withRouter
} from 'react-router-dom'
import { Map, GoogleApiWrapper, Marker, Listing, Text, View } from 'google-maps-react';
import ReactAudioPlayer from 'react-audio-player';





class ResultPage extends React.Component {
    constructor(props) {
        super(props);
        this.picture = {}
        this.language = {}
        this.state = {
            text: undefined,
            places: []

        }
        let prev = this.props.location.state || { from: {} }
        this.picture = prev.data.picture || {}
        this.language = prev.data.selectedOption
        this.filename = this.picture[0].name
        this.imag = null
        this.image_rect = prev.data.image_rect
        this.title = prev.data.title
        this.landmark = prev.data.landmark
        this.latitud = prev.data.latitud
        this.longitud = prev.data.longitud
        this.fetchPlaces = this.fetchPlaces.bind(this);
        this.crearMarcador = this.crearMarcador.bind(this)
        // this.initMap = this.initMap.bind(this);
        // this.crearMarcador = this.crearMarcador.bind(this);




    }



    componentWillMount() {
        //fetch('pruebaCeca.html').then(data => data.text()).then(html=> document.getElementById('elementID').innerHTML = html);
        if (this.landmark != undefined) {
            fetch('/text/' + this.landmark + '/' + this.language.value).then(res => res.json()).then(data => {
                this.setState({ text: data.text });
            });

        }
        console.log(this.image_rect)


    }
    // callback(results, status, infowindow) {
    //     if (status == google.maps.places.PlacesServiceStatus.OK) {
    //         for (var i = 0; i < results.length; i++) {
    //             //var place = results[i];
    //             this.crearMarcador(results[i]);
    //         }
    //     }
    // }

    // initMap() {
    //     // Creamos un mapa con las coordenadas actuales

    //     var latLng = new google.maps.LatLng(this.latitud, this.longitud);

    //     var mapOptions = {
    //         center: latLng,
    //         zoom: 16,
    //         mapTypeId: google.maps.MapTypeId.SATELLITE
    //     };

    //     var map = new google.maps.Map(document.getElementById("map"), mapOptions);

    //     // Creamos el infowindow
    //     var infowindow = new google.maps.InfoWindow();

    //     // Especificamos la localización, el radio y el tipo de lugares que queremos obtener
    //     var request = {
    //         location: latLng,
    //         radius: 5000,
    //         //openNow: true, si los queremos abiertos ahora
    //         types: ['cafe', 'health']
    //     };

    //     // Creamos el servicio PlaceService y enviamos la petición.
    //     var service = new google.maps.places.PlacesService(map);

    //     service.nearbySearch(request, this.callback());
    // }


    // crearMarcador(place, infowindow, map) { //var image =dir 
    //     // Creamos un marcador
    //     var marker = new google.maps.Marker({
    //         map: map,
    //         animation: google.maps.Animation.DROP,
    //         position: place.geometry.location
    //         //icon:image para cambiar el icono
    //     });

    //     // Asignamos el evento click del marcador
    //     google.maps.event.addListener(marker, 'click', function () {
    //         infowindow.setContent(place.name + JSON.stringify(place.plus_code) + "" + place.rating + " " + JSON.stringify(place.formatted_phone_number));
    //         //infowindow.setContent("hola");
    //         infowindow.open(map, this);
    //     });
    // }
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

        // Asignamos el evento click del marcador
        // google.maps.event.addListener(marker, 'click', function() {
        //   infowindow.setContent(place.name + JSON.stringify(place.plus_code)+"" + place.rating+" " + JSON.stringify(place.formatted_phone_number));
        //   //infowindow.setContent("hola");
        //   infowindow.open(map, this);
        // });
    }


    render() {

        /* if(this.state.image_render){
             this.imag = <Image src= {require ('./instance/images/' + this.state.image_rect)} style={ {width: 500, height: 500}} rounded/> 
             //this.setState({image_render: false})
             
         }*/
        const mapStyles = {
            width: '500px',
            height: '500px',

        };
        if (this.image_rect != undefined) {

            return (

                <Container>
                    <h1>{this.title}</h1>
                    <Row>
                        <Col>
                            <Image src={require('./instance/images/' + this.image_rect)} style={{ width: 500, height: 500 }} rounded />
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
                            <ReactAudioPlayer
                                src="my_audio_file.ogg"
                                autoPlay
                                controls
                            />


                        </Col>


                    </Row>

                    {/*<div id='elementID'></div>*/}
                    {/* <Container>
                        <Map
                            googleMapURL= "http:://maps.googleapis.com/maps/api/js?v=3.exp&key=AIzaSyC-hTIvFx317AdIgrB9NewMDbU1WhSB4rY"
                            loadingElement= {<p>Cargando</p>}
                        />
                    </Container> */}
                    {/* <div style={{ height: '100vh', width: '100%' }}>
                        <GoogleMapReact
                            bootstrapURLKeys={{ key: 'AIzaSyC-hTIvFx317AdIgrB9NewMDbU1WhSB4rY'}}
                            defaultCenter={{lat:59.95, lng:30.33}}
                            defaultZoom={11}
                        >
                            <AnyReactComponent
                                lat={59.955413}
                                lng={30.337844}
                                text="My Marker"
                            />
                        </GoogleMapReact>
                    </div> */}




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