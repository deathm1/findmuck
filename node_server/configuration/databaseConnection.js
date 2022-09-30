const mongoose = require('mongoose')

const connectDB = async (connstr) => {
  try {
    await mongoose.connect(connstr)
    console.log('Connection with database is extablished.')
    return true
  } catch (err) {
    console.log(
      `Connection with database was not established. Error Message => [${err.message}]`,
    )
    return false
  }
}
module.exports = { connectDB }
