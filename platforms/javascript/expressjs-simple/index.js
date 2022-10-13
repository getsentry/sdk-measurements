const express = require('express')
const app = express()
const port = process.env.SENTRY_PORT_BACKEND || 8081

process.once('SIGTERM', function () {
  console.log('got SIGTERM');
  process.exit(0);
});

app.get('/', (req, res) => {
  res.send('Hello Anton & Radu!')
})

app.listen(port, () => {
  console.log(`Example app listening on port ${port}`)
})
