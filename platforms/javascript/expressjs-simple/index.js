const express = require('express')
const app = express()
const port = process.env.SENTRY_PORT_BACKEND

app.get('/', (req, res) => {
  res.send('Hello Anton & Radu!')
})

app.listen(port, () => {
  console.log(`Example app listening on port ${port}`)
})
