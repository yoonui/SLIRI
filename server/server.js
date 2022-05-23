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
    database: 'capstone'
}
app.use(cors());

// 수어 인식
app.get('/myhand', (req, res) => {
    const {hands1} = req.query;

    // let args = {hands1}
    let options = {
        args: hands1
    }
    
    // console.log(req.query);
    // const optionsJSON = JSON.stringify(hands1);
    // console.log(options);
    console.log(hands1[0]);

    PythonShell.run("./server/hand_recog/module1.py", hands1, function(err, data) {
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
                    //console.log('Appended to file!');
                });
            }
        })
    });

})

// txt 파일 값 전달
app.get('/myhandRes', (req, res) => {

    // 파일을 열어서 내부 값 전달하기
    // 아직 실행 X
    const file = './server/test.txt';
    fs.readFile(file, 'utf8', function(err, data){
        if(err) throw err;
        console.log(data);
        res.send(data);
    });

})

// 명령어 리스트 전달
app.get('/myList', (req, res) => {
    const {hands1} = req.query;

    // DB에서 조회하기
    const connection = mysql.createConnection(conn);
    connection.connect();

    const testQuery = "select list1, list2, list3 from myList where oneChar = " + hands1;
    
    connection.query(testQuery, function(err, result, fields){
        if(err){
            console.log(err);
        }
        console.log(result);
        res.send(JSON.stringify(result));
    })
})

server.listen(5000, ()=> {
    console.log('running');
})