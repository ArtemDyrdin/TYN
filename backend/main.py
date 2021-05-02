import asyncio
import websockets
import numpy as np
import urllib.request as ur
from cv2 import cv2
from PIL import Image

connected = set()

print('server started \n')

async def server(websocket, path):
  # Register.
  connected.add(websocket)
  print('websocket opened \n')
  try:
    async for message in websocket:

      # extract the contents of the URL:
      try:
        url_response = ur.urlopen(message)

        # convert it into a numpy array
        img_array = np.array(bytearray(url_response.read()), dtype=np.uint8)

        # decode the image (готово для использования в библиотеке cv2)
        img = cv2.imdecode(img_array, -1)
        print(img)
        # cv2.imshow('URL Image', img)
        # cv2.waitKey()
        print('done \n')
      except:
        print('error with url decoding')

  except:
    # Unregister.
    print('ERROR!!!! \n websocket closed \n')
    connected.remove(websocket)

start_server = websockets.serve(server, "localhost", 5000)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()