const express = require('express');
const app = express();
const cors = require('cors');
const server = require('http').createServer(app);
const spawn = require('child_process').spawn;

app.use(cors());

app.get('/', (req, res) => {
    const result1 = spawn('python', ['./server/hand_recog2/hand_recog.py']);
    const result2 = spawn('python', ['./server/audio_listener.py']);

    result1.stdout.on('data', function(data){
        console.log(data.toString());
    })
    result1.stderr.on('data', function(data){
        console.log(data.toString());
    })
    
})

server.listen(5000, ()=> {
    console.log('running');
})