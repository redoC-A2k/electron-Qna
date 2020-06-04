const { remote } = require('electron');
const path = require('path');
const url = require('url');
const dialog = remote.dialog;
const next = document.getElementById('next');
const videoFile = document.getElementById('videoFile');
const subFile = document.getElementById('subFile');
const win = remote.getCurrentWindow();
let subFilePath = 2;
let videoFilePath = 1;
let videopromise;
let subpromise;
//video file 
try {
    let videoFileOptions = {
        title: 'Select video file in mp4 format',
        buttonLabel: 'select',
        filters: [
            { name: 'Movies', extensions: ['mp4'] }
        ],
        properties: ['openFile']
    };
    videopromise = new Promise(function (resolve, reject) {
        videoFile.addEventListener('click', function () {
            videoFilePath = dialog.showOpenDialogSync(win, videoFileOptions);
            const videopath = videoFilePath[0];
            videoFilePath = videopath;
            videoFile.innerHTML = videopath;
            videoFile.style.backgroundColor = "rgba(2, 117, 216 , 0.8)"
            resolve();
        });
    });
    //subtitle file
    let subFileOptions = {
        title: 'Select subtitle file in .vtt format',
        buttonLabel: 'select',
        filters: [
            { name: 'Subtitles', extensions: ['vtt']}
        ],
        properties: ['openFile']
    };

    subpromise = new Promise(function (resolve, reject) {
        subFile.addEventListener('click', function () {
            subFilePath = dialog.showOpenDialogSync(win, subFileOptions);
            const subpath = subFilePath[0];
            subFilePath = subpath;
            subFile.innerHTML = subpath;
            subFile.style.backgroundColor = "rgba(2, 117, 216 , 0.8)"
            resolve();
        });
    });
    //next
    next.addEventListener('click', function () {
        win.loadURL(url.format({
            pathname: path.join(__dirname, './video/index.html'),
            protocol: 'file',
            slashes: true
        }));
    });
} catch (error) {
    console.log('error occured ' + error);
}
videopromise.then(function () {
    localStorage.setItem('video', videoFilePath)
})
subpromise.then(function () {
    localStorage.setItem('sub', subFilePath);
    console.log(subFilePath + 'how are you' + videoFilePath);
})