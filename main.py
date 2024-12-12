#TODO:
#Test input and output signals in Hammond first with oscilloscope
#then Adjust pins for new Xiao board

import rp2
from machine import Pin
import utime
from ws2812 import WS2812

## the state machine pio loop

@rp2.asm_pio(set_init=rp2.PIO.OUT_LOW)
def divide():
    
    pull(noblock)
    mov(y,osr)
    
    wrap_target()
    label("start")
    mov(x, y)
    set(pins,0)    
    label("loop1")
    wait(0,pin,0)
    jmp(x_dec,"d1")
    jmp("part2")
    label("d1")
    wait(1,pin,0)
    jmp(x_dec,"loop1")

    label("part2") # second half of the output wave
    
    set(pins,1)
    mov(x, y)
    label("loop2")
    wait(0,pin,0)
    jmp(x_dec,"d2")
    jmp("start")
    label("d2")
    wait(1,pin,0)
    jmp(x_dec,"loop2")
    
    
    wrap()
    
 ##-------------------------------------------   

  



#LED STUFFS

power = machine.Pin(11,machine.Pin.OUT)
power.value(1)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 150, 0)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
PURPLE = (180, 0, 255)
WHITE = (255, 255, 255)
COLORS = (BLACK, RED, YELLOW, GREEN, CYAN, BLUE, PURPLE, WHITE)

led = WS2812(12,1)#WS2812(pin_num,led_count)

modepin = Pin(1, Pin.IN, Pin.PULL_UP) #a solder jumper on pin 7 to select either 5833 or 5832 mode
pin0 = Pin(26, Pin.IN, Pin.IN)

if modepin.value() == 0:	#only in 5833 mode
    div0 = 338
    div1 = 358
    div2 = 379
    div3 = 402
    div4 = 426
    div5 = 451
    div6 = 0 #no div6 on MM5833
    sm7 = rp2.StateMachine(6, divide, set_base=Pin(19), in_base=pin0)
    sm7.put(div6)
    sm7.active(1)
    activecolour = CYAN
    led.pixels_fill(activecolour)
    led.pixels_show()
    
else:
    div0 = 478
    div1 = 239
    div2 = 253
    div3 = 268
    div4 = 284
    div5 = 301
    div6 = 319  
    activecolour = PURPLE
    led.pixels_fill(activecolour)
    led.pixels_show()
    

#start the actual statemachines    

    
sm1 = rp2.StateMachine(0, divide, set_base=Pin(27), in_base=pin0)
sm1.put(div0)
sm1.active(1)

sm2 = rp2.StateMachine(1, divide, set_base=Pin(28), in_base=pin0)
sm2.put(div1)
sm2.active(1)

sm3 = rp2.StateMachine(2, divide, set_base=Pin(29), in_base=pin0)
sm3.put(div2)
sm3.active(1)

sm4 = rp2.StateMachine(3, divide, set_base=Pin(6), in_base=pin0)
sm4.put(div3)
sm4.active(1)

sm5 = rp2.StateMachine(4, divide, set_base=Pin(7), in_base=pin0)
sm5.put(div4)
sm5.active(1)

sm6 = rp2.StateMachine(5, divide, set_base=Pin(0), in_base=pin0)
sm6.put(div5)
sm6.active(1)


while True:

    utime.sleep(2)
    led.pixels_fill(BLACK)
    led.pixels_show()
    utime.sleep(0.1)
    led.pixels_fill(activecolour)
    led.pixels_show()



    
    