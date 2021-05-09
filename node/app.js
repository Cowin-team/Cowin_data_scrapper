// var express = require('express');
// // var app = express();

const pune = require('./services/pune');
const tamilnadu = require('./services/tamilnadu');
const mumbai = require('./services/rcmedicrew');
const telangana = require('./services/telangana');

const sheetsAPI = require('./services/sheetsAPI');


telangana.fetchData().then((response) => {
    // console.log(response)
    sheetsAPI.send(response).then((res) => {
        console.log(res)
    })
})

// app.get('/mumbai', function (req, res) {
//     mumbai.fetchData().then((response) => {
//         res.send(response)
//     })
//     // res.send('Hello World');
//  })
 
//  var server = app.listen(8081, function () {
//     var host = server.address().address
//     var port = server.address().port
    
//     console.log("Example app listening at http://%s:%s", host, port)
//  })