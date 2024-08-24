const logger = require("./logger");
const Config = require("config");
require("express-async-errors");
const { PythonShell } = require("python-shell");

const express = require("express");

const app = express();

app.use(express.json());

app.use((req, res, next) => {
  const origin = Config.get("origin");
  res.setHeader("Access-Control-Allow-Origin", origin);
  res.setHeader("Access-Control-Allow-Methods", "POST");
  res.setHeader("Access-Control-Allow-Headers", "Content-Type");

  next();
});

app.use("/health", async (req, res) => {
  res.json("OK");
});

app.post("/", async (req, res) => {
  const requestData = req.body;

  //options for running python script
  const options = {
    mode: "text",
    pythonOptions: ["-u"], // get print results in real-time
    args: JSON.stringify(requestData),
  };

  // getting what python file prints and return it to the client
  try {
    const result = await PythonShell.run("final.py", options);
    console.log(result[0]);
    res.json(JSON.parse(result[0]));
  } catch (err) {
    logger.error(err);
    res.status(500).send("Internal Server Error. Python Faild to Execute");
  }
});

app.use((err, req, res, next) => {
  logger.error(err);

  res.status(500).send("Unexpected Error Occured.");
});

const port = Config.get("port") || 8080;
app.listen(port, () => logger.info(`start listening at port ${port}`));
