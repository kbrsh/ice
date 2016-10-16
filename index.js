var http = require('http');
var fs = require('fs');

var options = {
  host: 'api.forismatic.com',
  path: '/api/1.0/?method=getQuote&format=json&lang=en'
};

var quotes = [];

function getData() {
  for(var i = 0; i < 100; i++) {
    http.get(options, function(resp){
      resp.on('data', function(data){
        data = JSON.parse(data);
        quotes.push(data.quoteText)
      });
    }).on("error", function(e){
      console.log("Got error: " + e.message);
    });
  }
}
