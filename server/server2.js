const express = require('express');
const app = express();
const cors = require('cors');
const server = require('http').createServer(app);
const spawn = require('child_process').spawn;
const {PythonShell} = require('python-shell');

app.use(cors());

app.get('/', (req, res) => {

    PythonShell.run("./server/hand_recog2/hand_recog.py", function(err, data) {
        if (err) throw err;

        console.log("수어 인식");

        let result = data[0].replace(`b\'`, '').replace(`\'`, '');
        let buff = Buffer.from(result, 'base64');
        let text = buff.toString('utf-8');

        console.log(text);
    })

    PythonShell.run("./server/audio_listener.py", function(err, data) {
        if (err) throw err;

        console.log("소리 인식");
        
        let result = data[0].replace(`b\'`, '').replace(`\'`, '');
        let buff = Buffer.from(result, 'base64');
        let text = buff.toString('utf-8');

        console.log(text);
    })

    // const result1 = spawn('python', ['./server/hand_recog2/hand_recog.py']);
    // const result2 = spawn('python', ['./server/audio_listener.py']);

    /*
    result1.stdout.on('data', function(data){
        console.log(data.toString());
    })
    result1.stderr.on('data', function(data){
        console.log(data.toString());
    })
    */
    
})

server.listen(5000, ()=> {
    console.log('running');
})