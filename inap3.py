import requests
from bs4 import BeautifulSoup
import difflib
import time
from datetime import datetime

TOKEN = "6975578482:AAFILENq--Ooy0YbYoRNn2tpk9Hpk0bADok"
chat_id = "309941493"

# target U
link = "https://sede.inap.gob.es/tail-oep-2020-2021-2022"
# act like a browser
headers = {
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'}

PrevVersion = ""
FirstRun = True
while True:

	# download the page
	response = requests.get(link, headers=headers)
	# parse the downloaded homepage
	soup = BeautifulSoup(response.text, "lxml")

	# remove all scripts and styles
	for script in soup(["script", "style"]):
		script.extract()
	soup = soup.get_text()
	# compare the page text to the previous version
	if PrevVersion != soup:
		# on the first run - just memorize the page
		if FirstRun == True:
			PrevVersion = soup
			FirstRun = False
			# print("Start Monitoring " + link + "" + str(datetime.now()))

			message = "Start Monitoring"
			url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={message}"
			print(requests.get(url).json())  # this sends the message

		else:
			# print("Changes detected at: " + str(datetime.now()))

			message = "Cambios en la web detectados!!!"
			url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={message}"
			print(requests.get(url).json())  # this sends the message

			OldPage = PrevVersion.splitlines()
			NewPage = soup.splitlines()
			# compare versions and highlight changes using difflib
			d = difflib.Differ()
			diff = d.compare(OldPage, NewPage)
			out_text = "\n".join([ll.rstrip() for ll in '\n'.join(diff).splitlines() if ll.strip()])
			# print(out_text)
			OldPage = NewPage
			# print ('\n'.join(diff))
			PrevVersion = soup
	else:
		#print("No Changes " + str(datetime.now()))

		message = "No Changes"
		url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={message}"
		print(requests.get(url).json())  # this sends the message
	time.sleep(120)
	continue