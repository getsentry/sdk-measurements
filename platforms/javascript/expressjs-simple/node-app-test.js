const express = require("express");
const app = express();
const Sentry = require("@sentry/node");
const dataLogger = require("./custom-data-logger");

const port = process.env.SENTRY_PORT_BACKEND || 8081;

const APP_NAME = "node-app-test";
console.log(`Starting app ${APP_NAME}`);

// dataLogger.writeCustomData([
//   {  name:"baseTest", value:"false"},
//   {  name:"displayName", value:"With Sentry"}
// ])


Sentry.init({ dsn: process.env.SENTRY_DSN });

console.log({ sentryDSN: process.env.SENTRY_DSN });

app.use(Sentry.Handlers.requestHandler());

// Throw an error randomly
app.get("/", function mainHandler(req, res) {
  const MAX_RANDOM_NUMBER = 10;
  const randomNumber = Math.floor(Math.random() * MAX_RANDOM_NUMBER);

  if (randomNumber === 5) {
    throw new Error("My first Sentry error!");
  }

  res.status(200).json({ ping: "pong" });
});

app.use(Sentry.Handlers.errorHandler());

app.listen(port, () => {
  console.log(`${APP_NAME} listening on port ${port}`);
});
