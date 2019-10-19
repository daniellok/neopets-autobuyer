# Neopets Autobuyer
**Update 19/10/2019: This repo was last updated in 2017, and since then, Neopets has somewhat improved their site security. As far as I know, this script no longer works. There are currently no plans to update this script.**

This is a simple script to buy profitable items from the NPC shops in Neopets. I wrote it largely as a learning exercise—it actually turned out to be quite simple, and I believe you can write your own if you have some experience programming. The most crucial thing to learn would be how to use HTTP requests.

In the case of this program, I use Python (3) together with the [Requests](https://github.com/requests/requests) package. Their documentation is indeed fantastic (as they claim themselves), so much so that I managed to pick it up having no prior knowledge about what an HTTP request even was.

## Requirements

I work on a Mac, so I haven't tested this script for cross-OS compatibility with Windows or Linux, but I don't believe there should be any problems.

- [Python 3](https://www.python.org/downloads/) (follow the link to install it if you don't already)
- Python's [Requests](https://github.com/requests/requests) package (type `pip install requests` into the command line once you've installed python 3)
- Some sort of code editor is recommended (I like [Sublime](https://www.sublimetext.com/)), but you can make do with Notepad/TextEdit.

## Starting the Program

1. Download this repo 

2. Open up your command prompt/terminal and navigate to the folder using `cd` ([here](http://lifehacker.com/5633909/who-needs-a-mouse-learn-to-use-the-command-line-for-almost-anything)'s a good primer for using the command-line, if you don't already know how to use it).

3. Edit the variables inside the `config.py` file (see 'Configuring the Program' below) to your liking. You can edit these by opening the file in any code editing program (you can even use Notepad/TextEdit, but I find that syntax highlighting makes a big difference).

4. Enter `python autobuyer.py` to run the autobuyer script!

5. If login is successful, you'll be presented with a list of shops (taken from the config file), like this:

   ![initial screen](https://user-images.githubusercontent.com/28850773/29163241-718b3992-7dee-11e7-9e50-f5ff64cab008.png)

   Simply enter the shop ID (in brackets next to the shop name) that you want to buy in, and press enter.

6. Once you've done that, you'll be asked how long you want to run the program for. Personally, I usually run it for around 6 hours at a time. The program will automatically take breaks throughout the entire duration, so no worries there.

   ![duration screen](https://user-images.githubusercontent.com/28850773/29163251-77e927a4-7dee-11e7-9615-0f6cfa20a49a.png)

   The length of both the breaks and the autobuying sessions is defined by you in the config file.

7. That's it! You can just let it run in the background while you do your thing (though I'd suggest not playing Neopets while it is running). It'll make a small noise when it sees something to buy, so you don't have to worry about missing anything.

   The program will print to the command prompt/terminal shell every time it refreshes, so you can monitor its status.

   ![buyer in action](https://user-images.githubusercontent.com/28850773/29163587-8c255188-7def-11e7-99a9-b252fdbaf7bb.png)

If you'd like to quit the program, press [Ctrl+C](https://en.wikipedia.org/wiki/Control-C) at any time.

## Configuring the Program

All configurations should be made to the `config.py` file. 

Here, you can edit various settings such as the refresh rate, the duration of a session, and how long breaks should be in-between sessions. For the most part, you can leave these values as they are in the default settings (except for the username and password—you'll need to put your own account details). 

If you'd like to be more aggressive or conservative than the defaults, by all means do so! More specific instructions can be found in the code comments in the `config.py` file itself.

## Generating Buylists

Make sure that all the shops in your `shoplist` variable in the config file have a corresponding buylist in the `ABLists` folder! I've included my lists in the folder, but these haven't been updated in a number of months, so you'll probably want to make them a bit more current.

The buylists should be named with the shop ID of the shop they represent, and they should be in .txt format in plain text. [Here](http://www.neocodex.us/forum/topic/121985-guide-eefis-restock-list-helper-d/) is NeoCodex's guide on making your own list—it's pretty easy to follow!

## Acknowledgements

Shoutout to NeoCodex for their great tutorials on how to get started writing an autobuyer. I'm not active in the community, but there's a lot of good information there which is publicly available.

If you've got any questions or bug reports, let me know!

