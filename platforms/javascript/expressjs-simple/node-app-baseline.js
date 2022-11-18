const express = require("express");
const dataLogger = require("./custom-data-logger")
const app = express();
const port = process.env.SENTRY_PORT_BACKEND || 8081;

const APP_NAME = "node-app-baseline";
console.log(`Starting app ${APP_NAME}`);

dataLogger.writeCustomData([
    {  name:"baseTest", value:"true"},
    {  name:"displayName", value:"Base"}
])

app.get("/", (req, res) => {
  res.send("Hello Anton & Radu!");
});

app.listen(port, () => {
  console.log(`${APP_NAME} listening on port ${port}`);
});
