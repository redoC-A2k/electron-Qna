const ytlink = localStorage.ytlink;
console.log(ytlink);
const iframe = document.getElementById('iframe');
const { remote } = require('electron');
const url = require('url');
const path = require('path');
const browserWindow = remote.BrowserWindow;
const app = remote.app;
const win = remote.getCurrentWindow();
let window ;
const quebtn = document.getElementById('que');
iframe.setAttribute('src',ytlink);
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