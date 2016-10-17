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
  request('http://api.forismatic.com/api/1.0/?method=getQuote&key=457653&format=json&lang=en', function (error, response, body) {
      if (!error && response.statusCode == 200 && !body.match(new RegExp("\'", "g")) && !body.match(new RegExp("\"\"", "g"))) {
        var obj = JSON.parse(body);
        console.log(obj.quoteText);
        quotes.push(obj.quoteText);
      }
  });
  request('http://quote.machinu.net/api', function (error, response, body) {
      if (!error && response.statusCode == 200) {
        var obj = JSON.parse(body);
        console.log(obj.text);
        quotes.push(obj.text);
      }
  });
}

setInterval(mineData, 1500);


process.on('SIGINT', function() {
    pushData(function() {
      process.exit();
    });
});
