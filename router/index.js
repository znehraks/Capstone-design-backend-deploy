const express = require("express");
const router = express.Router();
const auth = require("./auth/index.js");
const recommendation = require("./recommendation/index.js");
const history = require("./history/index.js");
const app = express();

//url Routing
router.use("/api/auth", auth);
router.use("/api/recommendation", recommendation);
router.use("/api/history", history);

module.exports = router;
