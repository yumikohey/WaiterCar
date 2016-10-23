import React, { Component } from 'react';
import { View, StyleSheet, ListView, Text, Image} from 'react-native';


export default class Invoice extends Component {
  constructor() {
    super();
    const ds = new ListView.DataSource({rowHasChanged: (r1, r2) => r1 !== r2});
    this.state = {
      dataSource: ds.cloneWithRows(['Pasta', 'Robster']),
      total: 32
    };
  }

  _renderRow(rowData: string, sectionID: number, rowID: number, highlightRow: (sectionID: number, rowID: number) => void) {
    return (
        <View>
          <View style={styles.row}>
            <Text style={styles.textList}>
              {rowData}
            </Text>
            <Text style={styles.text}>
            ${ (rowID+3) * 2 }
            </Text>
          </View>
        </View>
    );
  }

  render() {
    return (
      <View>
        <View style={styles.listTitle}>
          <Text style={{ color: '#fff', backgroundColor: 'transparent', fontSize: 20 }}> Receipt </Text>
        </View>
        <ListView
          dataSource={this.state.dataSource}
          renderRow={this._renderRow}
          style={styles.list}
        />
        <View style={styles.total}>
          <Text style={{ color: '#fff', backgroundColor: 'transparent' }}>Total:    ${this.state.total}.00</Text>
        </View>
      </View>
    );
  }

}

const styles = StyleSheet.create({
  list: {
    shadowColor: "#000",
    shadowOpacity: 0.8,
    shadowRadius: 2,
    shadowOffset: {
      height: -3,
      width: 0
    },
    backgroundColor: 'rgba(0,0,0,0.2)'
  },
  row: {
    flexDirection: 'row',
    justifyContent: 'center',
    padding: 10,
    backgroundColor: 'transparent',
    borderColor: 'transparent',
    borderWidth: 1
  },
  textList: {
    flex: 1,
    width: 250,
    color: '#fff'
  },
  text: {
    color: '#fff'
  },
  total: {
    flexDirection: 'row',
    padding: 10,
    backgroundColor: 'transparent',
    borderColor: 'transparent',
    borderWidth: 1,
    borderBottomRightRadius: 5,
    borderBottomLeftRadius: 5,
    shadowColor: "#000",
    shadowOpacity: 0.8,
    shadowRadius: 2,
    shadowOffset: {
      height: -3,
      width: 0
    },
    backgroundColor: 'rgba(0,0,0,0.2)',
    justifyContent: 'flex-end'
  },
  listTitle: {
    marginTop: 50,
    flexDirection: 'row',
    padding: 10,
    backgroundColor: 'transparent',
    borderColor: 'transparent',
    borderWidth: 1,
    shadowColor: "#000",
    shadowOpacity: 0.8,
    borderTopRightRadius: 5,
    borderTopLeftRadius: 5,
    shadowOffset: {
      height: -3,
      width: 0
    },
    backgroundColor: 'rgba(0,0,0,0.2)',
    justifyContent: 'center'
  }
});



