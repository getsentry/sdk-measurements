process.once("SIGTERM", function () {
  console.log("got SIGTERM, exiting...");
  // Exit code is 0 to make Argo runtime happy
  process.exit(0);
});

if (process.env.APP_ENABLE_INSTRUMENTATION) {
  require("./node-app-test");
} else {
  require("./node-app-baseline");
}
