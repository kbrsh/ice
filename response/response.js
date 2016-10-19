function randomElement(arr) {
    return arr[Math.floor(Math.random() * arr.length)];
}

module.exports.get(data, min) {
    var sentence = [];
    var map = {};
    var starters = [];
    for (var i = 0; i < data.length; i++) {
        var words = data[i].split(" ");
        starters.push(words[0]);
        for (var j = 0; j < words.length; j++) {
            if (map.hasOwnProperty(words[j])) {
                map[words[j]].push(words[j + 1]);
            } else {
                map[words[j]] = [words[j + 1]];
            }
        }
    }

    var word = randomElement(starters);
    var counter = 0;
    sentence.push(word);

    while(map.hasOwnProperty(word)) {
    	counter++;
    	var nexts = map[word];
      word = randomElement(nexts);
      sentence.push(word);
      if(map[word] === [null] && counter > min) break;
    }

    return sentence.join(" ");
}
