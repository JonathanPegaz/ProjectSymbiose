import machine, neopixel, time
import bluetooth
from ble_advertising import advertising_payload
from ble_uart_peripheral import *

ble = bluetooth.BLE()
uart = BLEUART(ble, "esp_led_3")

# define neopixel
pin = 5
n = 300
mid_n = int(n / 2)
np = neopixel.NeoPixel(machine.Pin(pin), n)

# to folow the current led 
currentLed = 0

rm = 80
gm = 10
bm = 70

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
        
def glowLight(r, g, b, i):
    
    currentLed = i
    minLed = currentLed - 10
        
    np[i] = (r, g, b)
            
    if minLed > -1 :             
        np[minLed] = (int(r/2), int(g/2), int(b/2))
        


def stepGlowLights(r, g, b, end, delai):
        
    for i in range(0, end) :
        glowLight(r, g, b, i)
        time.sleep(delai)
        np.write()


######### code for led
            
# reset led
init()

uart.irq(handler=on_rx)

while True:
        
    if status == "reset" :
        init()
        
    elif status == "running" :
        stepGlowLights(rm, gm, bm, n, 0)

    elif status == "signal_1" :
        stepGlowLights(rh, gh, bh, int(n * 1/3), 0)
        
    elif status == "signal_2" :
        stepGlowLights(rh, gh, bh, int(n * 2/3), 0)
        
    elif status == "signal_3" :
        stepGlowLights(rh, gh, bh, int(n * 3/3), 0)
    
    elif status == "end" :
        if(endIsSend == 1) :
            # voir pour changer le message en fonction de la fin de l'expérience
            uart.write("next step")
            endIsSend = 1
            
        stepGlowLights(rh, gh, bh, n, 0)
        
    if status == "next" :
        print("next")
        stepGlowLights(int(rh/10), int(gh/10), int(bh/10), n, 0)
        status = "terminated"
        
uart.close()

