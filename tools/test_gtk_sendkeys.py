#!/usr/bin/python
import webkit, gtk, time
window = gtk.Window()
browser = webkit.WebView()
window.set_title("Dashboard")
window.add(browser)
window.show()
browser.show()
browser.load_uri("http://google.com")
browser.execute_script("document.getElementById('lst-ib').value = 'Hey ho lets go'")

def hitReturn():    
    event = gtk.gdk.Event(gtk.gdk.KEY_PRESS)
    event.keyval = gtk.keysyms.Return
    event.time = 0
    browser.emit('key-press-event', event)

#window.fullscreen()
window.connect("delete-event", gtk.main_quit)
#window.connect("load-finished", onload)

time.sleep(3)
doSearch()
#gtk.main()
