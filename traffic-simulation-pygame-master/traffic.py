import pygame
import sys
import math as mt
import numpy as np
import datetime
from pygame import *
from pygame.locals import *
from pygame.sprite import *

# initialize pygame
pygame.init()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BGCOLOR = (128, 128, 128)

STREET = 120
STRIPE = 6
WIDTH = int(120 * 6)
HEIGHT = int(120 * 6)

HORMAP = [[0 for col in range(WIDTH)] for row in range(4)]
VERMAP = [[0 for col in range(HEIGHT)] for row in range(4)]

CAPTION = 'Traffic Simulation'
SPEED = 0
STREET_POS = [(0, (HEIGHT - STREET) / 2, WIDTH, STREET),
              ((WIDTH - STREET) / 2, 0, STREET, HEIGHT)]
SIGNAL_POS = [[WIDTH / 2 - STREET / 2 - 20, HEIGHT / 2 + STREET / 2 + 5],
              [WIDTH / 2 + STREET / 2 + 20, HEIGHT / 2 - STREET / 2 - 5],
              [WIDTH / 2 - STREET / 2 - 5, HEIGHT / 2 - STREET / 2 - 20],
              [WIDTH / 2 + STREET / 2 + 5, HEIGHT / 2 + STREET / 2 + 20]]

STOP_LANE = [(WIDTH / 2 + STREET * 5 / 4 - STRIPE, HEIGHT / 2 - STREET / 2, STRIPE, STREET),
             (WIDTH / 2 - STREET * 5 / 4, HEIGHT / 2 - STREET / 2, STRIPE, STREET),
             (WIDTH / 2 - STREET / 2, HEIGHT / 2 - STREET - 30, STREET, STRIPE),
             (WIDTH / 2 - STREET / 2, HEIGHT / 2 + STREET + 30 - STRIPE, STREET, STRIPE)]

DOUBLE_LANE = [(0, HEIGHT / 2 - 2, WIDTH / 2 - STREET * 5 / 4, STRIPE / 3),
               (0, HEIGHT / 2 + 2, WIDTH / 2 - STREET * 5 / 4, STRIPE / 3),
               (WIDTH / 2 + STREET * 5 / 4, HEIGHT / 2 - 2, WIDTH / 2 - STREET * 3 / 4, STRIPE / 3),
               (WIDTH / 2 + STREET * 5 / 4, HEIGHT / 2 + 2, WIDTH / 2 - STREET * 3 / 4, STRIPE / 3),
               (WIDTH / 2 - 2, 0, STRIPE / 3, HEIGHT / 2 - STREET * 5 / 4),
               (WIDTH / 2 + 2, 0, STRIPE / 3, HEIGHT / 2 - STREET * 5 / 4),
               (WIDTH / 2 - STRIPE / 3, HEIGHT / 2 + STREET + STREET / 4, STRIPE / 3, HEIGHT / 2 - STREET * 3 / 4),
               (WIDTH / 2 + STRIPE / 3, HEIGHT / 2 + STREET + STREET / 4, STRIPE / 3, HEIGHT / 2 - STREET * 3 / 4)]
DASHED_LANE = [(0, HEIGHT / 2 - STREET / 4, STRIPE * 2, STRIPE / 3),
               (0, HEIGHT / 2 + STREET / 4, STRIPE * 2, STRIPE / 3),
               (WIDTH / 2 + STREET * 5 / 4, HEIGHT / 2 - STREET / 4, STRIPE * 2, STRIPE / 3),
               (WIDTH / 2 + STREET * 5 / 4, HEIGHT / 2 + STREET / 4, STRIPE * 2, STRIPE / 3),
               (WIDTH / 2 - STREET / 4, 0, STRIPE / 3, STRIPE * 2),
               (WIDTH / 2 + STREET / 4, 0, STRIPE / 3, STRIPE * 2),
               (WIDTH / 2 - STREET / 4, HEIGHT / 2 + STREET * 5 / 4, STRIPE / 3, STRIPE * 2),
               (WIDTH / 2 + STREET / 4, HEIGHT / 2 + STREET * 5 / 4, STRIPE / 3, STRIPE * 2)]
CROSSWALK = [(WIDTH / 2 - STREET, (HEIGHT - STREET) / 2, STREET / 2, STRIPE),
             ((WIDTH + STREET) / 2, (HEIGHT - STREET) / 2, STREET / 2, STRIPE),
             ((WIDTH - STREET) / 2, HEIGHT / 2 - STREET, STRIPE, STREET / 2),
             ((WIDTH - STREET) / 2, (HEIGHT + STREET) / 2, STRIPE, STREET / 2)]
COUNT_POS = [(SIGNAL_POS[0][0] - 10, SIGNAL_POS[0][1] + 5, 20, 20),
             (SIGNAL_POS[1][0] - 10, SIGNAL_POS[1][1] - 25, 20, 20),
             (SIGNAL_POS[2][0] - 25, SIGNAL_POS[2][1] - 10, 20, 20),
             (SIGNAL_POS[3][0] + 5, SIGNAL_POS[3][1] - 10, 20, 20)]
CAR_LANES = [(WIDTH, int(HEIGHT / 2 - 3 * STREET / 8)),
             (WIDTH, int(HEIGHT / 2 - STREET / 8)),
             (0, int(HEIGHT / 2 + STREET / 8)),
             (0, int(HEIGHT / 2 + 3 * STREET / 8)),
             (int(WIDTH / 2 - 3 * STREET / 8), 0),
             (int(WIDTH / 2 - STREET / 8), 0),
             (int(WIDTH / 2 + STREET / 8), HEIGHT),
             (int(WIDTH / 2 + 3 * STREET / 8), HEIGHT)]

CARSIZE = [40, 20]
MAX_SPEED = 30
BTN_POS = [[20, 20], [61, 20], [102, 20]]
velocity = [10, 10]


# make a class of cars
class Cars(Sprite):

  def __init__(self, lane: int, speed=2):
    self.delay = 5
    self.speed = speed
    self.lane = lane
    if lane == 0 or lane == 1:
      self.origin = 'r'
      self.sign = -1
    elif lane == 2 or lane == 3:
      self.origin = 'l'
      self.sign = 1
    elif lane == 4 or lane == 5:
      self.origin = 'u'
      self.sign = 1
    else:
      self.origin = 'd'
      self.sign = -1
    Sprite.__init__(self)
    self.image = image.load('img/' + self.origin + 'car.png')
    self.x = int(CAR_LANES[lane][0])  # variable denoting x position of car
    self.y = int(CAR_LANES[lane][1])  # y position of car
    self.rect = self.image.get_rect(center=(self.x, self.y))  # used to place the car

    # car1.move(xp,signal_counter,car2)

  def move(self, xp, sgn, a):

    if self.x < 0 or self.x > WIDTH:
      self.x = int(CAR_LANES[self.lane][0])
    if self.y < 0 or self.y > HEIGHT:
      self.y = int(CAR_LANES[self.lane][1])

    if self.lane < 4:
      try:
        if HORMAP[self.lane][self.x + 40 * self.sign] == 0:
          self.x += self.sign * self.speed
          if self.lane > 1:
            self.rect.left = self.x
          else:
            self.rect.right = self.x
      except:
        self.x += self.sign * self.speed
        if self.lane > 1:
          self.rect.left = self.x
        else:
          self.rect.right = self.x
    else:
      try:
        if VERMAP[self.lane][self.y + 40 * self.sign] == 0:
          print(self.x,self.y)
          self.y += self.sign * self.speed
          if self.lane > 5:
            self.rect.bottom = self.y
          else:
            self.rect.top = self.y
      except:
        self.y += self.sign * self.speed
        if self.lane > 5:
          self.rect.bottom = self.y
        else:
          self.rect.top = self.y

    '''
    # if
    xp = self.x + xp  # new place for the car

    if xp > WIDTH:
      xp = xp - 1200
    dista = xp - a.x

    if sgn == 0 or sgn == 1:
      self.rect.left = xp*self.sign  # move the car
      self.x = xp  # update the car position
    elif sgn == 2:
      if self.x > WIDTH / 2 - STREET * 6 / 4:
        self.rect.left = xp
        self.x = xp
      elif self.x >= WIDTH / 2 - STREET * 6 / 4 and self.x <= 550:
        pass
      elif dista > -20 and dista < 20:  # to check nearby cars
        pass
      else:
        self.rect.left = xp
        self.x = xp'''


class Signal(Sprite):
  def __init__(self, x, y, origin):
    Sprite.__init__(self)
    self.origin = origin
    self.image = image.load('img/' + origin + 'red.png')
    self.rect = self.image.get_rect(center=(x, y))

  def change_sign(self, color):
    self.image = image.load('img/' + self.origin + color + '.png')
    if color == 'red':
      if self.origin == 'l' or self.origin == 'r':
        HORMAP[0][int(STOP_LANE[0][0]) + STRIPE] = 1
        HORMAP[1][int(STOP_LANE[0][0]) + STRIPE] = 1
        HORMAP[2][int(STOP_LANE[1][0])] = 1
        HORMAP[3][int(STOP_LANE[1][0])] = 1
      else:
        VERMAP[0][int(STOP_LANE[2][1])] = 1
        VERMAP[1][int(STOP_LANE[2][1])] = 1
        VERMAP[2][int(STOP_LANE[3][1]) + STRIPE] = 1
        VERMAP[3][int(STOP_LANE[3][1]) + STRIPE] = 1

    else:

      if self.origin == 'l' or self.origin == 'r':
        HORMAP[0][int(STOP_LANE[0][0]) + STRIPE] = 0
        HORMAP[1][int(STOP_LANE[0][0]) + STRIPE] = 0
        HORMAP[2][int(STOP_LANE[1][0])] = 0
        HORMAP[3][int(STOP_LANE[1][0])] = 0
      else:
        VERMAP[0][int(STOP_LANE[2][1])] = 0
        VERMAP[1][int(STOP_LANE[2][1])] = 0
        VERMAP[2][int(STOP_LANE[3][1]) + STRIPE] = 0
        VERMAP[3][int(STOP_LANE[3][1]) + STRIPE] = 0


class Watch(Sprite):
  def __init__(self, x, y):
    Sprite.__init__(self)
    self.image = image.load('img/off.png')
    self.rect = self.image.get_rect(center=(x, y))

  def change_num(self, num):
    self.image = image.load('img/' + str(num) + '.png')


class Button(Sprite):
  def __init__(self, button, x, y):
    Sprite.__init__(self)
    self.image = image.load('img/btn/' + button + '.png')
    self.rect = self.image.get_rect(center=(x, y))

  def hover(self, button):
    self.image = image.load('img/btn/' + button + '.png')


def drawBackground(frame, HEIGHT, WIDTH, STREET, STRIPE):
  frame.fill(BGCOLOR)

  # pygame.draw.rect(screen, color, (x,y,width,height), thickness)

  # Desenho das ruas
  pygame.draw.rect(frame, BLACK, STREET_POS[0], 0)
  pygame.draw.rect(frame, BLACK, STREET_POS[1], 0)

  # Desenho das faixas dupla contínuas na rua horizontal
  pygame.draw.rect(frame, YELLOW, DOUBLE_LANE[0], 0)  # desenho da faixa contínua
  pygame.draw.rect(frame, YELLOW, DOUBLE_LANE[1], 0)  # desenho da faixa contínua
  pygame.draw.rect(frame, YELLOW, DOUBLE_LANE[2], 0)
  pygame.draw.rect(frame, YELLOW, DOUBLE_LANE[3], 0)
  # Desenho das faixas dupla contínuas na rua vertical
  pygame.draw.rect(frame, YELLOW, DOUBLE_LANE[4], 0)
  pygame.draw.rect(frame, YELLOW, DOUBLE_LANE[5], 0)
  pygame.draw.rect(frame, YELLOW, DOUBLE_LANE[6], 0)
  pygame.draw.rect(frame, YELLOW, DOUBLE_LANE[7], 0)

  # Desenho das faixas de retenção na rua horizontal
  pygame.draw.rect(frame, WHITE, STOP_LANE[0], 0)
  pygame.draw.rect(frame, WHITE, STOP_LANE[1], 0)
  # Desenho das faixas de retenção na rua horizontal
  pygame.draw.rect(frame, WHITE, STOP_LANE[2], 0)
  pygame.draw.rect(frame, WHITE, STOP_LANE[3], 0)

  # Desenho das faixas tracejadas
  for i in range(int((WIDTH / 2 - STREET) // (STRIPE * 4)) - 1):
    pygame.draw.rect(frame, WHITE, tuple(map(sum, zip(DASHED_LANE[0], (i * 4 * STRIPE, 0, 0, 0)))), 0)
    pygame.draw.rect(frame, WHITE, tuple(map(sum, zip(DASHED_LANE[1], (i * 4 * STRIPE, 0, 0, 0)))), 0)
    pygame.draw.rect(frame, WHITE, tuple(map(sum, zip(DASHED_LANE[2], (i * 4 * STRIPE, 0, 0, 0)))), 0)
    pygame.draw.rect(frame, WHITE, tuple(map(sum, zip(DASHED_LANE[3], (i * 4 * STRIPE, 0, 0, 0)))), 0)

  for i in range(int((HEIGHT / 2 - STREET) // (STRIPE * 4)) - 1):
    pygame.draw.rect(frame, WHITE, tuple(map(sum, zip(DASHED_LANE[4], (0, i * 4 * STRIPE, 0, 0)))), 0)
    pygame.draw.rect(frame, WHITE, tuple(map(sum, zip(DASHED_LANE[5], (0, i * 4 * STRIPE, 0, 0)))), 0)

    pygame.draw.rect(frame, WHITE, tuple(map(sum, zip(DASHED_LANE[6], (0, i * 4 * STRIPE, 0, 0)))), 0)
    pygame.draw.rect(frame, WHITE, tuple(map(sum, zip(DASHED_LANE[7], (0, i * 4 * STRIPE, 0, 0)))), 0)

    # Desenho das faixas de pedestres
  for i in range(10):
    pygame.draw.rect(frame, WHITE, tuple(map(sum, zip(CROSSWALK[0], (0, i * STREET / 10, 0, 0)))), 0)
    pygame.draw.rect(frame, WHITE, tuple(map(sum, zip(CROSSWALK[1], (0, i * STREET / 10, 0, 0)))), 0)

    pygame.draw.rect(frame, WHITE, tuple(map(sum, zip(CROSSWALK[2], (i * STREET / 10, 0, 0, 0)))), 0)
    pygame.draw.rect(frame, WHITE, tuple(map(sum, zip(CROSSWALK[3], (i * STREET / 10, 0, 0, 0)))), 0)

  # Desenho do background do contador

  pygame.draw.rect(frame, BLACK, COUNT_POS[0], 0)
  pygame.draw.rect(frame, BLACK, COUNT_POS[1], 0)
  pygame.draw.rect(frame, BLACK, COUNT_POS[2], 0)
  pygame.draw.rect(frame, BLACK, COUNT_POS[3], 0)


def traffic():
  clock = pygame.time.Clock()  # load clock
  # datetime.date.timetuple(datetime.datetime.now())
  # time.struct_time(tm_year=2018, tm_mon=7, tm_mday=4, tm_hour=0, tm_min=0, tm_sec=0, tm_wday=2, tm_yday=185, tm_isdst=-1)
  start = datetime.date.timetuple(datetime.datetime.now())

  frame = pygame.display.set_mode((WIDTH, HEIGHT))
  display.set_caption(CAPTION)

  lwatch1 = Watch(SIGNAL_POS[0][0] - 5, SIGNAL_POS[0][1] + 15)
  lwatch2 = Watch(SIGNAL_POS[0][0] + 5, SIGNAL_POS[0][1] + 15)

  rwatch1 = Watch(SIGNAL_POS[1][0] - 5, SIGNAL_POS[1][1] - 15)
  rwatch2 = Watch(SIGNAL_POS[1][0] + 5, SIGNAL_POS[1][1] - 15)

  uwatch1 = Watch(SIGNAL_POS[2][0] - 20, SIGNAL_POS[2][1])
  uwatch2 = Watch(SIGNAL_POS[2][0] - 10, SIGNAL_POS[2][1])

  dwatch1 = Watch(SIGNAL_POS[3][0] + 10, SIGNAL_POS[3][1])
  dwatch2 = Watch(SIGNAL_POS[3][0] + 20, SIGNAL_POS[3][1])

  xp = 10

  car1 = Cars(0)
  car2 = Cars(1)
  car3 = Cars(2)
  car4 = Cars(3)
  car5 = Cars(4)
  car6 = Cars(5)
  car7 = Cars(6)
  car8 = Cars(7)

  lsignal = Signal(SIGNAL_POS[0][0], SIGNAL_POS[0][1], 'l')
  lsignal.change_sign('green')
  rsignal = Signal(SIGNAL_POS[1][0], SIGNAL_POS[1][1], 'r')
  rsignal.change_sign('green')
  usignal = Signal(SIGNAL_POS[2][0], SIGNAL_POS[2][1], 'u')
  dsignal = Signal(SIGNAL_POS[3][0], SIGNAL_POS[3][1], 'd')

  button0 = Button('stop', BTN_POS[0][0], BTN_POS[0][1])
  button1 = Button('pause', BTN_POS[1][0], BTN_POS[1][1])
  button2 = Button('play', BTN_POS[2][0], BTN_POS[2][1])

  all_cars = Group(car1, car2, car3, car4, car5, car6, car7, car8)
  all_signals = Group(lsignal, rsignal, usignal, dsignal)
  all_watches = Group(lwatch1, lwatch2, rwatch1, rwatch2, uwatch1, uwatch2, dwatch1, dwatch2)
  all_buttons = Group(button0, button1, button2)

  signal_counter = 0
  cont = 0
  green_time = 10
  yellow_time = 3
  red_time = 10
  total_time = green_time + red_time + yellow_time

  while True:

    now = datetime.datetime.timetuple(datetime.datetime.now())
    seconds = (now.tm_hour * 3600 + now.tm_min * 60 + now.tm_sec) - (
      start.tm_hour * 3600 + start.tm_min * 60 + start.tm_sec)
    rtime = seconds % total_time
    # flaggreen=0

    if rtime == 0:
      signal_counter = 0
      lsignal.change_sign('green')
      rsignal.change_sign('green')
      usignal.change_sign('red')
      dsignal.change_sign('red')
    elif rtime == green_time:
      signal_counter = 1
      lsignal.change_sign('yellow')
      rsignal.change_sign('yellow')
    elif rtime == green_time + yellow_time:
      signal_counter = 2
      lsignal.change_sign('red')
      rsignal.change_sign('red')
      usignal.change_sign('green')
      dsignal.change_sign('green')
    elif rtime == green_time + red_time:
      signal_counter = 2
      usignal.change_sign('yellow')
      dsignal.change_sign('yellow')

    if rtime < green_time:
      if cont != rtime:
        lwatch1.change_num(mt.floor((green_time - rtime) / 10))
        lwatch2.change_num(mt.floor((green_time - rtime) % 10))
        rwatch1.change_num(mt.floor((green_time - rtime) / 10))
        rwatch2.change_num(mt.floor((green_time - rtime) % 10))
        uwatch1.change_num('off')
        uwatch2.change_num('off')
        dwatch1.change_num('off')
        dwatch2.change_num('off')
      else:
        cont = rtime

    elif rtime < green_time + yellow_time:

      if cont != rtime:
        lwatch1.change_num('off')
        lwatch2.change_num('off')
        rwatch1.change_num('off')
        rwatch2.change_num('off')
      else:
        cont = rtime
    elif rtime < green_time + red_time:
      if cont != rtime:

        lwatch1.change_num('off')
        lwatch2.change_num('off')
        rwatch1.change_num('off')
        rwatch2.change_num('off')
        uwatch1.change_num(mt.floor((green_time + red_time - rtime) / 10))
        uwatch2.change_num(mt.floor((green_time + red_time - rtime) % 10))
        dwatch1.change_num(mt.floor((green_time + red_time - rtime) / 10))
        dwatch2.change_num(mt.floor((green_time + red_time - rtime) % 10))
      else:
        cont = rtime
    else:
      uwatch1.change_num('off')
      uwatch2.change_num('off')
      dwatch1.change_num('off')
      dwatch2.change_num('off')
    mouse_pos = mouse.get_pos()
    click = mouse.get_pressed()

    xp = 10

    drawBackground(frame, HEIGHT, WIDTH, STREET, STRIPE)
    # print(frame.get_at((int(WIDTH/2),int(HEIGHT/2))))
    car1.move(xp, signal_counter, car2)
    car2.move(xp, signal_counter, car3)
    car3.move(xp, signal_counter, car4)
    car4.move(xp, signal_counter, car1)
    car5.move(xp, signal_counter, car2)
    car6.move(xp, signal_counter, car3)
    car7.move(xp, signal_counter, car4)
    car8.move(xp, signal_counter, car1)
    e = event.pump()  # Don't ever remove this for Odin's sake!

    # Stop execution
    if BTN_POS[0][0] + 18 > mouse_pos[0] > BTN_POS[0][0] - 18 and BTN_POS[0][1] + 18 > mouse_pos[1] > BTN_POS[0][
      1] - 18:
      button0.hover('stoph')
      if click[0] == 1:
        break
    else:
      button0.hover('stop')
    # Pause execution
    if BTN_POS[1][0] + 18 > mouse_pos[0] > BTN_POS[1][0] - 18 and BTN_POS[1][1] + 18 > mouse_pos[1] > BTN_POS[1][
      1] - 18:
      button1.hover('pauseh')
      if click[0] == 1:
        while True:
          mouse_pos = mouse.get_pos()
          click = mouse.get_pressed()

          e = event.pump()  # Don't ever remove this for Odin's sake!
          if BTN_POS[0][0] + 18 > mouse_pos[0] > BTN_POS[0][0] - 18 and BTN_POS[0][1] + 18 > mouse_pos[1] > BTN_POS[0][
            1] - 18:
            button0.hover('stoph')
            if click[0] == 1:
              pygame.quit()
              quit()
          else:
            button0.hover('stop')
          if BTN_POS[2][0] + 18 > mouse_pos[0] > BTN_POS[2][0] - 18 and BTN_POS[2][1] + 18 > mouse_pos[1] > BTN_POS[2][
            1] - 18:
            button2.hover('playh')
            if click[0] == 1:
              button2.hover('play')
              start = datetime.date.timetuple(datetime.datetime.now())
              break
          else:
            button2.hover('play')

          drawBackground(frame, HEIGHT, WIDTH, STREET, STRIPE)
          all_cars.draw(frame)
          all_signals.draw(frame)
          all_watches.draw(frame)
          all_buttons.draw(frame)
          display.update()
          pygame.display.flip()
    else:
      button1.hover('pause')
    all_cars.draw(frame)
    all_signals.draw(frame)
    all_watches.draw(frame)
    all_buttons.draw(frame)
    display.update()
    pygame.display.flip()
  pygame.quit()
  quit()
  clock = pygame.time.Clock()  # load clock


if __name__ == '__main__':
  traffic()
