var request = require('request');
var fs = require('fs');

var options = {
  host: 'quote.machinu.net',
  path: '/api'
};

var quotes = JSON.parse(fs.readFileSync("./data.json")) || [];
module.exports.quotes = quotes;

function pushData(cb) {
  quotes = quotes.filter(function(item, pos) {
    return quotes.indexOf(item) == pos;
  });
  fs.writeFile('data.json', JSON.stringify(quotes), function (err) {
    // console.log('Data inserted in data.json');
    cb();
  });
}

module.exports.addData = function(data) {
  quotes.push(data);
  fs.writeFile('data.json', JSON.stringify(quotes), function (err) {});
}


function mineData() {
var options = {
  host: 'api.forismatic.com',
  path: '/api/1.0/?method=getQuote&key=457653&format=json&lang=en'
};

var req = http.get(options, function(res) {
  var body = [];
  res.on('data', function(chunk) {
    body.push(chunk);
  }).on('end', function() {
    var data = JSON.parse(body);
    console.log(data.quoteText);
    quotes.push(data.quoteText)
  })
});
}

setInterval(mineData, 1500);


process.on('SIGINT', function() {
    pushData(function() {
      process.exit();
    });
});
