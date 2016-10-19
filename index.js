var fs = require("fs");
var twitterPkg = require("twitter");
var express = require('express');
var hexu = require("hexu");
var request = require("request");
var kov = require("kov");
var app = express();

var addData = require("./data/data.js").addData;

var config = JSON.parse(fs.readFileSync("./config.json"));

var data = JSON.parse(fs.readFileSync("./data/data.json"));

var Twitter = new twitterPkg(config);

var opts = {
  type: "sentence",
  min: 2,
  max: 5
}


var makePost = function() {
  var post = response.get(data, 2);
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
  });
}

// Routes
app.get("/", function(req, res) {
  res.header('Content-Type', 'application/json');
  res.end(JSON.stringify(require("./data/data.js").quotes));
  // console.log(hexu.green("GET '/'"));
});

app.get("/new", function(req, res) {
  makePost();
  console.log(hexu.green("GET '/new', making new post..."));
})

app.listen(process.env.OPENSHIFT_NODEJS_PORT || 3000, process.env.OPENSHIFT_NODEJS_IP || "localhost");
console.log(hexu.blue("======= Ice is Awake ======="))

makePost()
setInterval(makePost, 1000 * 60 * 60)
