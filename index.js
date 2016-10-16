var http = require('http');
var fs = require('fs');

var options = {
  host: 'api.forismatic.com',
  path: '/api/1.0/?method=getQuote&format=json&lang=en'
};

var quotes = [];

function getData() {
  setInterval(function () {
    http.get(options, function(response){
      var body = '';

      response.on('data', function(chunk) {
        body += chunk;
      });

      response.on('end', function(data){
        data = JSON.parse(body);
        console.log(data.quoteText)
        quotes.push(data.quoteText)
      });
    }).on("error", function(e){
      console.log("Got error: " + e.message);
    });
  }, 1500);
}

getData()

function pushData(cb) {
  quotes = quotes.filter(function(item, pos) {
    return quotes.indexOf(item) == pos;
  });
  fs.writeFile('data.json', JSON.stringify(quotes), function (err) {
    console.log('Data inserted in data.json');
    cb();
  });
}

process.on('SIGINT', function() {
    pushData(function() {
      process.exit();
    });
});
