/**
 * Sample React Native App
 * https://github.com/facebook/react-native
 * @flow
 */

import React, { Component } from 'react';
import {
  AppRegistry,
  StyleSheet,
  Text,
  Image,
  Dimensions,
  ListView,
  TouchableOpacity, 
  View
} from 'react-native';
import { CardIOView, CardIOModule, CardIOUtilities } from 'react-native-awesome-card-io';
import Invoice from './components/Invoice';
import Success from './components/Success';

import './shim.js'

var crypto = require('crypto');

const {height, width} = Dimensions.get('window');

export default class WaiterCar extends Component {
  constructor() {
    super();
    this.state = {
      madePayment: false
    };
  }

  componentWillMount() {
    CardIOUtilities.preload();
    console.log('test');
  }

  componentDidUpdate(prevProps, prevState) {
    if(prevProps.madePayment !== this.state.madePayment){
      return <Success />
    }
  }

  didScanCard(card) {
    // the scanned card
    console.log(card);
  }

  scanCard() {
    CardIOModule
      .scanCard()
      .then(card => {
        // the scanned card
        console.log('scanned');
        var paymentAuthorizationRequest = JSON.stringify({
          "amount": "10",
          "currency": "USD",
          "payment": {
            "cardNumber": "4111111111111111",
            "cardExpirationMonth": "10",
            "cardExpirationYear": "2016"
          }
        });
        var apiKey = 'GC7JI68GHUYE6CLLA7CM21mxYdEXrwOlPd_bJ4LKCJkutKUQ0';
        var baseUri = 'cybersource/';
        var resourcePath = 'payments/v1/authorizations';
        var queryParams = 'apikey=' + apiKey;

        var timestamp = Math.floor(Date.now() / 1000);
        var sharedSecret = 'OMUgXztUzV$9jM6bH8Dw23XtZ#q4i$Cz#gl}ufkP';
        var preHashString = timestamp + resourcePath + queryParams + paymentAuthorizationRequest;
        var hashString = crypto.createHmac('SHA256', sharedSecret).update(preHashString).digest('hex');
        var preHashString2 = resourcePath + queryParams + paymentAuthorizationRequest;
        var hashString2 = crypto.createHmac('SHA256', sharedSecret).update(preHashString2).digest('hex');
        var xPayToken = 'xv2:' + timestamp + ':' + hashString;
        console.log(xPayToken);

        fetch('https://sandbox.api.visa.com/cybersource/payments/v1/authorizations?apikey='+apiKey, {
          method: 'POST',
          headers: {
            'content-type': 'application/json',
            'x-pay-token': xPayToken
          },
          body: paymentAuthorizationRequest
        })
        .then((response) => {
          if(response.status === 201){
            this.setState((prevState, props) => {
              return {madePayment: !prevState.madePayment};
            });
            console.log(this.state.madePayment);
          }
        })

      })
      .catch(() => {
        // the user cancelled
      })
  }

  visaCheckout() {
    CardIOModule
      .scanCard()
      .then(card => {
        // the scanned card
        console.log('scanned');
        var paymentAuthorizationRequest = JSON.stringify({
          "amount": "10",
          "currency": "USD",
          "payment": {
            "cardNumber": "4111111111111111",
            "cardExpirationMonth": "10",
            "cardExpirationYear": "2016"
          }
        });
        var apiKey = 'GC7JI68GHUYE6CLLA7CM21mxYdEXrwOlPd_bJ4LKCJkutKUQ0';
        var baseUri = 'cybersource/';
        var resourcePath = 'payments/v1/authorizations';
        var queryParams = 'apikey=' + apiKey;

        var timestamp = Math.floor(Date.now() / 1000);
        var sharedSecret = 'OMUgXztUzV$9jM6bH8Dw23XtZ#q4i$Cz#gl}ufkP';
        var preHashString = timestamp + resourcePath + queryParams + paymentAuthorizationRequest;
        var hashString = crypto.createHmac('SHA256', sharedSecret).update(preHashString).digest('hex');
        var preHashString2 = resourcePath + queryParams + paymentAuthorizationRequest;
        var hashString2 = crypto.createHmac('SHA256', sharedSecret).update(preHashString2).digest('hex');
        var xPayToken = 'xv2:' + timestamp + ':' + hashString;
        console.log(xPayToken);

        fetch('https://sandbox.api.visa.com/cybersource/payments/v1/authorizations?apikey='+apiKey, {
          method: 'POST',
          headers: {
            'content-type': 'application/json',
            'x-pay-token': xPayToken
          },
          body: paymentAuthorizationRequest
        })
        .then((response) => {
          if(response.status === 201){
            this.setState((prevState, props) => {
              return {madePayment: !prevState.madePayment};
            });
            console.log(this.state.madePayment);
          }
        })

      })
      .catch(() => {
        // the user cancelled
      })
  }

  render() {
    if(!this.state.madePayment){
      return (
        <View style={styles.container}>
          <Image style={styles.background} source={require('./images/background.png')} resizeMode={'cover'} />
            <Text style={styles.subtitle}>
              Make a payment?
            </Text>
            <TouchableOpacity onPress={this.scanCard.bind(this)}>
              <Image style={{width: 80, height: 80, resizeMode: 'stretch', marginTop: 30}} source={require('./images/credit_card.png')}/>
              <View style={styles.button}>
                  <Text style={styles.textButton}>PAY NOW</Text>
              </View>
            </TouchableOpacity>
            <Invoice />
            <View style={styles.row}>
              <Image style={{width: 200, height: 150, transform: [{scaleX: 1.5}, {scaleY: 1.5}], resizeMode: 'center', marginLeft: -10}} source={require('./images/visa-checkout.png')} />
              <Image style={{width: 100, height: 100, resizeMode: 'center', marginLeft: 10, marginTop: 30}} source={require('./images/qrCode.png')} />
            </View>
            <CardIOView
              didScanCard={this.didScanCard}
              style={{ flex: 1 }}
            />
        </View>
      );
    }else{
      return (
        <View style={styles.container}>
          <Image style={styles.background} source={require('./images/background.png')} resizeMode={'cover'} />
          <Image style={{width: 100, height: 100, resizeMode: 'center'}} source={require('./images/check-white.png')}/>
          <Text style={styles.subtitle}>
            Thank you for using Robot to complete payments ;)
          </Text>
        </View>
      )
    }
  }
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#F5FCFF',
  },
  row: {
    flexDirection: 'row',
    justifyContent: 'center',
    padding: 10,
    backgroundColor: 'transparent',
    borderColor: 'transparent',
    borderWidth: 1,
    marginTop: 50
  },
  subtitle: {
    fontSize: 25,
    textAlign: 'center',
    marginTop: 50,
    color: 'white',
    backgroundColor: 'transparent'
  },
  instructions: {
    textAlign: 'center',
    color: '#333333',
    marginBottom: 5,
  },
  background: {
    position: 'absolute',
    top: 0,
    left: 0,
    right: 0,
    bottom: 0,
    width: width,
    height: height
  },
  infoContainer: {
    position: 'absolute',
    bottom: 20,
    left: 20,
    width: 300,
    justifyContent: 'center'
  },
  button: {
    marginTop: 50,
    height: 100,
    width: 100,
    backgroundColor: '#1ba549',
    justifyContent: 'center',
    borderRadius: 50,
    backgroundColor: 'transparent',
    borderWidth: 1,
    borderColor: '#fff',
  },
  button: {
    height: 20,
    backgroundColor: '#1ba549',
    justifyContent: 'center',
    backgroundColor: 'transparent',
  },
  textButton: {
    textAlign: 'center',
    color: '#fff'
  }
});

AppRegistry.registerComponent('WaiterCar', () => WaiterCar);


