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
    // const {hands1} = req.query;

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

    /*
    let args = {hands1};
    let options = {
        args: [hands1]
    }
    */
    
    console.log(req.query);
    // const optionsJSON = JSON.stringify(options);
    // console.log(options);
    // console.log(optionsJSON);

    PythonShell.run("./server/hand_recog/module1.py", req.query, function(err, data) {
        if (err) throw err;

        let result = data[0].replace(`b\'`, '').replace(`\'`, '');

        let buff = Buffer.from(result, 'base64');
        let text = buff.toString('utf-8');
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
                });
            }
        })
        
    });

})

app.get('/response', (req, res) => {

    // 파일을 열어서 내부 값 전달하기
    const file = './server/test.txt';
    fs.readFile('sample.txt', 'utf8', function(err, data){
        console.log(data);
    });
    res.send(text);

})
server.listen(5000, ()=> {
    console.log('running');
})