var fs = require("fs");

var data = JSON.parse(fs.readFileSync("./data.json"));

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

console.log(generate(5))
