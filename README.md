# Neopets Autobuyer

This is a simple script to buy profitable items from the NPC shops in Neopets. I wrote it largely as a learning exercise—it actually turned out to be quite simple, and I believe you can write your own if you have some experience programming. The most crucial thing to learn would be how to use HTTP requests.

In the case of this program, I use Python (3) together with the [Requests](https://github.com/requests/requests) package. Their documentation is indeed fantastic (as they claim themselves), so much so that I managed to pick it up having no prior knowledge about what an HTTP request even was.

## Requirements

I work on a Mac, so I haven't tested this script for cross-OS compatibility with Windows or Linux, but I don't believe there should be any problems.

- [Python 3](https://www.python.org/downloads/) (follow the link to install it if you don't already)
- Python's [Requests](https://github.com/requests/requests) package (type `pip install requests` into the command line once you've installed python 3)

## Starting the Program

1. Download this repo 
2. Open up your command prompt/terminal and navigate to the folder using `cd` ([here](http://lifehacker.com/5633909/who-needs-a-mouse-learn-to-use-the-command-line-for-almost-anything)'s a good primer for using the command-line, if you don't already know how to use it).
3. Edit the variables inside the `config.py` file (see 'Configuring the Program' below) to your liking. You can edit these by opening the file in any code editing program (you can even use Notepad/TextEdit, but I find that syntax highlighting makes a big difference).
4. Enter `python autobuyer.py` to run the autobuyer script!

Once the program is running, you'll be presented with a list 

## Configuring the Program

All configurations should be made to the `config.py` file. Here, you can edit various settings such as the refresh rate, the duration of a session, and how long breaks should be in-between sessions.



