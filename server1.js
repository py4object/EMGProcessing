var app = require('express')();
var http = require('http').Server(app);
var io = require('socket.io')(http);
kdata={};
sockets=[];

io.on('connection', function(socket){
  console.log('a user connected');

  socket.on('emg',function(data){
    console.log({'emg':data});

    socket.broadcast.emit('emg',{'emg':data});

  })


  socket.on('kdata',function(data){
    console.log({y:data});
    socket.broadcast.emit('kdata',{y:data});
  })
});

app.get('/', function(req, res){
  res.send('<h1>yes you are connected</h1>');
});

http.listen(8080, function(){
  console.log('listening on *:8080');
});
