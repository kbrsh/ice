var http = require('http');
var fs = require('fs');

var options = {
  host: 'api.forismatic.com',
  path: '/api/1.0/?method=getQuote&format=json&lang=en'
};

var quotes = [];

http.get(options, function(resp){
  resp.on('data', function(data){
    data = JSON.parse(data);




    fs.writeFile('data.json', quotes, function (err) {
      console.log('Data inserted in data.json');
    });


  });
}).on("error", function(e){
  console.log("Got error: " + e.message);
});
