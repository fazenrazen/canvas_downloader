# Canvas File Downloader

*This only works right now if you are just from umich, you can EDIT the canvas link on the top of the python script "canvas_downloader" for your school and it will work*

Description: This script allows you to select which classes on canvas you would like to download the files from. This script includes ALL the courses at that particular dashboard that are available. 

Clone the repo or download the folder:
```
git clone git@github.com:fazenrazen/canvas_downloader.git
cd canvas_downloader
```

Setup 
In the terminal we will do these commands
For mac users 
```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
For Windows Command Prompt
```
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

Login to your canvas online and follow the steps below. 

Create a API Key by going from:
1. Accounts settings in Canvas
![alt text](image.png)
2. Create a new access token under the "Approved Integrations"
![alt text](image-1.png)
3. Write in "My canvas downloader" for the purpose blank and create a random expiration date and time. SAVE the key generation on your favorite notes app (since it is shown only ONCE) and enter the information into the python code below WITH the quotes!

The API Key looks something like this:
"1700~L9MPJL2342BXyeKxxMJJG3Fu4chCn24QaasdfamMNTChJNmU44ChzGEeashdf4GMT"
 
![alt text](image-2.png)

After you edit these two fields in the code:
```
API_URL = "https://umich.instructure.com"  # Replace with your Canvas URL
API_TOKEN = "Enter your key here!"
```
You should be set to run the code!
``` 
python3 canvas_downloader.py 
```


