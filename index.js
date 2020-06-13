const { remote } = require('electron');
const path = require('path');
const url = require('url');
const dialog = remote.dialog;
const go = document.getElementById('go');
const videoInputField = document.getElementById('inputfield');
const win = remote.getCurrentWindow();
const spawn = require('child_process').spawn;
let ytlink;
let gopromise;
let ytpromise;
//ytvideo 
try {
    //Go
    gopromise = new Promise(function (resolve, reject) {
        go.addEventListener('click', function (event) {
            ytlink = videoInputField.value;

            resolve();
        });
    });
} catch (error) {
    console.log('error occured ' + error);
}

gopromise.then(function () {
    ytpromise = new Promise(function (resolve, reject) {
        const pythonProcess = spawn('python', ['./ytToEmbed.py', ytlink])
        pythonProcess.stdout.on('data', (data) => {
            ytlink = data.toString()
            localStorage.clear()
            localStorage.setItem('ytlink', ytlink)
            console.log('ytlink is ' + ytlink);
            resolve();
        });
    });
    ytpromise.then(function () {
        win.loadURL(url.format({
            pathname: path.join(__dirname, './video/index.html'),
            protocol: 'file',
            slashes: true
        }));
    })
});

