const express = require('express')
const app = express()
const port = process.env.SENTRY_PORT_BACKEND || 8081

process.once('SIGTERM', function () {
  console.log('got SIGTERM, exiting...');
  // Exit code is 0 to make Argo runtime happy
  process.exit(0);
});

app.get('/', (req, res) => {
  res.send('Hello Anton & Radu!')
})

app.listen(port, () => {
  console.log(`Example app listening on port ${port}`)
})
