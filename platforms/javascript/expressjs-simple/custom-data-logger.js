// Write custom data to an output file

const fs = require("fs")
const path = '/tmp/custom-data.json'

function writeCustomData(labels) {
    const customData = {
        labels: labels
    }
    const raw = JSON.stringify(customData, null, "  ") + "\n"
    fs.writeFile(path, raw, (err) => {
        if (err) {
            console.log(`Failed to write custom file to ${path} error \n ${err}`)
        } else {
            console.log(`Written to ${path}`)
        }
    })
}

exports.writeCustomData = writeCustomData
