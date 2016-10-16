var http = require('http');
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

quotes = quotes.slice(100, quotes.length)
fs.writeFile('data.json', JSON.stringify(quotes), function (err) {
});

console.log(quotes.length)

process.on('SIGINT', function() {
    pushData(function() {
      process.exit();
    });
});
