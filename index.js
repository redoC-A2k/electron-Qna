const { remote } = require('electron');
const path = require('path');
const url = require('url');
const dialog = remote.dialog;
const go= document.getElementById('go');
const videoInputField = document.getElementById('inputfield'); 
const win = remote.getCurrentWindow();
let ytlink ;
let gopromise ;
//ytvideo 
try {
    //Go
    gopromise = new Promise(function(resolve,reject){
        go.addEventListener('click', function () {
            ytlink = videoInputField.value ;
            win.loadURL(url.format({
                pathname: path.join(__dirname, './video/index.html'),
                protocol: 'file',
                slashes: true
            }));
        });
    })
} catch (error) {
    console.log('error occured ' + error);
}
gopromise.then(function () {
    localStorage.setItem('ytlink', ytlink)
})