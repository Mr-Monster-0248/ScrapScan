import requests
import shutil

myURL = "https://www.scan-vf.co/"

search = input("Scan to find: ")
searchURL = myURL + "search?query=" + search
print("quering", searchURL)
resp = requests.get(searchURL)

if(resp.status_code == 200):
    data = resp.json()
    #print(data)
    for item in data:
        for i in data[item]:
            print(i['value'])
            

else:
    print("Error request:" , resp.status_code)



# if(resp.status_code == 200):
#     local_file = open('test.jpg', 'wb')
#     resp.raw.decode_content = True
#     shutil.copyfileobj(resp.raw, local_file)
# else:
#     print("Error request:" , resp.status_code)

del resp
