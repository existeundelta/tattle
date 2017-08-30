#!/usr/bin/python
import webkit, gtk, time
window = gtk.Window()
browser = webkit.WebView()
window.set_title("Scrape text analyser")
window.add(browser)
window.show()
browser.show()
browser.load_uri("https://www.online-utility.org/text/analyzer.jsp")
#browser.execute_script("document.getElementsByClassName('bigtextarea').focus()")

def send_keys(inputs):
    for value in inputs:
        event = gtk.gdk.Event(gtk.gdk.KEY_PRESS)
        if type(value) is str:
            event.keyval = ord(value)
        else:
            event.keyval = value
        event.time = 0
        browser.emit('key-press-event', event)

send_keys([gtk.keysyms.Tab,gtk.keysyms.Tab])
send_keys([gtk.keysyms.Tab,gtk.keysyms.Tab])
send_keys([gtk.keysyms.Tab,gtk.keysyms.Tab])
send_keys([gtk.keysyms.Tab,gtk.keysyms.Tab])
send_keys([gtk.keysyms.Tab,gtk.keysyms.Tab])
send_keys([gtk.keysyms.Tab])
send_keys('The cat crept into the crypt crapped and crept out again')
send_keys([gtk.keysyms.Tab,gtk.keysyms.Tab])
send_keys([gtk.keysyms.Return])

page = browser.get_main_frame().get_data_source().get_data()

#window.fullscreen()
window.connect("delete-event", gtk.main_quit)
#window.connect("load-finished", onload)
#gtk.main()
