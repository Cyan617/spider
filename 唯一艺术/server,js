const express = require("express");
const bodyParser = require("body-parser");

const encrypt = require("./test");

var app = express();
app.use(bodyParser.json({limit:'100mb'}));
app.use(bodyParser.urlencoded({ limit:'100mb', extended: true }));

app.use(
    bodyParser.urlencoded({
        extended: true,
    })
);
app.use(bodyParser.json());

app.post("/decrypt", (req, res) => {
    let result = req.body;
    let a = result.data;
    result = encrypt.get_decrypt(a);
    res.send(result.toString());
});

app.post("/encrypt", (req, res) => {
    let result = req.body;
    let a = result.id;
    let b = result.num;
    result = encrypt.get_encrypt(a, b);
    res.send(result.toString());
});

app.listen(9999, () => {
    console.log("开启服务，端口9999");
});
