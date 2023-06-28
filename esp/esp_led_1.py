import machine, neopixel, time
import bluetooth
from ble_advertising import advertising_payload
import machine, neopixel, time
import bluetooth
from ble_advertising import advertising_payload
from ble_uart_peripheral import *

ble = bluetooth.BLE()
uart = BLEUART(ble, "esp_led_1")

# define neopixel
pin = 5
n = 300
mid_n = int(n / 2)
np = neopixel.NeoPixel(machine.Pin(pin), n)

# to folow the current led 
currentLed = 0

rr = 40
gr = 15
br = 0

rh = 60
gh = 80
bh = 40

# waiting, running, end
status = "waiting"
endIsSend = 0

def init():
    global status
    status = "waiting"
    reset()
    
def reset():
    for i in range(n):
        np[i] = (0, 0, 0)
    np.write()
        
def on_rx():
    global status
    status = uart.read().decode().strip()
    uart.write(status)
    if status == "reset":
        reset()
        
def glowLight(r, g, b, i, isStart):
    
    currentLed = i
    minLed = currentLed - 10
    
    if isStart :
        
        if n > i and i < mid_n:
            np[i] = (r, g, b)
            
        if minLed > -1 and i < mid_n + 10 :             
            np[minLed] = (int(r/2), int(g/2), int(b/2))
            
    else :
        
        if n > i :
            np[i] = (r, g, b)
          
        if mid_n < i - 10:
            np[minLed] = (int(r/2), int(g/2), int(b/2))


def stepGlowLights(r, g, b, isStart, delai):
    
    if isStart :
        arr = range(0, mid_n + 10)
    else :
        arr = range(mid_n, n + 10)
        
    for i in arr :
        glowLight(r, g, b, i, isStart)
        time.sleep(delai)
        np.write()

######### code for led
            
# reset led
init()

uart.irq(handler=on_rx)

while True:
        
    if status == "running" :
        stepGlowLights(rr, gr, br, False, 0)
    
    elif status == "end" :
        if(endIsSend == 1) :
            uart.write("next step")
            endIsSend = 1
            
        stepGlowLights(rh, gh, bh, True, 0)
        
    if status == "next" :
        stepGlowLights(int(rr/2), int(gr/2), int(br/2), False, 0)
        stepGlowLights(int(rh/2), int(gh/2), int(bh/2), True, 0)
        status == "terminated"
        
uart.close()