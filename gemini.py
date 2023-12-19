#!/usr/bin/env python3

from email.message import Message
import sys, subprocess
import os
import tempfile
import textwrap
import urllib.parse
import gemini_protocol
import jpeg_to_text
import shutil

escape = "\33["

def open_file(filename):
    if sys.platform == "win32":
        os.startfile(filename)
    else:
        opener = "open" if sys.platform == "darwin" else "xdg-open"
        subprocess.call([opener, filename])

menu = []
hist = []

def print_long(string):
    text = string.splitlines()
    if (len(text) > os.get_terminal_size()[1] - 1):
        i = 0
        while (i <= len(text)):
            for j in range(os.get_terminal_size[1] - 1):
                i += 1
                if (i <= len(text)):
                    print(text[i])


def absolutise_url(base, relative):
    # Absolutise relative links
    if "://" not in relative:
        # Python's URL tools somehow only work with known schemes?
        base = base.replace("gemini://","http://")
        relative = urllib.parse.urljoin(base, relative)
        relative = relative.replace("http://", "gemini://")
    return relative

while True:
    # Get input
    cmd = input(escape + "0m" + "> ").strip()
    # Handle things other than requests
    if cmd.lower() == "q":
        print("Bye!")
        break
    # Get URL, from menu, history or direct entry
    if cmd.isnumeric():
        try:
            url = menu[int(cmd)-1]
        except IndexError:
            print("Link " + cmd + " doesn't exist")
            continue
    elif cmd.lower() == "b":
        # Yes, twice
        url = hist.pop()
        url = hist.pop()
    else:
        url = cmd
        if not "://" in url:
            url = "gemini://" + url
    # Do the Gemini transaction
    success, status, mime, fp = gemini_protocol.gemini(url)
    if success:
        # Handle text
        if mime.startswith("text/"):
            # Decode according to declared charset
            m = Message()
            m['content-type'] = mime
            mime = m.get_content_type()
            body = fp.read()
            try:
                m.set_param("charset","UTF-8")
                body = body.decode(m.get_param("charset"))
            except AttributeError:
                pass
            # Handle a Gemini map
            if mime == "text/gemini":
                menu = []
                preformatted = False
                #first, put all the lines into a list
                lines = []
                for num, line in enumerate(body.splitlines()):
                    if line.startswith("```"):
                        preformatted = not preformatted
                    elif preformatted:
                        lines.append(line)
                    elif line.startswith("=>") and line[2:].strip():
                        bits = line[2:].strip().split(maxsplit=1)
                        link_url = bits[0]
                        link_url = absolutise_url(url, link_url)
                        menu.append(link_url)
                        text = bits[1] if len(bits) == 2 else link_url
                        lines.append("[%d] %s" % (len(menu), text))
                    else:
                        linewrapped = textwrap.fill(line, min(80, os.get_terminal_size()[0])).splitlines()
                        for j in range(len(linewrapped)):
                            lines.append(linewrapped[j])
                        if (len(linewrapped) == 0):
                        	lines.append("")
                #and then print the lines
                offset = 2
                lastbreak = 0
                for i in range(len(lines)):
                    print(lines[i])
                    if ((((i - lastbreak) + 1) % (os.get_terminal_size()[1] - (offset + 1))) == 0):
                        input("<press return to continue>")
                        lastbreak = i
            # Handle any other plain text
            else:
                print_long(body)
        # Handle non-text
        else:
            tmpfp = tempfile.NamedTemporaryFile("wb", delete=False)
            tmpfp.write(fp.read())
            tmpfp.close()
            if mime.startswith("image/"):
                jpeg_to_text.print_img(tmpfp.name)
            else:
                newname = input("save file as? ")
                shutil.copy2(tmpfp.name, "./downloads/" + newname)
                open_file("./downloads/" + newname)
                os.unlink(tmpfp.name)
        # Update history
        hist.append(url)
