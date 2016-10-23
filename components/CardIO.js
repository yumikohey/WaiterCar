import React, { Component } from 'react';
import { View, StyleSheet, TouchableOpacity, Image, Text } from 'react-native';
import { CardIOModule, CardIOUtilities } from 'react-native-awesome-card-io';
import '../shim.js'

var crypto = require('crypto');

const styles = StyleSheet.create({
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

export default class CardIO extends Component {
  constructor(paid) {
    super();
    this.state = {
      paid: paid
    };
  }

  componentWillMount() {
    CardIOUtilities.preload();
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
              return {paid: !prevState.paid};
            });
          }
        })

      })
      .catch(() => {
        // the user cancelled
      })
  }

  render() {
    return (
      <View>
        <TouchableOpacity onPress={this.scanCard}>
          <Image style={{width: 80, height: 80, resizeMode: 'stretch', marginTop: 30}} source={require('../images/credit_card.png')}/>
          <View style={styles.button}>
              <Text style={styles.textButton}>PAY NOW</Text>
          </View>
        </TouchableOpacity>
      </View>
    );
  }
}