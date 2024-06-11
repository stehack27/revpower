import os
from settings import SCREENSHOT_DIRECTORY, UPLOAD_DIRECTORY, DOWNLOAD_DIRECTORY, color
from threading import Thread
from http_server import http_run
from tcp_server import TCP_Handler

#Create directories if not exits
[os.makedirs(d) for d in [SCREENSHOT_DIRECTORY, UPLOAD_DIRECTORY, DOWNLOAD_DIRECTORY] if not os.path.exists(d)]

#Start magic...
print(f"{color.PURPLE}RevPower - @steppeerr{color.END}")
http_thread = Thread(target=http_run, daemon=True)
http_thread.start()
tcp_thread = TCP_Handler().run()
