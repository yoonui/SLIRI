const express = require('express');
const app = express();
const cors = require('cors');
const server = require('http').createServer(app);
const mysql = require('mysql');
const {PythonShell} = require('python-shell');
const fs = require('fs');

const conn = {
    host: 'localhost',
    port: '3306',
    user: 'root',
    password: '1189',
    database: 'demo'
}
app.use(cors());

app.get('/myhand', (req, res) => {
    const {num, hands1, hands2, hands3} = req.query;

    /*mysql 연결 부분
    const connection = mysql.createConnection(conn);
    connection.connect();

    const testQuery = "select * from test where id = " + id;
    
    connection.query(testQuery, function(err, result, fields){
        if(err){
            console.log(err);
        }
        console.log(result);
        res.send(result);
    })
    */

    let options = {
        args: [hands1, hands2, hands3]
    }
    // const optionsJSON = JSON.stringify(options);
    // console.log(options);
    // console.log(optionsJSON);

    PythonShell.run("./server/hand_recog/hand_recog_json.py", options, function(err, data) {
        if (err) throw err;

        let result = data[0].replace(`b\'`, '').replace(`\'`, '');

        let buff = Buffer.from(result, 'base64');
        let text = buff.toString('utf-8');g
        console.log(text);
        
        /* 파일관련 코드 추가 */
        const file = './server/test.txt';
        fs.open(file, 'a', function(err, fd) { // 파일 생성
            if(err) throw err;
            if(fd == '9'){
                console.log('file create.');
            } else { // 파일 이어쓰기
                fs.appendFile('./server/test.txt', text, function(err){
                    if(err) throw err;
                    console.log('Appended to file!');
                    res.send(text);
                });
            }
        })
        
    });

})

server.listen(5000, ()=> {
    console.log('running');
})