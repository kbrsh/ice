var http = require('http');
var fs = require('fs');

var options = {
  host: 'quote.machinu.net',
  path: '/api'
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
        console.log(data.text)
        quotes.push(data.text)
      });
    }).on("error", function(e){
      console.log("Got error: " + e.message);
    });
  }, 1500);
}

function pushData(cb) {
  quotes = quotes.filter(function(item, pos) {
    return quotes.indexOf(item) == pos;
  });
  fs.writeFile('data.json', JSON.stringify(quotes), function (err) {
    console.log('Data inserted in data.json');
    cb();
  });
}

module.exports.addData = function(data) {
  quotes = fs.readFileSync("./data.json");
  quotes.push(data);
  fs.writeFile('data.json', JSON.stringify(quotes), function (err) {
    console.log('Data inserted in data.json');
  });
}

getData();

process.on('SIGINT', function() {
    pushData(function() {
      process.exit();
    });
});
