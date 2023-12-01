from bs4 import BeautifulSoup
from urllib.parse import urljoin
import requests
from io import BytesIO
import pytesseract
from PIL import Image

from src.html.mainboardcrawler import cycleSHBoard
from src.html.stocktimecrawler import cycleStocksTime
from src.html.stockcustomcrawler import getStockData_datareader

# import src.html.eastmoney
# import src.html.sinafinance