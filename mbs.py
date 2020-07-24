import requests
from bs4 import BeautifulSoup
import pickle
from notify_run import Notify

with open('macbooks', 'rb') as inFile:
    allItemsOld = pickle.load(inFile)

mbPotential = []

### macbook pro scrape

mbp = requests.get('https://www.ebay.co.uk/sch/i.html?_from=R40&_nkw=macbook+pro+2016&_sacat=0&LH_BIN=1&_sop=15&_ipg=200&rt=nc&LH_PrefLoc=1').text

mbpSoup = BeautifulSoup(mbp, 'html.parser')

mbpTable = mbpSoup.find('ul', class_ = 'srp-results srp-list clearfix')

mbpItemsAll = mbpTable.find_all('li')

mbpItemsValid = []

for item in mbpItemsAll:
        
    if item.find('span', class_ = 's-item__price') != None:
        mbpItemsValid.append(item)

for item in mbpItemsValid:

    strippedItem = item.find('span', class_ = 's-item__price').text.split(' ', 1)[0].lstrip('£').replace(',', '')

    if float(strippedItem) < 625:
        mbPotential.append(item)

### macbook air scrape

mba = requests.get('https://www.ebay.co.uk/sch/i.html?_from=R40&_trksid=p2334524.m570.l1313.TR11.TRC1.A0.H0.Xmacbook+air+2018.TRS0&_nkw=macbook+air+2018&_sacat=0&LH_TitleDesc=0&LH_PrefLoc=1&_sop=15&_osacat=0&_odkw=macbook+pro+2016&LH_BIN=1&rt=nc&_ipg=200').text

mbaSoup = BeautifulSoup(mba, 'html.parser')

mbaTable = mbaSoup.find('ul', class_ = 'srp-results srp-list clearfix')

mbaItemsAll = mbaTable.find_all('li')

mbaItemsValid = []

for item in mbaItemsAll:
        
    if item.find('span', class_ = 's-item__price') != None:
        mbaItemsValid.append(item)


for item in mbaItemsValid:
    
    strippedItem = item.find('span', class_ = 's-item__price').text.split(' ', 1)[0].lstrip('£').replace(',', '')

    if float(strippedItem) < 580:
        mbPotential.append(item)

# all

allItems = []

for item in mbPotential:

    try:
        itemName = item.find(class_ = 's-item__title').text
    except:
        itemName = 'n/a'

    try:
        itemPrice = item.find('span', class_ = 's-item__price').text
    except:
        itemPrice = 'n/a'

    try:
        itemLink = item.find(class_ = 's-item__link')['href']
    except:
        itemLink = 'n/a'

    try:
        itemShippingPrice = item.find('span', class_ = 's-item__shipping s-item__logisticsCost').text.lstrip('+')
    except:
        itemShippingPrice = 'n/a'
    
    itemInfo = (f'''
    {itemName}
    {itemPrice} + {itemShippingPrice}
    {itemLink}
    ''')

    allItems.append(itemInfo)

newItems = []

for item in allItems:
    if item not in allItemsOld:
        newItems.append(item)

notify = Notify()

for item in newItems:
    print(item)
    notify.send(item)

with open('macbooks', 'wb') as outFile:
    pickle.dump(allItems, outFile)
