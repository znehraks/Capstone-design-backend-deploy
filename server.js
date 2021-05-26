const express = require("express");
const bodyParser = require("body-parser");
const { spawn } = require("child_process");
const cors = require('cors');
const app = express();
const port = 3002;
const connection = require("./connection");

//크롤링 및 분석 후에 최종 res.send로 프론트에 전달해야 함.
//json parsing하는데에 변수가 많음.

app.use(cors());
// "Origin, X-Requested-With, Content-Type, Accept"
app.use(function (req, res, next) {
  res.header("Access-Control-Allow-Origin", "*");
  res.header(
    "Access-Control-Allow-Headers",
    "Origin, X-Requested-With, Content-Type, Accept"
  );
  next();
});
// app.all('/*', function(req, res, next) {
//   res.header("Access-Control-Allow-Origin", "*");
//   res.header("Access-Control-Allow-Headers", "X-Requested-With");
//   next();
// });

app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json());

String.prototype.replaceAll = function (org, dest) {
  return this.split(org).join(dest);
};


connection.getConnection(function (err, connection) {
  if (!err) {
    console.log("getConnected");
  }
  connection.release();
});


//recommendation 라우터
app.post("/recommendation", (req, res) => {
  try {
    var data;
    //   var largeDataset = [];
    // spawn new child process to call the python script
    const python = spawn("python3", [
      "./cal_weight.py",
      req.body.univ_name,
      req.body.univ_lon,
      req.body.univ_lat,
      req.body.Q2Answer,
      req.body.Q3Answer,
      req.body.Q4Answer,
      req.body.Q5Answer,
      req.body.w1,
      req.body.w2,
      req.body.w3,
      req.body.w4,
      req.body.w5,
    ]);
    // collect data from script
    python.stdout.on("data", function (chunk) {
      // console.log("Pipe data from python script ...");
      // largeDataset.push(data);

      data = chunk.toString("utf-8");
    });

    // in close event we are sure that stream from child process is closed
    python.on("close", (code) => {
      console.log(`child process close all stdio with code ${code}`);
      res.json(data);
    });
  } catch (e) {}
});

//히스토리라우터
app.get("/get_diy", (req, res) => {
  let sql = "SELECT * FROM diy_reco_history where is_deleted = 0";
  connection.query(sql, (err, rows, fields) => {
    res.send(rows);
  });
});

//히스토리추가
app.post("/add_diy", (req, res) => {
  let sql = `INSERT INTO diy_reco_history(user_no, w_1st, w_2nd, w_3rd, w1, w2, w3, w4, w5, total_w, Q1, Q2, Q3, Q4, Q5, univ_lat, univ_lon, T_set ) values (${req.body.user_no}, ${req.body.w_1st}, ${req.body.w_2nd}, ${req.body.w_3rd}, ${req.body.w1}, ${req.body.w2}, ${req.body.w3}, ${req.body.w4}, ${req.body.w5}, ${req.body.total_w},'${req.body.Q1}', ${req.body.Q2},'${req.body.Q3}','${req.body.Q4}','${req.body.Q5}',${req.body.univ_lat},${req.body.univ_lon}, '${req.body.T_set}')`;

  connection.query(sql, (err, rows, fields) => {
    res.send(rows);
    console.log(err);
  });
});

//설문조사 저장 라우터
app.post("/add_eval", (req, res) => {
  let sql = `INSERT INTO evaluation(evaluation_category_no, univ_name, T_set, rank01_score, rank02_score, rank03_score, rank04_score, rank05_score) values (${req.body.evaluation_category_no}, '${req.body.univ_name}', '${req.body.T_set}', ${req.body.rank01_score}, ${req.body.rank02_score}, ${req.body.rank03_score}, ${req.body.rank04_score}, ${req.body.rank05_score})`;

  connection.query(sql, (err, rows, fields) => {
    res.send(rows);
    console.log(err);
  });
});
//회원가입라우터

//로그인라우터
app.listen(port, () =>
  console.log(`Example app listening on port 
${port}!`)
);