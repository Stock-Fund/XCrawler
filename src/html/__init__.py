from bs4 import BeautifulSoup
from urllib.parse import urljoin
import requests
from io import BytesIO
import pytesseract
from PIL import Image

from src.html.stockutils import getStockTimeUrl, getStockSuffix
from src.html.mainboardcrawler import getSHBoard, get_Data_FromSoup
from src.html.stocktimecrawler import getStocksTime
from src.html.stockcustomcrawler import getStockData_datareader
from src.html.stockAllcrawler import getAllStock
