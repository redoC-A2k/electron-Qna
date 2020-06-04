const fs = require('fs');
const path = require('path');
const url = require('url');
const submitbtn = document.getElementById('submit');
const question = document.getElementById('question');
const pathname = path.join(__dirname, 'question.txt');
console.log(question.value);
console.log('working fine');
let submitbtnpromise;
let questionContent;
submitbtn.addEventListener('click', function (event) {
    console.log('button clicked')
    questionContent = question.value;
    fs.writeFile(pathname, questionContent, function (err) {
        if (err)
            console.log(err);
        console.log('file was saved successfully');
    })
});  