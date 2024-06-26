from bs4 import BeautifulSoup
from urllib.parse import urljoin
import requests
from io import BytesIO
import pytesseract
from PIL import Image

from src.html.stockutils import (
    getStockTimeUrl,
    getStockSuffix,
    get_StockInflow_OutflowUrl,
    get_Stock_chipsUrl,
)
from src.html.mainboardcrawler import getSHBoard, get_Data_FromSoup
from src.html.stocktimecrawler import (
    getStocksTime,
    checkAllTimeStock,
    getStockInflowOutflow,
    getStockAllInflowOutflow,
    getStockChips,
)
from src.html.stockcustomcrawler import getStockData_datareader, showStockData,getStockData_efinance
from src.html.stockAllcrawler import getAllStock, checkAllStock
from src.html.securities_margin_trading import getmargindata
