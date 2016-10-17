# split-array [![Build Status](https://travis-ci.org/arthurvr/split-array.svg?branch=master)](https://travis-ci.org/arthurvr/split-array)

> Split an array into arrays of a specific length


## Install

```
$ npm install --save split-array
```


## Usage

```js
var splitArray = require('split-array');

splitArray(['a', 'b', 'c', 'd', 'e', 'f'], 2);
//=> [['a', 'b'], ['c', 'd'], ['e', 'f']]

splitArray(['a', 'b', 'c', 'd', 'e', 'f', 'foo'], 3);
//=> [['a', 'b', 'c'], ['d', 'e', 'f'], ['foo']]
```


## API

### splitArray(array, maxLength)

#### array

*Required*  
Type: `array`

The array to split up.

#### maxLength

*Required*  
Type: `number`  

The maximum amount of items a partial can have


## License

MIT © [Arthur Verschaeve](http://arthurverschaeve.be)
