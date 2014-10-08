#!/usr/bin/env python
import shelve
import hashlib
import os        

KEY_FILE='keys.db'

def save_key(core_name, email,type):
    core_name = str(core_name)
    print "saving key for", core_name, email
    s = shelve.open(KEY_FILE)
    if core_name in s:
        return False
    salt = os.urandom(32).encode('base_64')
    keys = hashlib.md5( salt + core_name ).hexdigest()
    view_key, delete_key = keys[:16],keys[16:]
    if type != "private":
        view_key="";
    s[core_name] = (view_key, delete_key, salt, email)
    s.close()
    return view_key, delete_key
 
def check_delete_key(core_name, provided_key):
    core_name = core_name.encode("utf-8")
    provided_key =  provided_key.encode("utf-8")
    s = shelve.open(KEY_FILE)
    if core_name not in s:
        s.close()
        return False
    else:
        view_key, delete_key, salt, email = s[core_name]
        s.close()
        return provided_key == delete_key
    s.close()

def check_key(core_name, provided_key):
    core_name = core_name.encode("utf-8")
    provided_key =  provided_key.encode("utf-8")
    s = shelve.open(KEY_FILE)
    if core_name not in s:
        s.close()
        return False
    else:
        view_key, delete_key, salt, email = s[core_name]
        s.close()
        return provided_key == view_key
    s.close()

def is_private(core_name):
    core_name = core_name.encode("utf-8")
    s = shelve.open(KEY_FILE)
    if core_name not in s:
        s.close()
        return False
    else:
        view_key, delete_key, salt, email = s[core_name]
        s.close()
        if view_key=="":
            return False
        return True

def private_cores():
    s = shelve.open(KEY_FILE)
    names = s.keys()
    names2= []
    for name in names:
        view_key, delete_key, salt, email = s[name]
        if view_key != "":
            names2.append(name)
    s.close()
    return names2

def dump_keys():
    s = shelve.open(KEY_FILE)
    for core_name in s:
        print core_name, s[core_name] 

from mako.template import Template

def sendmail(recipient, view_url, delete_url, network_name):
    print "SENNNDING MAIL"
    gmail_user = 'pinv.biosual@gmail.com'
    gmail_pwd = ''
    from mako.lookup import TemplateLookup
    lookup = TemplateLookup(directories=['html'])
    tpl = lookup.get_template("email.mako")
    import smtplib
    from email.mime.text import MIMEText
    s = smtplib.SMTP("smtp.gmail.com",587)
    s.ehlo()
    s.starttls()
    s.ehlo
    s.login(gmail_user, gmail_pwd)
    messagetext = tpl.render(network_name=network_name, view_url=view_url, delete_url=delete_url)
    msg = MIMEText(messagetext)
    sender = "pinv@cbio.uct.ac.za"
    import datetime
    msg['Subject'] = 'PINV network loaded! (%s)'%datetime.datetime.now().strftime("%H:%M")
    msg['From'] = sender
    msg['To'] = recipient
    rsp = s.sendmail(sender, [recipient], msg.as_string())
    s.quit()
    return messagetext
