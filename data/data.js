var request = require('request');
var forismatic = require('forismatic-node')();
var fs = require('fs');
var hexu = require('hexu');


var quotes = JSON.parse(fs.readFileSync(__dirname + "/data.json")) || [];
module.exports.quotes = quotes;

// console.log(hexu.blue("*** Ice is mining data ***"));
function pushData(cb) {
  quotes = quotes.filter(function(item, pos) {
    return quotes.indexOf(item) == pos;
  });
  fs.writeFile(__dirname + '/data.json', JSON.stringify(quotes), function (err) {
    cb();
  });
}

module.exports.addData = function(data) {
  quotes.push(data);
  fs.writeFile(__dirname + '/data.json', JSON.stringify(quotes), function (err) {});
}


function mineData() {
  request('http://quote.machinu.net/api', function (error, response, body) {
      if (!error && response.statusCode == 200) {
        var obj = JSON.parse(body);
        if(obj.text.split(" ").length <= 10 && obj.text.split(" ").length >= 3 && !/fuck|shit|damn|sex|virgin|masturbate|hoe|bitch|dick|frig|cock/gi.test(obj.text)) {
          console.log(hexu.green("\t Success \u2713 => ") + "Mined Data: " + obj.text.replace(/"/g, ""));
          quotes.push(obj.text.replace(/"/g, ""));
        }
      }
  });

  forismatic.getQuote(function (err, quote) {
    if(err) {
      throw err;
    }
    if(quote.quoteText.split(" ").length <= 10) {
      console.log(hexu.green("\t Success \u2713 => ") + "Mined Data: " + quote.quoteText);
      quotes.push(quote.quoteText);
    }
  });
}

setInterval(mineData, 2000);


process.on('SIGINT', function() {
    pushData(function() {
      process.exit();
    });
});
