// todo crawler logic code
// import { argv } from 'process';
const { argv } = require('process');
// import { argv } from 'process';
const { open } = require('fs/promises');
// import { argv } from 'process';
// import { open } from 'fs/promises';

// JPEG (jpg)，文件头：FFD8FF
// PNG (png)，文件头：89504E47
// GIF (gif)，文件头：47494638

const JPG_HEADER = [0xFF, 0xD9];
const PNG_HEADER = [0x89, 0x50];
const GIF_HEADER = [0x47, 0x49];

let readFile;
let writeFile;
let fileTypeObj;

function xorOpeartion(fileTypeArr = [], fileHeaderBuffer = []) {
    const fileCode = fileTypeArr[0] ^ fileHeaderBuffer[0];
    let returnValue = {
        isTrue: false,
        fileCode: null,
    }

    if (fileCode ^ fileHeaderBuffer[1] === fileTypeArr[1]) {
        returnValue.isTrue = true;
        returnValue.fileCode = fileCode;
    }

    return returnValue;
}

function getFileType(fileHeaderBuffer) {
    const fileTypeArr = [
        { type: 'jpg', value: JPG_HEADER },
        { type: 'png', value: PNG_HEADER },
        { type: 'gif', value: GIF_HEADER },
    ];
    let returnValue = {
        isTrue: false,
        fileCode: null,
        fileType: null,
    };
    for (let item of fileTypeArr) {
        returnValue = { ...returnValue, ...xorOpeartion(item.value, fileHeaderBuffer) };
        if (returnValue.isTrue) {
            returnValue.fileType = item.type;
            break;
        }
    }
    return returnValue;
}

// 将原先的代码包在顶层的 async 函数中
async function main() {
    try {

        readFile = await open(argv[2], 'r')

        let fileHeaderBuffer = Buffer.alloc(2);
        await readFile.read({
            buffer: fileHeaderBuffer,
        });
        fileTypeObj = getFileType(fileHeaderBuffer);
        if (!fileTypeObj.isTrue) {
            // 即无匹配文件
            throw new Error('不属于jpg, png, gif文件, 解码失败');
        }

        writeFile = await open(`${argv[2]}.${fileTypeObj.fileType}`, 'w')

        // 解码文件
        const readStream = readFile.createReadStream({
            start: 0,
        });
        const writeStream = writeFile.createWriteStream();
        readStream.on('data', (chunk) => {
            let isOk = true;
            let finalData = [];
            for (let dataEachItem of chunk) {
                finalData.push(dataEachItem ^ fileTypeObj.fileCode);
            }

            isOk = writeStream.write(Buffer.from(finalData));

            if (!isOk) {
                readStream.pause();
                writeStream.once('drain', () => {
                    readStream.resume();
                });
            }

            console.log(`Received ${chunk.length} bytes of data.`);
        });

        readStream.on('end', () => {
            console.log('End');
            writeStream.end();
        })
    } catch (error) {
        console.log(`Usage: node ${argv[1]} <input filename>`);
        console.log(error);
    }
}

main();