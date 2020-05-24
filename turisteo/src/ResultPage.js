import React from 'react';

import { Container, Row, Col } from 'reactstrap';

import Image from 'react-bootstrap/Image'
import {
    withRouter
} from 'react-router-dom'
import { Map, GoogleApiWrapper, Marker } from 'google-maps-react';
import ReactAudioPlayer from 'react-audio-player';



class ResultPage extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            text: undefined,
            places: [],
            audio: undefined,
            checked: [false, false, false, false, false,
                false, false, false, false, false,
                false, false, false, false, false,
                false, false, false, false, false],
            mapProps: undefined,
            map: undefined,
            markers: [],
            audio_loading: localStorage.getItem('audioLoading') || undefined,
            near_place: localStorage.getItem('nearPlace') || undefined,
            text_loading: localStorage.getItem('textLoading') || undefined,
            near_places: ["metro_bw", "estacionTren_bw", "aeropuerto_bw", "bus_bw", "tranvia_bw",
                            "cafeteria_bw", "parque_bw", "restaurante_bw", "centroComercial_bw", "farmacia_bw",
                            "gasolinera_bw", "museo_bw", "parking_bw", "iglesia_bw", "hospital_bw",
                            "cajero_bw", "policia_bw", "supermercado_bw", "zoo_bw", "atraccionTuristica_bw"],
            img_height: 0

        }
        if (typeof this.props.location.state !== 'undefined') {
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

        this.calcHeight = this.calcHeight.bind(this);
        this.fetchPlaces = this.fetchPlaces.bind(this);
        this.handlePlaces = this.handlePlaces.bind(this);
        this.crearMarcador = this.crearMarcador.bind(this)
        this.removeItemFromArr = this.removeItemFromArr.bind(this)
        this.audio = null
        this.text = undefined
        this.places = ['subway_station', 'train_station', 'airport', 'bus_station', 'light_rail_station',
            'cafe', 'park', 'restaurant', 'shopping_mall', 'pharmacys',
            'gas_station', 'museum', 'parking', 'church', 'hospital',
            'atm', 'police', 'supermarket', 'zoo', 'tourist_attraction']

    }

    calcHeight(e) {
        let height = e.target;
        console.log(height);
        /*this.setState({
            img_height: node.offsetHeight
            });*/
    }

    componentDidMount() {
        if (typeof this.props.location.state !== 'undefined') {
            if (this.landmark !== undefined) {
                fetch('/title/' + 'Nearby places' + '/' + this.language).then(res => res.json()).then(data => {
                    this.setState({ near_place: data.title })
                    localStorage.setItem('nearPlace', data.title);
                });

                fetch('/title/' + 'Loading audio...' + '/' + this.language).then(res => res.json()).then(data => {
                    this.setState({ audio_loading: data.title })
                    localStorage.setItem('audioLoading', data.title);
                });

                fetch('/title/' + 'Loading text...' + '/' + this.language).then(res => res.json()).then(data => {
                    this.setState({ text_loading: data.title })
                    localStorage.setItem('textLoading', data.title);
                });
                fetch('/text/' + this.landmark + '/' + this.language).then(res => res.json()).then(data => {
                    this.setState({ text: data.text });
                    localStorage.setItem('text', data.text);
                    if (this.audio_check === 'true') {
                        fetch('/speech/' + this.state.text + '/' + this.language).then(res => res.json()).then(data => {
                            localStorage.setItem('audio', data.audio);
                            this.setState({ audio: data.audio });

                        }).catch(error => {
                            fetch('/title/' + 'Audio generating error' + '/' + this.language).then(res => res.json()).then(data => {
                                this.setState({ audio_loading: data.title });
                                localStorage.setItem('audioLoading', data.title);
                            });
                        });
                    }

                }).catch(error => {
                    fetch('/title/' + 'Text generating error' + '/' + this.language).then(res => res.json()).then(data => {
                        this.setState({ text_loading: data.title });
                        localStorage.setItem('textLoading', data.title);
                    });
                    fetch('/title/' + 'Audio generating error' + '/' + this.language).then(res => res.json()).then(data => {
                        this.setState({ audio_loading: data.title });
                        localStorage.setItem('audioLoading', data.title);
                    });
                });


            }
        } else {
            this.setState({ text: localStorage.getItem('text') });
            this.setState({ audio: localStorage.getItem('audio') });

        }



    }

    fetchPlaces(mapProps, map) {
        const { google } = mapProps;
        const service = new google.maps.places.PlacesService(map);
        var latLng = new google.maps.LatLng(this.latitud, this.longitud);
        for (var i = 0; i < this.state.markers.length; i++) {
            this.state.markers[i].setMap(null);
        }
        for (var i = 0; i < this.state.places.length; i++) {
            var request = {
                location: latLng,
                radius: 5000,
                //openNow: true, //si los queremos abiertos ahora
                type: this.state.places[i]
            };
            service.nearbySearch(request, (results, status) => {
                if (status === google.maps.places.PlacesServiceStatus.OK) {

                    for (var j = 0; j < results.length; j++) {
                        this.crearMarcador(results[j], mapProps, map, latLng);
                    }
                }


            });
        }

        this.setState({ mapProps: mapProps, map: map });

    }
    crearMarcador(place, mapProps, map, latLng) {
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

        let m = this.state.markers;
        m.push(marker);
        this.setState({ markers: m });

        google.maps.event.addListener(marker, 'click', function () {
            var stars = "";
            for (var i = 0; i < place.rating; i++) {
                stars += " <img src=\"images/star.png\" width=\"15\" hight=\"15\"></img>"
            }
            const service = new google.maps.DistanceMatrixService();
            const matrixOptions_driving = {
                origins: [latLng.lat() + ', ' + latLng.lng()], // technician locations
                destinations: [place.geometry.location.lat() + ', ' + place.geometry.location.lng()], // customer address
                travelMode: 'DRIVING',
                unitSystem: google.maps.UnitSystem.IMPERIAL
            };
            // Call Distance Matrix service
            service.getDistanceMatrix(matrixOptions_driving, (response, status) => {
                if (status !== "OK") {
                    alert("Error with distance matrix");
                    return;
                }
                let time_driving = response.rows[0].elements[0].duration.text;
                let car = "<img src=\"images/coche.png\" width=\"40\" hight=\"40\"></img>"
                html += "</b> <br/>" + car + "  " + "</b>" + time_driving + "<br/>";
                infowindow.setContent(html);



            });
            const matrixOptions_walk = {
                origins: [latLng.lat() + ', ' + latLng.lng()], // technician locations
                destinations: [place.geometry.location.lat() + ', ' + place.geometry.location.lng()], // customer address
                travelMode: 'WALKING',
                unitSystem: google.maps.UnitSystem.IMPERIAL
            };
            service.getDistanceMatrix(matrixOptions_walk, (response, status) => {
                if (status !== "OK") {
                    alert("Error with distance matrix");
                    return;
                }
                let time_walking = response.rows[0].elements[0].duration.text;
                let walk = "<img src=\"images/andar.png\" width=\"40\" hight=\"40\"></img>"
                html += "</b> <br/>" + walk + "  " + "</b>" + time_walking + "<br/>";
                infowindow.setContent(html);



            });
            const matrixOptions_Transit = {
                origins: [latLng.lat() + ', ' + latLng.lng()], // technician locations
                destinations: [place.geometry.location.lat() + ', ' + place.geometry.location.lng()], // customer address
                travelMode: 'TRANSIT',
                unitSystem: google.maps.UnitSystem.IMPERIAL
            };
            service.getDistanceMatrix(matrixOptions_Transit, (response, status) => {
                if (status !== "OK") {
                    alert("Error with distance matrix");
                    return;
                }
                let time_transit = response.rows[0].elements[0].duration.text;
                let transit = "<img src=\"images/transporte.png\" width=\"40\" hight=\"40\"></img>"
                html += "</b> <br/>" + transit + "  " + "</b>" + time_transit + "<br/>";
                infowindow.setContent(html);



            });
            var html = "<b><strong>" + place.name + "</strong></b> <br/>" + place.vicinity + "</b> <br/>" + stars + "<br/>";
            infowindow.setContent(html);



            infowindow.open(map, this);
        });

    }

    removeItemFromArr(arr, item) {
        var i = arr.indexOf(item);

        if (i !== -1) {
            arr.splice(i, 1);
        }
    }
    handlePlaces(event) {
        let pos = event.target.id;
        let check = this.state.checked
        let pl = this.state.places;
        let near_places = this.state.near_places;
        check[pos] = !check[pos];
        this.setState({ checked: check })
        if (check[pos]) {

            pl.push(this.places[pos]);
            let image = this.state.near_places[pos];
            var res = image.split("_", 2);
            near_places[pos] = res[0];

        } else {
            this.removeItemFromArr(pl, this.places[pos])
            let image = this.state.near_places[pos];
            near_places[pos] = image +'_bw';
        }
        this.fetchPlaces(this.state.mapProps, this.state.map)
        this.setState({ places: pl, near_places: near_places})
    }

    render() {

        const mapStyles = {
            width: '500px',
            height: '500px',

        };
        if (this.image_rect !== 'undefined') {
            if (this.state.audio !== undefined && this.state.audio !== null) {
                this.audio = <ReactAudioPlayer
                    src={require('./instance/audios/' + this.state.audio)}
                    autoPlay
                    controls
                    currentTime
                />
            } else if (this.audio_check === 'true' && this.state.audio_loading !== undefined) {

                this.audio = <p className="introduction_text">{this.state.audio_loading}</p>


            }
            if (this.state.text !== undefined) {
                this.text = this.state.text;
            } else {
                this.text = this.state.text_loading;

            }

            return (
                <Row>
                    <Col xs='0' sm='0' md='2' className="side_col_l"></Col>
                    <Col xs='12' sm='12' md='8'>
                    <h1><font size='50'>{this.title}</font></h1>
                        <Row>
                            <Col md='6' xs='12' sm='12'>
                            <Image className="image" /*ref={(e) => this.calcHeight(e)}*/ src={require('./instance/images/' + this.image_rect)} style={{ width: '100%', height: 350 }} rounded />
                            </Col>
                            <Col md='6' xs='12' sm='12'>
                            <Container className="scroll_text">
                                        <p className="introduction_text">{this.text}</p>
                            </Container>
                            </Col>
                        </Row>
                        <Row>
                            <Col md='6' xs='12' sm='12'>
                                <Container className="container" style={{height: '500px', width:'94%', marginLeft:'0', paddingLeft: '0'}}>

                                
                                <Map style={{height: '500px', width:'94%'}}
                                            google={this.props.google}
                                            zoom={15}
                                            onReady={this.fetchPlaces}
                                            initialCenter={{ lat: this.latitud, lng: this.longitud }}
                                        >
                                            <Marker position={{ lat: this.latitud, lng: this.longitud }} icon={"http://maps.google.com/mapfiles/ms/icons/blue-dot.png"} />

                                        </Map>
                                
                                        </Container>
                            </Col>
                            
                            <Col md='6' xs='12' sm='12'>
                            <Container>
                            <h4 className="places">{this.state.near_place}</h4>
                                    <Container className="places">
                                        <Row >
                                            <Image className="image" src={"images/"+this.state.near_places[0] +'.png'} id="0" onClick={(e) => this.handlePlaces(e)} style={{ width: 40, height: 40 }} rounded />
                                            <Image className="places" src={"images/"+this.state.near_places[1] +'.png'} id="1" onClick={(e) => this.handlePlaces(e)} style={{ width: 40, height: 40 }} rounded />
                                            <Image className="places" src={"images/"+this.state.near_places[2] +'.png'} id="2" onClick={(e) => this.handlePlaces(e)} style={{ width: 40, height: 40 }} rounded />
                                            <Image className="places" src={"images/"+this.state.near_places[3] +'.png'} id="3" onClick={(e) => this.handlePlaces(e)} style={{ width: 40, height: 40 }} rounded />
                                            <Image className="places" src={"images/"+this.state.near_places[4] +'.png'} id="4" onClick={(e) => this.handlePlaces(e)} style={{ width: 40, height: 40 }} rounded />
                                        </Row>
                                        <Row>
                                            <Image className="image" src={"images/"+this.state.near_places[5] +'.png'} id="5" onClick={(e) => this.handlePlaces(e)} style={{ width: 40, height: 40 }} rounded />
                                            <Image className="places" src={"images/"+this.state.near_places[6] +'.png'} id="6" onClick={(e) => this.handlePlaces(e)} style={{ width: 40, height: 40 }} rounded />
                                            <Image className="places" src={"images/"+this.state.near_places[7] +'.png'} id="7" onClick={(e) => this.handlePlaces(e)} style={{ width: 40, height: 40 }} rounded />
                                            <Image className="places" src={"images/"+this.state.near_places[8] +'.png'} id="8" onClick={(e) => this.handlePlaces(e)} style={{ width: 40, height: 40 }} rounded />
                                            <Image className="places" src={"images/"+this.state.near_places[9] +'.png'} id="9" onClick={(e) => this.handlePlaces(e)} style={{ width: 40, height: 40 }} rounded />
                                        </Row>
                                        <Row>
                                            <Image className="image" src={"images/"+this.state.near_places[10] +'.png'} id="10" onClick={(e) => this.handlePlaces(e)} style={{ width: 40, height: 40 }} rounded />
                                            <Image className="places" src={"images/"+this.state.near_places[11] +'.png'} id="11" onClick={(e) => this.handlePlaces(e)} style={{ width: 40, height: 40 }} rounded />
                                            <Image className="places" src={"images/"+this.state.near_places[12] +'.png'} id="12" onClick={(e) => this.handlePlaces(e)} style={{ width: 40, height: 40 }} rounded />
                                            <Image className="places" src={"images/"+this.state.near_places[13] +'.png'} id="13" onClick={(e) => this.handlePlaces(e)} style={{ width: 40, height: 40 }} rounded />
                                            <Image className="places" src={"images/"+this.state.near_places[14] +'.png'} id="14" onClick={(e) => this.handlePlaces(e)} style={{ width: 40, height: 40 }} rounded />
                                        </Row>
                                        <Row>
                                            <Image className="image" src={"images/"+this.state.near_places[15] +'.png'} id="15" onClick={(e) => this.handlePlaces(e)} style={{ width: 40, height: 40 }} rounded />
                                            <Image className="places" src={"images/"+this.state.near_places[16] +'.png'} id="16" onClick={(e) => this.handlePlaces(e)} style={{ width: 40, height: 40 }} rounded />
                                            <Image className="places" src={"images/"+this.state.near_places[17] +'.png'} id="17" onClick={(e) => this.handlePlaces(e)} style={{ width: 40, height: 40 }} rounded />
                                            <Image className="places" src={"images/"+this.state.near_places[18] +'.png'} id="18" onClick={(e) => this.handlePlaces(e)} style={{ width: 40, height: 40 }} rounded />
                                            <Image className="places" src={"images/"+this.state.near_places[19] +'.png'} id="19" onClick={(e) => this.handlePlaces(e)} style={{ width: 40, height: 40 }} rounded />
                                        </Row>

                                    </Container>
                                    {this.audio}
                                    </Container>
                            </Col>
                            
                        </Row>
                        

                    
                    </Col>
                    <Col xs='0' sm='0' md='2' className="side_col_r"></Col>
                </Row>


            );
        } else {
            return (


                <Container style={{ width: '900px', hight: '900px' }}>
                    <Row className="error">
                        <h1 ><font size='50'>Error :(</font></h1>

                    </Row>
                    <Row >
                        <p><font size='5'>The image could not be detected.</font></p>

                    </Row>

                </Container>

            );
        }


    }
}

export default GoogleApiWrapper({
    apiKey: 'AIzaSyC-hTIvFx317AdIgrB9NewMDbU1WhSB4rY',

})(withRouter(ResultPage));
//export default withRouter(ResultPage);