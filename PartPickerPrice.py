from urllib.request import urlopen as uOpen
from urllib.request import Request as uReq
from bs4 import BeautifulSoup as soup
import datetime
from re import sub
from decimal import Decimal
import os

filename = "PCBuildPrices.csv"
try:
	f = open(filename, "r")
	lines = f.readlines()
	arg = lines[1].split(",")
	url = arg[0] 
	f.close()
except:
	print("Type in PC Part Picker URL you which to price track:")
	url = input()
	f = open(filename, "w")
	headers = "URL, Date_Time, PC_Price, ChangeInPrice\n"
	f.write(headers)

now = datetime.datetime.now()

my_url = url
hdr = {'User-Agent': 'Mozilla/5.0'}
#opening Client
try:
	req = uReq(my_url, headers=hdr)	
	uClient	 = uOpen(req)
	page_html = uClient.read()
	uClient.close()
except:
	f.close()
	print("Could not Open URL... Try a again with different url")
	os.remove(filename)
	quit()

#parses the html page
page_soup = soup(page_html,	"html.parser")
#Gets the current Price of the PC Build
Prices = page_soup.findAll("tr",{"class":"total-price part-list-totals"})
price = Prices[0]
buildprice = '"' + price.find("td",{"class":"tr nowrap"}).text + '"'
print("Current PC Build Costs: " + buildprice)
#Opens PriceFile 
try:
	f = open(filename, "r")
	lines = f.readlines()	
	#Obtains last Line from file
	totalength = len(lines)
	if len(lines) >= 2:
		Lastline = totalength - 1
		arg = lines[Lastline].split(",")
		#obtains Last cost and Compares
		LastCost= arg[2] 	
		PreviousCost = Decimal(sub(r'[^\d.]', "", LastCost))
		NewCost = Decimal(sub(r'[^\d.]', "", buildprice))
		Change = NewCost - PreviousCost
		f.close()
		f = open(filename, "a")
		f.write( my_url   + ", " + now.strftime("%c") + "," + price.find("td",{"class":"tr nowrap"}).text + "," + str(Change) + "\n")
		print("The change in Price was: " + str(Change))

	else:
		f.close()
		f = open(filename, "a")
		print("There were no Previous Costs recorded to compare against")
		f.write( my_url   + ", " + now.strftime("%c") + "," + price.find("td",{"class":"tr nowrap"}).text + "," + "0" + "\n")
	
except:
	print("Cannot Find file...")
	exit()

