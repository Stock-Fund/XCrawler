import pytesseract
from PIL import Image

# 打开图像文件
image = Image.open('Assets/logo.png')

# 设置 pytesseract 参数
custom_config = r'--psm 6 --oem 2'

# 将图像转换为灰度图像
image = image.convert('L')

# 使用pytesseract进行文本识别
text = pytesseract.image_to_string(image,lang='chi_sim', config=custom_config)

# 打印识别结果
print("result:"+text)