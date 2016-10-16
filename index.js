var fs = require("fs");
var twitterPkg = require("twitter");
var express = require('express');
var hexu = require("hexu");
var app = express();

var addData = require("./data.js").addData;

var config = JSON.parse(fs.readFileSync("./config.json"));

var data = JSON.parse(fs.readFileSync("./data.json"));

var Twitter = new twitterPkg(config);


var terminals = {};
var startwords = [];
var wordstats = {};

for (var i = 0; i < data.length; i++) {
    var words = data[i].split(' ');
    terminals[words[words.length-1]] = true;
    startwords.push(words[0]);
    for (var j = 0; j < words.length - 1; j++) {
        if (wordstats.hasOwnProperty(words[j])) {
            wordstats[words[j]].push(words[j+1]);
        } else {
            wordstats[words[j]] = [words[j+1]];
        }
    }
}

var choice = function (a) {
    var i = Math.floor(a.length * Math.random());
    return a[i];
};

var generate = function (min_length) {
    word = choice(startwords);
    var title = [word];
    while (wordstats.hasOwnProperty(word)) {
        var next_words = wordstats[word];
        word = choice(next_words);
        title.push(word);
        if (title.length > min_length && terminals.hasOwnProperty(word)) break;
    }
    if (title.length < min_length) return generate(min_length);
    return title.join(' ');
};

var makePost = function() {
  var post = generate(5);
  Twitter.post('statuses/update', {status: post},  function(error, tweet, response){
    if(error){
      console.log(hexu.red(error));
    }
    console.log(hexu.green("Tweeted: " + post));
    addData(post);
  });
}

var greeting = function() {
  Twitter.post('statuses/update', {status: "I'm alive. Hello world?"},  function(error, tweet, response){
    if(error){
      console.log(error);
    }
    console.log(tweet);  // Tweet body.
    console.log(response);  // Raw response object.
  });
}

// Routes
app.get("/", function(req, res) {
  res.header('Content-Type', 'application/json');
  res.sendFile(__dirname + "/data.json");
});

app.listen(3000);

// greeting()
makePost()
setInterval(makePost, 1000 * 60 * 60)
