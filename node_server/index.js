const express = require('express')
const ini = require('ini')
const fs = require('fs')
const path = require('path')
const bodyParser = require('body-parser')
const { connectDB } = require('./configuration/databaseConnection')

const config = ini.parse(
  fs.readFileSync(path.join(__dirname, '../config.ini'), 'utf-8'),
)

connectDB(config.DATABASE.CONNECTION_STRING).then(function (
  wasConnectionEstablished,
) {
  if (wasConnectionEstablished) {
    // end

    const app = express()
    app.use(express.json())
    app.use(bodyParser.urlencoded({ extended: true }))

    try {
      console.log('Launching Routes...')
      console.log('All routes launched successfully.')
    } catch (error) {
      console.log(error)
      console.log('Something went wrong while initializing routes.')
    }

    app.listen(config.SERVER.PORT, () => {
      console.log(
        `FindMuck server is running at PORT : ${config.SERVER.PORT}\n`,
      )
    })
  } else {
    console.log(
      'Terminating server as connection with database was not established.',
    )
    process.exit(1)
  }
})
