const express = require('express')
const router = express.Router()
const { check, validationResult } = require('express-validator')
const REPORT = require('../../models/REPORT')
const { v4: uuidv4 } = require('uuid')
router.post(
  '/',
  [
    check('userFullName', 'Please include your name.').isLength({
      min: 3,
      max: 50,
    }),
    check('userEmail', 'Please enter a valid email.').notEmpty().isEmail(),
    check('userReportType', 'Please select a report type.').notEmpty(),
    check(
      'userDescription',
      'Please include the description of minumum 10 and maximum 500 length.',
    ).isLength({
      min: 10,
      max: 500,
    }),
  ],
  async (req, res) => {
    try {
      const errors = validationResult(req)
      if (!errors.isEmpty()) {
        res.status(400).json({
          success: false,
          status: 'Missing parameters, Please include all the details.',
          errors: errors.array(),
          timestamp: Date.now(),
        })
      } else {
        const {
          userFullName,
          userEmail,
          userReportType,
          userDescription,
        } = req.body
        MY_REPORT = REPORT({
          reportId: uuidv4(),
          userFullName: userFullName,
          userReportType: userReportType,
          userEmail: userEmail,
          userDescription: userDescription,
        })
        await MY_REPORT.save()
        res.status(200).json({
          success: true,
          status: 'Report has been noted successfully.',
          timestamp: Date.now(),
        })
      }
    } catch (error) {
      console.log(
        `[sendFeedback] Something went wrong at our end, Please try again, ERROR : ${error}`,
      )
      res.status(500).json({
        success: false,
        status:
          '[Server Error] Something went wrong at our end, Please try again later.',
        timestamp: Date.now(),
      })
    }
  },
)

module.exports = router
