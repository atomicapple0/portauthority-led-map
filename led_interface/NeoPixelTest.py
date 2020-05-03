import board
import neopixel
import time
pixels = neopixel.NeoPixel(board.D12, 200) 
pos = 50.0
vel = 0.0
while 1:
    pixels[int(pos)] = (0,0,0)
    vel += -.5
    pos += vel
    if pos <= 0:
        pos = 0
        vel = -1 * vel
    print(pos)
    pixels[int(pos)] = (255,5*int(pos),255-5*int(pos))
    time.sleep(.01)

