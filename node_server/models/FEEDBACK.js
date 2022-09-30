const mongoose = require("mongoose");

const feedbackSchema = new mongoose.Schema({
  feedbackId: {
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
  userDescription: {
    type: String,
    required: true,
  },
  timeStamp: {
    type: Date,
    default: Date.now,
  },
});

module.exports = mongoose.model("feedback", feedbackSchema);
