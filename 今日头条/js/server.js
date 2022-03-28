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

app.post("/get_signs", (req, res) => {
    let result = req.body;
    let a = result.urls;
    result = encrypt.get_sign(a);
    res.send(result.toString());
});

app.get("/get_sum", (req, res) =>{
    let a = parseInt(req.query.a)
    let b =parseInt(req.query.b)
    result = sum.add(a, b)
    res.send(result.toString())
});

app.listen(9999, () => {
    console.log("开启服务，端口9999");
});
