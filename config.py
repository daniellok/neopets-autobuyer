# Config File

'''
Enter your username and password here. Remember to include the quotation
marks, otherwise Python won't recognize it as a string!
'''
username = 'username'
password = 'password'

'''
Edit these settings to alter the lower and upper bounds for the refresh rate
(in milliseconds)
Recommended: 3000-4000 (3-4 seconds)
'''
refresh_rate_lo = 3000
refresh_rate_hi = 4000

'''
Edit these settings (units are in milliseconds) to determine how quickly you 
buy the item.

prehaggle: this is the duration the program will wait before clicking on the 
item in the shop. if you were a real human restocking, you'd take a bit of 
time to recognize that the shop has restocked, and even more time to scroll 
through the items and find a profitable one. I recommend setting this to at 
least 500 (0.5 seconds), given that the average human's visual reaction time 
is 0.25s.

ocr: this is the duration the program will wait before submitting the haggle
and clicking on the neopet in the captcha. A safe setting here would probably 
be something like 500 as well.

Personally, I'm able to get away with using a very low setting (~50), because 
I live far away from the US and the lag time makes up for it (my buy times 
range from 2.9s-7s). However, if you live in the US, buying an item in around 
1 second is probably suspicious.
'''
prehaggle = 500
ocr = 500

'''
Edit this to change how long the autobuyer sessions last (in seconds). This 
should vary based on what your refresh times are to prevent getting restock 
banned.

If you're refreshing once every 3-4 seconds, this should probably be somewhere 
around 10-15 minutes (600-900 seconds), with a 20-30 minute break.
'''
session_duration_lo = 600
session_duration_hi = 900

'''
Edit this to change how long the breaks are between autobuying sessions (in 
seconds). A good rule of thumb is to wait double the time you were autobuying 
for.

For example, if you were autobuying for 15 minutes, take a 30 minute break 
between sessions.
'''
break_duration_lo = 1200
break_duration_hi = 1800

'''
If you'd like, change this variable to include a proxy. If not, just leave it 
as an empty dictionary ({}). The format is like this:

proxy = {'http':'http://<ip address>:<port>'}

e.g.
proxy = {'http':'http://23.253.83.220:80'}

You can find a bunch of these by just Googling 'free proxy list'
'''
proxy = {}

'''
Enter your browser's user agent header here (once again, remember the 
quotation marks!). This is important so that it looks like you're using a 
browser to interact with the site. To find out yours, visit this website:

http://www.whatsmyua.info/

or, just google 'what is my user agent header'

For more information, see the Wikipedia page:

https://en.wikipedia.org/wiki/User_agent
'''
useragent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'

''' 
A dictionary of shops (you can add to this if you want, the keys are the shop 
IDs, and the values are nicknames for the shops). The defaults are the shops I 
visit most often.

Remember to separate dictionary entries with commas!
'''
shoplist = {1:'food',
            2:'magic',
            3:'toys',
            7:'books',
            9:'battle magic',
            10:'defense magic',
            20:'tropical food',
            36:'ice crystals',
            48:'usukis',
            58:'stamps',
            73:'kayla\'s',
            98:'plushies'}



