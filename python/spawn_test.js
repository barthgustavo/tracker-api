const child_process = require('child_process');

const python = child_process.spawn('python3', ['./mp-kcf-file.py']);

var dataToSend;
python.stdout.on('data', function (data) {
    console.log('Pipe data from python script ...');
    dataToSend = data.toString();
});

python.on('close', (code) => {
    console.log(`child process close all stdio with code ${code}`);
    console.log(dataToSend);
});