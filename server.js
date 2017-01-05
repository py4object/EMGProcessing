var express = require('express')
, bodyParser = require('body-parser');

var app = express();

app.use(bodyParser.json());
kneict={};
emg={};
  app.get('/kenict', function (req, res) {

    res.send(kneict)
      kneict={}
})
app.get('/emg', function (req, res) {

  res.send(emg)
    emg={}
})
app.post('/kenict', function(request, response){
  console.log(request.body);      // your JSON
  kneict=request.body   // echo the result

  response.send()
});
app.post('/emg', function(request, response){
  console.log(request.body);      // your JSON
  kneict=request.body   // echo the result
  response.send()
});

app.listen(3000, function () {
  console.log('Example app listening on port 3000!')
})
