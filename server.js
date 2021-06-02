const express = require("express");
const bodyParser = require("body-parser");
const { spawn } = require("child_process");
const cors = require('cors');
const app = express();
const port = 3002;
const connection = require("./connection");
const bcrypt = require("bcrypt");
const jwt = require("jsonwebtoken");
// const fs = require("fs");
// const data = fs.readFileSync("./email.json");
// const conf = JSON.parse(data);
// const nodemailer = require('nodemailer');

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

app.get("/student_recommendation/:univ_name", (req, res) => {
  let sql = `SELECT Q1, Q2, Q3, Q4, Q5, univ_lon, univ_lat, w1, w2 ,w3 ,w4, w5, T_set  FROM diy_reco_history GROUP BY T_set HAVING Q1 LIKE '%${req.params.univ_name}%'  ORDER BY COUNT(T_set) DESC LIMIT 1`;

  connection.query(sql, (err, rows, fields) => {
    res.send(rows);
    console.log(err);
  });
});

//회원가입라우터

app.post("/signup", (req, res) => {
  bcrypt.genSalt(10, (err, salt) => {
    bcrypt.hash(req.body.user_pwd, salt, (err, hash) => {
      let sql = `INSERT INTO user (user_id, user_pwd, user_email, auth) values('${req.body.user_id}','${hash}', '${req.body.user_email}', '${req.body.authNum}')`;
      connection.query(sql, (err, rows, fields) => {
        //중복검사
        if (err && err.errno === 1062) {
          return res.json({ signupSuccess: false });
        }
        return res.json({ signupSuccess: true });
      });
    });
  });
});

app.post("/signin", (req, res) => {
  let sql = "SELECT * FROM user WHERE user_id = ? and is_validated = 1";
  connection.query(sql, req.body.user_id, (err, user, fields) => {
    if (err) return res.json(err);
    if (user.length === 0)
      return res.json({
        loginSuccess: false,
        message:
          "ID에 해당하는 유저가 없거나 인증이 완료되지 않은 아이디입니다.",
      });
    const isSame = bcrypt.compareSync(req.body.user_pwd, user[0].user_pwd);
    if (isSame) {
      // 로그인 성공 토큰 생성 추후 config로 암호화 필요
      let token = jwt.sign(user[0].user_id, "secretToken");
      res.cookie("user", token).status(200).json({
        loginSuccess: true,
        userId: user[0].user_id,
      });
    } else {
      return res.json({
        loginSuccess: false,
        message: "비밀번호가 틀렸습니다",
      });
    }
  });
});

//이메일 전송 api
app.post("/sendEmail", async (req, res) => {
  let authNum = req.body.authNum;
  let emailTemplete;
  ejs.renderFile(
    appDir + "/template/authMail.ejs",
    { authCode: authNum },
    function (err, data) {
      if (err) {
        console.log(err);
      }
      emailTemplete = data;
    }
  );

  let transporter = nodemailer.createTransport({
    service: "gmail",
    host: "smtp.gmail.com",
    port: 587,
    secure: false,
    auth: {
      user: conf.emailId,
      pass: conf.emailPwd,
    },
  });

  let mailOptions = await transporter.sendMail({
    from: `저기어때.`,
    to: req.body.user_email,
    subject: "저기어때. 회원가입을 위한 인증번호를 입력해주세요.",
    html: emailTemplete,
  });

  transporter.sendMail(mailOptions, function (error, info) {
    if (error) {
      console.log(error);
    }
    console.log("Finish sending email : " + info.response);
    res.send(authNum);
    transporter.close();
  });
});

//이메일 인증번호 인증 api
app.post("/validate", (req, res) => {
  let sql = `UPDATE user SET is_validated = 1, auth = "" WHERE auth = '${req.body.authNum}'`;

  connection.query(sql, (err, rows, fields) => {
    if (err) {
      return res.json({
        validateSuccess: false,
        message: "인증번호가 맞지 않습니다.",
      });
    }
    return res.json({ validateSuccess: true, message: "인증되었습니다." });
  });
});

app.listen(port, () =>
  console.log(`Example app listening on port 
${port}!`)
);
