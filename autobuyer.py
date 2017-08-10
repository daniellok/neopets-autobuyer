# --------- PACKAGES AND STUFF --------- #

import config
import re
import time
import random
import pickle
import os
from io import BytesIO
from PIL import Image
from requests import *

# --------- VARIABLE DECLARATION --------- #

# Initialize random number generator
random.seed()

# Some regular expressions I use to find stuff
shop_item_re = re.compile("</A><B>(.*?)<")
price_re = re.compile("Cost: (.*?) NP")
haggle_url_re = re.compile("\"(haggle.phtml\?.*?)\"")
captcha_re = re.compile("(/captcha_show.phtml\?.*?)\"")
success_re = re.compile("I accept")

# An empty list which will be appended to each time the autobuyer makes a buy
grablist = []

# This is used to log in
login_url = "http://www.neopets.com/login.phtml"

# These are the default browser headers. There should
headers = {'user-agent':config.useragent}

# --------- MAIN FUNCTIONS --------- #

# Print the current time to the console.
def print_time():
  current_time = "%d:%02d:%02d" % ((time.gmtime().tm_hour + 8) % 24,
    time.gmtime().tm_min,time.gmtime().tm_sec)
  print("Current time: %s." % current_time)

'''
Generates an alternating-number haggle to make it seem like you're a human
trying to haggle quickly. For example, if the item is priced at 15,678 NP,
this function returns 15151 as the haggle. 
'''
def offer(num):
  stringrep = str(num).replace(",","") # strip the commas
  length = len(stringrep)
  first = stringrep[0]
  second = stringrep[1] 
  new_offer = "" 
  for i in range(0,length):
    if i % 2 == 0:
      new_offer = new_offer + first
    else:
      new_offer = new_offer + second
  return int(new_offer)

''' 
This function refreshes a given shop, and returns a list of relevant things.
The arguments are:

name (str): name of the account you're refreshing with
url (str): url of the shop you want to refresh
s: request session (from the requests package)
'''
def refresh_shop(url,s):
  print('Refreshing...')
  shop_text = (s.get(url,headers=headers)).text # get the raw html
  # get a list of items
  items = shop_item_re.findall(shop_text)
  # get a list of prices (they will be in the same order as the items)
  prices = price_re.findall(shop_text)
  # get a list of links which lead to the haggle pages for the items
  links = haggle_url_re.findall(shop_text)
  print('Items in shop: %i' % len(items)) 
  return(items,prices,links)

'''
This is the function which puts together all our sub-functions. It refreshes 
the shop ( with refresh_shop() ), and if an item in our buylist, it attempts 
to buy it. Depending on the result of the buy attempt, it returns either 1 (
for a successful buy), or -1 (for a failed buy). If no item in our buylist is 
present, it returns 0. The arguments are:

url (str): url of the shop you want to buy in
ablist (str list): a list of the items you want to buy (this is loaded from a 
  .txt file)
shopheaders (dict): when you click on an item in the shop, you need to have 
  the appropriate 'referrer' header in order to be access the haggle page. 
  this variable is declared in the menu() function below.
s: the requests session
'''
def camper(url,ablist,shopheaders,s):
  items,prices,links = refresh_shop(url,s) # refresh the shop
  for item in ablist: # check if an item in our buylist is present
    if item in items: # if it is, try to buy it (using haggle())
      print("\a",end="") # makes a small noise
      print("Trying to get %s..." % item)
      success,message = (haggle("http://www.neopets.com/%s" % 
        links[items.index(item)],prices[items.index(item)],shopheaders,s))
      if success: # if we've successfully bought the item,
        print("\a",end="") # make a small noise and print a message
        print("Successfully bought %s. (%s)" % (item,message))
        grablist.append(item)
        return 1
      else: # if we haven't, print a message
        print("Darn!! Missed it! (%s)" % message)
        return (-1)
  return 0

'''
This function handles everything relating to actually buying an item. It 
visits the haggle page, solves the captcha, and submits an alternating-number 
haggle based on the price of the item (using the offer() function). It takes
four arguments:

url (str): the link to the item's haggle page (taken from the 'links') array in
  camper()
price (str): the price of the item. we pass this to the offer() function
shopheaders (str): same as shopheaders for camper()
s: the requests session

This function solves the captcha by finding the darkest pixel in the image.
For some reason, this is the correct answer 99% of the time (I believe it's 
because the neopet in the image usually has some faint black outline). TNT 
could prevent a lot of autobuyers from working properly if they just sprinkled
some black pixels throughout the captchas, but oh well, good for us!.
'''
def haggle(url,price,shopheaders,s):
  haggle_headers = {'referer': url,'user-agent':config.useragent}
  start = time.time()
  print("Waiting %.2fs (Pre-Haggle)..." % (config.prehaggle/1000))
  time.sleep(config.prehaggle/1000)
  print("Haggling...")
  haggle_page = (s.get(url, headers=shopheaders)).text
  if (captcha_re.search(haggle_page)):
    captcha_url = ("http://www.neopets.com" + 
      captcha_re.search(haggle_page).group(1))
    img_holder = (s.get(captcha_url,headers=haggle_headers))
    captcha_img = Image.open(BytesIO(img_holder.content))
    pixel_array = captcha_img.load()
    (cx,cy) = captcha_img.size
    (darkestx,darkesty) = (0,0)
    print("Solving OCR...")
    darkest_value = 765
    for y in range(0,cy):
      for x in range(0,cx):
        (r,g,b) = pixel_array[x,y];
        if (r+g+b) < darkest_value:
          (darkestx,darkesty) = (x,y);
          darkest_value = (r+g+b);
    newoffer = offer(price)
    print("Waiting %.2fs (OCR)..." % (config.ocr/1000))
    time.sleep(config.ocr/1000)
    payload = {'current_offer': newoffer, 'x': darkestx, 'y': darkesty}
    end = time.time()
    result = (s.post("http://www.neopets.com/haggle.phtml",
      data=payload,headers=haggle_headers)).text
    match = success_re.search(result)
    if match:
      return (True,"Price: %i; Buy Time: %.3fsec" % (newoffer,(end-start)))
    else:
      return (False,"Missed haggle")
  else:
    return (False,"No haggle")

'''
This function logs in to the account you've entered in the config file. It 
saves the cookie it gets, so you don't look suspicious by sending a login 
request every time you start the autobuyer. However, note that this cookie 
will be different from your browser's, so when you start the autobuyer you
will usually be automatically logged out from your browser.

Some might argue that this is also suspicious, but I've been using this for a 
few months without any issues.
'''
def test_cookie(s):
  cwd = os.getcwd()
  path = os.path.join(cwd,'cookie.txt')
  testcookie_re = re.compile('Welcome, <a href=\"/userlookup\.phtml\?user=' + 
      config.username + '\">' + config.username)
  if not os.path.isfile(path): # if there is no cookie.txt,
    print('Getting a cookie...') # make it
    s.post(login_url, 
      data={'username':config.username,'password':config.password}, 
      headers=headers)
    print('Writing cookie to file...')
    jar = open(path,'wb')
    pickle.dump(s.cookies,jar)
    jar.close()
    test_page = (s.get('http://www.neopets.com', headers=headers)).text
    if testcookie_re.search(test_page): # if it does, we're done
      print('Done.')
      return True
    else:
      print('Hmm... there seems to be a problem. Check your username and' + 
        ' password')
      return False
  else: # if there is a cookie.txt,
    cookiefile = open(path,'rb') # load it up
    cookies = pickle.load(cookiefile)
    cookiefile.close()
    s.cookies = cookies # attach it to the session, and see if it works
    test_page = (s.get('http://www.neopets.com', headers=headers)).text
    if testcookie_re.search(test_page): # if it does, we're done
      print('Nice, cookie works.')
      return True
    else: # otherwise, get a new one
      print('Cookie is expired, getting new one...')
      s.post(login_url, 
        data={'username':config.username,'password':config.password}, 
        headers=headers)
      print('Writing cookie to file...')
      jar = open(path,'wb')
      pickle.dump(s.cookies,jar)
      jar.close()
      test_page = (s.get('http://www.neopets.com', headers=headers)).text
      if testcookie_re.search(test_page): # if it does, we're done
        print('Done.')
        return True
      else:
        print('Hmm... there seems to be a problem. Check your username and' + 
          ' password')
        return False
'''
This function is for the menu. It just asks you what shop you'd like to buy in.
'''
def ask_for_shop(shoplist):
  print('Shops:')
  for shopID in shoplist:
    print('  - %s (%i)' % (shoplist[shopID],shopID))
  while True:
    shop = input('Which shop do you want to buy in? (enter the shop id)\n> ')
    if shop.isnumeric():
      shop = int(shop)
      if shop not in shoplist:
        print('Sorry, that shop isn\'t in the list')
      else: 
        break
    else:
      print('Please enter a valid number') 
  return shop

'''
This function is for the menu. It asks you how long you want to run the 
autobuyer for.
'''
def ask_for_duration():
  while True:
    duration = input("How long should the autobuyer run for?" + 
      " (in minutes) \n> ")
    if duration.isnumeric():
      duration = int(duration)
      break
    else:
      print("Please enter a valid number.")
  return duration * 60

'''
This function loads the buylist from a .txt file. For instructions on how to 
make this .txt file, consult the README
'''
def load_ablist(shopID):
  cwd = os.getcwd()
  path = os.path.join(cwd, "ABlists/%i.txt" % shopID)
  f = open(path, mode='r')
  ablist = (f.read()).split(sep="\n")
  f.close()
  return ablist

'''
This function handles all the looping. It calls the camper() function over and 
over again, and takes breaks depending on the settings in the config file.
'''
def menu(s):
  grablist.clear() # clear the grablist for a new autobuying session
  target = ask_for_shop(config.shoplist) # get the target shop
  total_duration = ask_for_duration() # get the total duration
  shop_url = ("http://www.neopets.com/objects.phtml?obj_type=%i&type=shop" % 
    target)
  ablist = load_ablist(target)
  shopheaders = {'referer':shop_url,'user-agent':config.useragent}
  start_time = time.time() # for loop tracking
  current_time = time.time() # for loop tracking
  while (current_time - start_time) < total_duration:
    session_duration = random.randint(config.session_duration_lo,
      config.session_duration_hi) # sets a session timer based on config
    print('Starting %.2f minute autobuying session...' % (session_duration/60))
    print_time()
    session_start_time = time.time()
    while (current_time - session_start_time) < session_duration:
      current_time = time.time()
      result = camper(shop_url,ablist,shopheaders,s)
      if result == 1:
        print("Waiting 5s (no-buy time)")
        time.sleep(5)
      elif result == 0:
        sleepo = (random.randint(config.refresh_rate_lo,
          config.refresh_rate_hi)/1000)
        print("Waiting %.2fs..." % sleepo)
        time.sleep(sleepo)
      else:
        print("Checking for next best item...")
    print_time()
    break_time = random.randint(config.break_duration_lo,config.break_duration_hi)
    print("Session finished, taking a break for %.2f minutes." %
      (break_time/60))
    time.sleep(break_time) # take a break based on config
  print("Time limit up! Stopping...")
  print_time()
  if grablist == []: # if we didn't get any items, print a frown
    print("Didn't manage to grab anything :(")
  else: # otherwise, print the items we managed to get!
    print("Managed to grab the following items:")
    print(grablist)

# --------- EXECUTION --------- #

s = Session() # initiate the requests session
s.proxies = config.proxy # set proxies (if any)

if test_cookie(s): # if login is sucessful,
  while True: # start!
    menu(s)