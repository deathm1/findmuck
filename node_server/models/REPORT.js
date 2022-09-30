const mongoose = require("mongoose");

const reportSchema = new mongoose.Schema({
  reportId: {
    type: String,
    required: true,
  },
  userFullName: {
    type: String,
    required: true,
  },
  userEmail: {
    type: String,
    required: true,
  },
  userReportType: {
    type: String,
    required: true,
  },
  userDescription: {
    type: String,
    required: true,
  },
  timeStamp: {
    type: Date,
    default: Date.now,
  },
});

module.exports = mongoose.model("reports", reportSchema);
