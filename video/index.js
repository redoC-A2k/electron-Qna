const videoPath = localStorage.video;
const subPath = localStorage.sub;
const { remote } = require('electron');
const url = require('url');
const path = require('path');
const browserWindow = remote.BrowserWindow;
const app = remote.app;
const win = remote.getCurrentWindow();
let window ;
let PlayrSub = document.getElementById('playrSub');
let PlayrPath = document.getElementById('playrPath');
const playr = document.getElementById('plyr-video');
const quebtn = document.getElementById('que');
PlayrPath.setAttribute('src', videoPath);
PlayrSub.setAttribute('src', subPath);
playr.addEventListener('loadedmetadata', function (event) {
    let width = playr.videoWidth;
    let height = playr.videoHeight;
    console.log(width + ' width and height' + height)
})

function createWindow() {
    console.log('browser window from rendere');
    window = new browserWindow({
        height: 220,
        width: 800,
        resizable: true,
        webPreferences: {
            enableRemoteModule: true,
            nodeIntegration: true
        }
    });
    window.loadURL(url.format({
        pathname: path.join(__dirname, './que.html'),
        protocol: 'file',
        slashes: true
    }));

    window.on('closed', () => {
        window = null;
        console.log("win closed");
    });
}

quebtn.addEventListener('click', function (event) {
    createWindow();
})