"""
Copyright Kinvert All Rights Reserved
If you would like to use this code for
business or education please contact
us for permission at:
www.kinvert.com/
Free for personal use
"""

import anki_vector
from anki_vector.util import degrees
import random
import sys
import time

try:
    from PIL import Image, ImageDraw 
except ImportError:
    sys.exit("Cannot import from PIL. Do `pip3 install --user Pillow` to install")
 
def npc_vector(bx,by,bvx,bvy):
    return by + random.randint(-5,5)
    
def draw_face(x, y, bx, by, px, py, vx, vy):
    dimensions = (184, 96)
    face_image = Image.new(
        'RGBA', dimensions, (0, 0, 0, 255))
    dc = ImageDraw.Draw(face_image)

##The cube for bashing
    
    dc.rectangle([bx-8, by-8, bx+8, by+8], fill=(255, 255, 255, 255))
    dc.rectangle([bx-7, by-7, bx+7, by+7], fill=(0, 0, 0, 255))
    dc.rectangle([bx-4, by-4, bx+4, by+4], (255, 255, 255, 255))
    dc.rectangle([bx-3, by-3, bx+3, by+3], (0, 0, 0, 255))
##The play area
    dc.line([92, 0, 92, 96], (255, 255, 255, 255))

##the paddals
    
    dc.rectangle([px-4, py-10, px, py+10], fill=(0, 0, 255, 255))
    dc.rectangle([vx+4, vy-10, vx, vy+10], fill=(255, 0, 0, 255))
    return face_image
##10 to 16 fix 
def impact(bx,by,bvx,bvy,paddleY):    
    if abs(paddleY-by) < 16:
        bvx = bvx * -1
        bvy += (0.5 * (by - paddleY))
        if abs(bvy) < 0.2:
            bvy = 0.5
        bvx = bvx * 1.1
    return bvx, bvy

up_axis=0
cjy=0
py = 30


args = anki_vector.util.parse_command_args()
with anki_vector.Robot(args.serial) as robot:

    print(" disconnecting from any connected cube…")
    robot.world.disconnect_cube()

    time.sleep(2)
    connected_cube = robot.world.connected_light_cube
    robot.behavior.say_text("Turning my cube in to !! a joystick !")
    connectionResult = robot.world.connect_cube()
    time.sleep(1)
    robot.behavior.say_text("There you go connected! first to 3 wins ")
    
    if robot.world.connected_light_cube:
            cube = robot.world.connected_light_cube

            cube.set_light_corners(anki_vector.lights.blue_light,
                                   anki_vector.lights.red_light,
                                   anki_vector.lights.blue_light,
                                   anki_vector.lights.red_light)
    
    robot.behavior.set_head_angle(degrees(45.0))
    Vscore = 0
    Pscore = 0
##yes the main loop start here    
    for x in range(0, 5):

        robot.behavior.say_text("The score is" + str(Vscore) + "to me  and" + str(Pscore) + " to you") 
    
        robot.behavior.say_text("touch my whole back to serve")


        
        while not robot.touch.last_sensor_reading.is_being_touched:
            time.sleep(0.1)
  

        
        robot.behavior.say_text(" Get ready. ")

        over = 0
        bx = 90
        by = 40
        bvx = -5
        bvy = -1
        px = 10
        vx = 173
        cjy=0
        py = 30

        
##yes i know it  not  cricket but round_done is a long ass verable         
        while not over:

        
            
            connected_cube = robot.world.connected_light_cube
            

            if (robot.world.connected_light_cube.up_axis) == 1: 
                up_axis=6
                py = (py - 5)
            
            if (robot.world.connected_light_cube.up_axis) == 2:
                py = (py + 5)
                up_axis=6
                
            if (robot.world.connected_light_cube.up_axis) == 3:
                py = (py + 5)
                up_axis=6

            if (robot.world.connected_light_cube.up_axis) == 4:
                py = py (py - 5)
                up_axis == 6


            if py<= 0:
                py = 1

            if py>= 96:
                py = 96
                    
                
            else:    
            
                
                vy = npc_vector(bx,by,bvx,bvy)
                if by <= 0:
                    bvy = bvy * -1
                if by > 95:
                    bvy = bvy * -1
                if bx <= px and bx >= 0:
                    bvx, bvy = impact(bx,by,bvx,bvy,py)
                if bx >= vx and bx <= 183:
                    bvx, bvy = impact(bx,by,bvx,bvy,vy)
                bx += bvx
                by += bvy
                if bx < 0:
                    robot.behavior.say_text("I win that one")
                    over = 1
                    robot.anim.play_animation_trigger('BlackJack_VictorBlackJackWin')
                    Vscore = (Vscore + 1)
                elif bx > 183:
                    robot.behavior.say_text("You win that one")
                    robot.anim.play_animation_trigger('BlackJack_VictorBlackJacklose')
                    over = 1
                    Pscore = (Pscore + 1)
                
                face_image = draw_face(0, 0, bx, by, px, py, vx, vy)
                screen_data = anki_vector.screen.convert_image_to_screen_data(
                    face_image)
                robot.screen.set_screen_with_image_data(
                    screen_data, 0.1, interrupt_running=True)
                if bvx < 0 and bx < 90:
                    time.sleep(0.1)
                else:
                    time.sleep(0.01)

    robot.behavior.say_text("game over!")

    robot.behavior.say_text("The score is" + str(Vscore) + "to me  and" + str(Pscore) + " to you")
    
    if Vscore >= Pscore:
        robot.behavior.say_text("Well ,I won ,better luck next time ")
        robot.anim.play_animation_trigger('GreetAfterLongTime')

    if Vscore <= Pscore:
        robot.behavior.say_text("What you  won  I demand  a rematch ")
        robot.anim.play_animation_trigger('RollBackRealine')
