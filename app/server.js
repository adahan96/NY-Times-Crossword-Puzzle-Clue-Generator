
const express = require("express");
const app = express();
const fs = require("fs");
// we've started you off with Express,
// but feel free to use whatever libs or frameworks you'd like through `package.json`.

// http://expressjs.com/en/starter/static-files.html
app.use(express.static("public"));

// http://expressjs.com/en/starter/basic-routing.html
app.get("/", function (request, response) {
  response.sendFile(__dirname + "/views/index.html");
});

app.get("/adahan", function (request, response) {
  response.sendFile(__dirname + "/views/index.html");
});

app.get('/data', (req, res) => {
  var exec = require('child_process').exec;
  exec("source .env/bin/activate && python main.py", {
    cwd: ".."
  },
    function (error, stdout, stderr) {
      console.log('stdout: ' + stdout);
      console.log('stderr: ' + stderr);
      if (error !== null) {
        console.log('exec error: ' + error);
      }
      res.json(JSON.parse(fs.readFileSync("data.json", 'utf8')))
    });
});


// listen for requests :)
const listener = app.listen(3131, function () {
  console.log("Your app is listening on port " + listener.address().port);
});
