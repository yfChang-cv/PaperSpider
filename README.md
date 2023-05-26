# PaperSpider
This is a web scraping tool designed to extract academic papers from various conference proceedings.<br>
- At present, papers from **CVPR**/**ICCV**/**WACV** can be crawled.<br>
- *Other conferences work in process.*<br>
- *And multithreading feature is still under development.*<br>


## Install
``` 
git clone https://github.com/yfChang-cv/PaperSpider.git
cd PaperSpider
pip install -r requirements.txt
```

## Usage

if you need proxies, just replace `set_req_old` with `set_req_proxies`.  
if you want to crawl papers from other conferences, simply modify these content:<br>

CVPR2022
```python
head = 'https://openaccess.thecvf.com'
url = "https://openaccess.thecvf.com/CVPR2022?day=all"
filename = 'cvpr2022.csv'
```
ICCV2021
```python
head = 'https://openaccess.thecvf.com'
url = "https://openaccess.thecvf.com/ICCV2021?day=all"
filename = 'iccv2021.csv'
```

## License

[MIT © Richard McRichface.](./LICENSE)
