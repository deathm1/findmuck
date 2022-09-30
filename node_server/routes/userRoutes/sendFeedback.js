const express = require("express");
const router = express.Router();

router.get("/", async (req, res) => {
  try {
    res.status(200).json({
      success: true,
      status: "Success",
    });
  } catch (error) {
    console.log(`Something went wrong, ERROR : ${error}`);
  }
});

module.exports = router;
