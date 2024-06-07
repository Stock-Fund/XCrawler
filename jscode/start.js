const fs = require('fs'); // 文件系统模块
const path = require('path'); // 路径模块
const { exec } = require('child_process'); // 执行系统命令模块

const folderPath = './dat'; // 你的文件夹路径，可以根据需要进行修改

// 用 fs.readdir 读取文件夹
fs.readdir(folderPath, (err, files) => {
    if (err) throw err;
    // 遍历文件夹中的所有文件和文件夹
    files.forEach((file) => {
        // 使用 path.join 和 path.extname 获取文件的完整路径和扩展名
        const filePath = path.join(folderPath, file);
        const fileExt = path.extname(filePath);
        // 检查文件的扩展名是否为 .dat
        if (fileExt === '.dat') {
            // 如果是 .dat 文件，那就执行你的命令
            exec(`node ./crawler.js ${filePath}`, (error, stdout, stderr) => {
                if (error) {
                    console.log(`Error: ${error}`);
                    return;
                }
                // 打印命令的输出
                if (stdout) console.log(`Output: ${stdout}`);
                // 打印命令的错误输出
                if (stderr) console.log(`Error Output: ${stderr}`);
            });
        }
    });
});