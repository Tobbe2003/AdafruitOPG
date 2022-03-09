import pyfirmata
import time
from Adafruit_IO import Client, Feed, RequestError

run_count = 0
ADAFRUIT_IO_USERNAME = "Tobbi2003"
ADAFRUIT_IO_KEY = "aio_EWHd69z5gJZFRjUQmjydXj3VqRUt"

aio = Client(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)

board = pyfirmata.Arduino('COM4')

it =  pyfirmata.util.Iterator(board)
it.start()

analog_input = board.get_pin ('a:0:i')
digital_output = board.get_pin ('d:12:o')

try:
    digital = aio.feeds('digital')
except RequestError:
    feed = Feed(name='digital')
    digital = aio.create_feed(feed)

while True:
    print('Sending count:', run_count)
    run_count += 1
    aio.send_data('counter', run_count)
    
    data = aio.receive(digital.key)

    print('Data: ', data.value)

    if data.value == "ON":
        digital_output.write(True)
    else:
        digital_output.write(False)
    aio.send_data("potentiometer", analog_input.read())
    time.sleep(3)