from random import randrange

from libs.animatable import *
from libs.animation import *
from libs.object import *

successes, failures = pygame.init()

w, h = (1280, 720)
screen = pygame.display.set_mode((w, h))
clock = pygame.time.Clock()
FPS = 1200

animation = AnimationSystem()
obj = Object()

a = Animatable(obj)
#               time in ms     position
translate_1 = [(0, np.array([0, 400])),
               [1000, np.array([100, 500])],
               [2000, np.array([200, 600])],
               [3000, np.array([300, 500])],
               [4000, np.array([400, 400])],
               [5000, np.array([500, 500])],
               [6000, np.array([600, 600])],
               [7000, np.array([700, 500])],
               [8000, np.array([100, 200])],
               [9000, np.array([500, 100])],
               [10000, np.array([350, 600])]]

#          time      color
colors = [[1000, (255, 0, 0)],
          [2000, (255, 255, 0)],
          [3000, (0, 234, 255)],
          [5000, (170, 0, 255)],
          [6000, (255, 127, 0)],
          [4000, (191, 255, 0)],
          [8000, (0, 149, 255)],
          [9000, (255, 0, 170)],
          [10000, (0, 120, 170)]]

scale = [[0, (1, 1)],
         [3000, (0.5, 3)],
         [6000, (2, 1)],
         [9000, (1, 2)]]

#  write Translation interpolation method
font = pygame.font.SysFont('Arial', 22)
i_methods = [LINEAR, CUBIC_SPLINE, B_SPLINE, CUBIC_BEZIER]


# pre defined keyframes
def sim_1():
    animation.add_animatable(a)
    for i in translate_1:
        a.translate(i[0], i[1])
    for i in colors:
        a.set_color(i[0], i[1])
    for i in scale:
        a.scale(i[0], i[1])


# random keyframes
def sim_2():
    animation.remove_objects()
    animation.add_animatable(a)
    for i in range(0, 19000, 1000):
        a.translate(i, np.array([randrange(12800) / 10, randrange(7200) / 10]))
        a.scale(i, np.array([randrange(100, 200) / 100, randrange(100, 200) / 100]))
        a.set_color(i, np.array([randrange(255), randrange(255), randrange(255)]))


# run simulation 1
sim_2()
state = 'Stopped'

if __name__ == '__main__':

    while True:
        clock.tick(FPS)
        screen.fill((0, 0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            elif event.type == pygame.KEYDOWN:

                if event.key == pygame.K_PLUS:
                    animation.increase_speed_by(0.2)
                elif event.key == pygame.K_MINUS:
                    animation.decrease_speed_by(0.2)

                elif event.key == pygame.K_SPACE:
                    if animation.playing:
                        animation.pause()
                        state = 'Paused'
                    else:
                        animation.play()
                        state = 'Playing'

                elif event.key == pygame.K_ESCAPE:
                    animation.stop()
                    state = 'Stopped'

                elif event.key == pygame.K_RETURN:
                    animation.stop()
                    i_methods.append(i_methods.pop(0))
                    int_method = i_methods[0]
                    a.set_translation_interpolation_method(int_method)
                    animation.play()
                    state = 'Playing'

                elif event.key == pygame.K_1:
                    animation.stop()
                    sim_1()
                elif event.key == pygame.K_2:
                    animation.stop()
                    sim_2()

        method_text = font.render(f'Interpolation method: {interpolation_methods[i_methods[0]]}', True, (255, 255, 255))
        screen.blit(method_text, (1000, 10))

        method_text = font.render(state, False, (0, 255, 255))
        screen.blit(method_text, (600, 10))

        animation.update()
        animation.draw(screen)

        pygame.display.update()
