const express = require('express');
const app = express();
const cors = require('cors');
const server = require('http').createServer(app);
const mysql = require('mysql');

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

    /*
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

    //console.log(num + ' 1 : ' + hands1 + ",\n2 : " + hands2 + ",\n3 : " + hands3);
    console.log(req);
})

server.listen(5000, ()=> {
    console.log('running');
})