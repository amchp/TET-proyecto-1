const express = require('express')
const path = require('path')
const cors = require('cors')
const app = express()
const port = 3000

app.use(cors())

app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, '/client.html'));
})

app.listen(port, () => {
  console.log(`Example app listening on port ${port}`)
})