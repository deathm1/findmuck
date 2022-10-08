const express = require("express");
const router = express.Router();
const yaml = require("js-yaml");
const fs = require("fs");
const path = require("path");
const { check, validationResult } = require("express-validator");
const Queue = require("bull");

const { v4: uuidv4 } = require("uuid");
const my_victim_queue = new Queue("my_victim");

router.post(
  "/",
  [
    check("countryCode", "Please include victim's country code.").isLength({
      min: 1,
      max: 3,
    }),
    check("phoneNumber", "Please include victim's phone number.").isLength({
      min: 3,
      max: 50,
    }),
    check("delay", "Please enter delay in seconds.").isInt({
      min: 3,
      max: 15,
    }),
    check("amount", "Please specify how many messages are to be sent.").isInt({
      min: 10,
      max: 200,
    }),
  ],
  async (req, res) => {
    try {
      const errors = validationResult(req);
      if (!errors.isEmpty()) {
        res.status(400).json({
          success: false,
          status: "Missing parameters, Please include all the details.",
          errors: errors.array(),
          timestamp: Date.now(),
        });
      } else {
        const { countryCode, phoneNumber, delay, amount } = req.body;
        const my_api_string = fs
          .readFileSync(
            path.join(__dirname, "../../configuration/services.yaml"),
            "utf8"
          )
          .replaceAll("{target}", phoneNumber)
          .replaceAll("{cc}", countryCode);
        const doc = yaml.load(my_api_string);

        const indiaServices = doc["providers"]["91"];
        const multiPurpose = doc["providers"]["multi"];

        // indiaServices.forEach((element) => {
        //   console.log(element);
        // });
        my_victim_queue.resume();
        console.log(indiaServices[0]["method"]);
        res.status(200).json({
          success: true,
        });
      }
    } catch (error) {
      console.log(
        `[attackVictim] Something went wrong at our end, Please try again, ERROR : ${error}`
      );
      res.status(500).json({
        success: false,
        status:
          "[Server Error] Something went wrong at our end, Please try again later.",
        timestamp: Date.now(),
      });
    }
  }
);

my_victim_queue.process(function (str) {
  console.log("str");
  throw new Error("some unexpected error");
});

module.exports = router;
