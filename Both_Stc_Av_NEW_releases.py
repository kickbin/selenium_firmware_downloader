# how to setup
#####################
# open terminal, # cd /Users/chrischeng/PycharmProjects/first_selenium_proj
# pipenv install selenium
#
# How to activate
#####################
# source .virtualenvs/first_selenium_proj/bin/activate
# to deactivate, open terminal,  # deactivate


from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time

#ver = input("Please enter version number e.g - 4.86 or 4.90\n")
#ver = ver.strip("\n")
USERNAME = "user@user.com"
PASSWORD = "pass"
ver = str("5.30")
CHROME_DRIVER_PATH = "D:\\Python363\\projects\\first_selenium_proj\\browsers\\chromedriver.exe"
## windows: "D:\\Python363\\projects\\first_selenium_proj\\browsers\\chromedriver.exe"
## mac: "/User/chrischeng/python/chrome.exe"


def createAVDownloads():
	AvDownloads = ([
	'Avalanche Application.exe'.format(ver),
	'l4l7Vm-{}'.format(ver),
	'Avv_{}'.format(ver),
	])

	print(len(AvDownloads), "Av items to download") # print items to download
	i = 0
	for i in AvDownloads:
		print(i)

	return AvDownloads

print("starting browser")
driver = webdriver.Chrome(CHROME_DRIVER_PATH)
driver.set_page_load_timeout(30)
driver.get("https://support.spirent.com")
driver.find_element_by_name("j_id0:xyz:username").send_keys(USERNAME)
driver.find_element_by_name("j_id0:xyz:password").send_keys(PASSWORD)
driver.find_element_by_id('login').click()

wait30 = WebDriverWait(driver, 30) # wait 30 second or until icon-download appears
wait30.until(EC.element_to_be_clickable((By.CLASS_NAME, "icon-downloads")))
driver.find_element_by_class_name("icon-downloads").click()

time.sleep(10)
driver.switch_to.frame(0)   # switch to OuterFrame
driver.switch_to.frame(0)   # switch to InnerFrame

# Make STC / Avalanche option appear by clicking "Please Select Product Line"

def selectcurrentprodline():
	DropMenusLeft = driver.find_elements_by_class_name("PanelClass")
	for i in range(len(DropMenusLeft)):
		w = i + 1
		print("Left Drop Menu Selection {}".format(w), DropMenusLeft[i].text)
	# Select whatever is in the selection 2
	DropMenusLeft[1].click()
	print("clicked", DropMenusLeft[1].text)

### Create a def to find Product line to click. This case is "Spirent TestCenter".

def selectprodline(ProdName):
	readProdLines = driver.find_elements_by_class_name("ui-menu-item")
	dictProdLines = {}
	for i in range(1, len(readProdLines)+1):
		ProdLines = driver.find_element_by_id("ui-id-{}".format(i))
		dictProdLines[ProdLines.text] = i - 1
	print(dictProdLines)
	TargetProd = dictProdLines.get(ProdName)
	readProdLines[TargetProd].click()

# Click ProdLine > Spirent TestCenter

selectcurrentprodline()		# click Current Product line to reveal all product lines
time.sleep(1)
selectprodline("Spirent TestCenter")	# find and click Prod Line
time.sleep(20)

### as of 2021, STC might have subversion
### Need to check subversion of STC
### step 1: selectAllVer
### step 2: check if there is subversion
def selectAllVer():
    buttonAll = driver.find_element_by_css_selector("#maincontentPH_ddlRelease-button")
    buttonAll.click()
    print("Clicked ALL to make other selections available")

def checkSubversion(ver):
	# grab all versions and output into dictionary as global variable

	AllVer = driver.find_elements_by_class_name("ui-menu-item")
	dictAllVer = {}  # create empty dict for loop below
	for i in range(len(AllVer)):
		dictAllVer[AllVer[i].text] = i

	# extract sub version number from dictionary

	for k, v in dictAllVer.items():
		if ver in k and len(k) > 4:  # version number matches "ver" and longer than 4 char e.g 4.85.11
			print(k, v)
			SubVer = k
			SubVerRef = v
			print("Sub version is ", SubVer)
			print("Reference number is ", SubVerRef)
			AllVer[SubVerRef].click()		# click the SubVer button
			return SubVer

		elif ver in k and len(k) == 4:
			print("no subversion number")
			print(k, v)
			Ver = k
			VerRef = v
			print("version is ", Ver)
			print("Reference number is ", VerRef)
			AllVer[VerRef].click()  # click the SubVer button
			return Ver

selectAllVer()
time.sleep(1)
ver = checkSubversion(ver)

## now we have determined the version number, we need to make a list of download items.

def createSTCList(ver):
	STCDownloads = ([
		'spt-c1-x11_{}.'.format(ver),
		'Spirent_TestCenter_LS_{}.'.format(ver),
		'Spirent_TestCenter_{}_CTL3_FW.zip'.format(ver),
		'Spirent_TestCenter_{}_CTL2_FW.zip'.format(ver),
		'Spirent_TestCenter_Virtual_qcow2_{}.'.format(ver),
		'Spirent_TestCenter_Virtual_ESX_{}.'.format(ver),
		'Spirent_TestCenter_Virtual_QEMU_{}.'.format(ver),
		'Spirent TestCenter Application.exe'.format(ver),
		'Spirent TestCenter Documentation.exe'.format(ver),
	])

	print(len(STCDownloads), "STC items to download")  # print items to download
	i = 0
	for i in STCDownloads:
		print(i)

	return STCDownloads

STCDownloads = createSTCList(ver)			### pass in "ver" variable and get the full download list

### Now it has reached the STC download page
### Loop shall make a dictionary of all the links and compare it to SetItemsToDl
### if dictionary entry matches, it will click on the link to start download

def pagescanner(DownloadList):

	dictDlist = {}				# create an empty list for below loop
	for i in range(0,10):		# loop thru each DL link
		try:					# stop operation once list reached end
			print("about to read line", i)
			DL = driver.find_element_by_css_selector("#maincontentPH_dtDownloads_btnDownload1_{}".format(i))
			DLtitle = DL.get_property("title")		# get the name of each DL link
			print("Reading", DLtitle, i)
			for loopItem1 in range(0, len(DownloadList)):
				if DownloadList[loopItem1] in DLtitle:
					DL.click()							# click button if matches
					print("starting download for ", DLtitle)
					removeDownloaded = str(DownloadList[loopItem1])
					DownloadList.remove(removeDownloaded)		# remove downloaded item from DownloadList
					print("going to sleep 7 sec while page jumps")
					time.sleep(7)						# avoid looping while page jumps when DL start
					print("woke")
			if i == 9:			# scans last item in page; check leftover shopping list
				print("DL list is left with", len(DownloadList), "items")
				print("-----------------------------")
				for itemDL in DownloadList:
					print(itemDL)
				print("-----------------------------")
				if len(DownloadList) == 0:  # check if shopping list completed
					print("PageScanner: list finished download, ending function")
					return  # exit function
		except Exception as e:
			print(e)


### Reach page 1, DL items

print("going to sleep for 15 secs")
time.sleep(15)
print("reading page 1")
pagescanner(STCDownloads)

### Go to page 2 to DL items
# driver.find_element_by_css_selector("#maincontentPH_dlPaging_lnkbtnPaging_1").click()
# PageScanner()

def scanotherpages(DownloadList):
	for Page in range(1,10):
		try:
			k = Page + 1
			switchpage = driver.find_element_by_css_selector("#maincontentPH_dlPaging_lnkbtnPaging_{}".format(Page))
			print("switching to page {}".format(k))
			switchpage.click()
			print("now on page{}".format(k))
			time.sleep(10)	# allow time to load page after clicking
			print("starting page scanner")
			pagescanner(DownloadList)
			print("page scanner completed")
			if len(DownloadList) == 0: # check if shopping list completed
			 	print("ScanOtherPages: list finished download, ending function")
			 	return	# exit function
		except:
			print("end of page reached")

scanotherpages(STCDownloads)

#### Start the second part to download Avalanche Items

print("Download Av Items", AvDownloads)
selectcurrentprodline()		# click Current Product line to reveal all product lines
time.sleep(1)
selectprodline("CyberFlood/Avalanche")	# find and click Prod Line
time.sleep(20)
print("reading page 1 of Avalanche")
pagescanner(AvDownloads)
scanotherpages(AvDownloads)
