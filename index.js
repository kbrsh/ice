var http = require('http');

var options = {
  host: 'api.forismatic.com',
  path: '/api/1.0/?method=getQuote&format=json&lang=en'
};

http.get(options, function(resp){
  resp.on('data', function(data){
    console.log(JSON.parse(data));
  });
}).on("error", function(e){
  console.log("Got error: " + e.message);
});
