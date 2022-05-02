import pygame
from libs.timeline import *
from libs.object import Object


class Animatable:
    def __init__(self, target: Object):
        self.target = target
        self.translateTimeline = TranslateTimeline(1, 1, method=LINEAR)
        self.scaleTimeline = ScaleTimeline(1, 1, method=LINEAR)
        self.colorTimeline = ColorTimeline(1, 1, method=LINEAR)
        self.footsteps = []

    def translate(self, timestamp=0, destination=np.array([0, 0, 0])):
        self.translateTimeline.addKeyframe(Keyframe(timestamp, destination))

    def set_color(self, timestamp=0, color=np.array([255, 255, 255])):
        self.colorTimeline.addKeyframe(Keyframe(timestamp, color))

    def scale(self, timestamp=0, scale=np.array([0, 0, 0])):
        self.scaleTimeline.addKeyframe(Keyframe(timestamp, scale))

    def update(self, t):
        self.target.set_translation((self.translateTimeline.get_pos(t)))
        self.target.set_color((self.colorTimeline.get_color(t)))
        self.target.set_scale((self.scaleTimeline.get_scale(t)))

    def draw(self, screen, current_timestamp):
        fs = self.translateTimeline.get_footsteps()
        cs = self.colorTimeline.get_footsteps()
        for i in range(len(fs)-1):
            p1 = (fs[i][0],  screen.get_height() - fs[i][1])
            p2 = (fs[i+1][0],  screen.get_height() - fs[i+1][1])
            try:
                pygame.draw.line(screen, cs[i+1], p1, p2)
            except:
                ...
        cps = self.translateTimeline.get_control_points()
        for i in range(len(cps)):
            pygame.draw.circle(screen, (0, 255, 0), (cps[i][0],  screen.get_height() - cps[i][1]), 1)
            font = pygame.font.SysFont('Arial', 16)
            time_left = self.translateTimeline.timestamps[i] - current_timestamp

            if time_left > 0:
                num = font.render(str(int(time_left/100)/10), True, (0, 255, 0))
                screen.blit(num, (cps[i][0],  screen.get_height() - cps[i][1]))
        self.target.draw(screen)

    def clear_footsteps(self):
        self.translateTimeline.clear_footsteps()
        self.scaleTimeline.clear_footsteps()
        self.colorTimeline.clear_footsteps()

    def get_translation_interpolation_method(self):
        return self.translateTimeline.get_interpolation_method()

    def set_translation_interpolation_method(self, method):
        return self.translateTimeline.set_interpolation_method(method)

    def is_active(self, t_ms):
        return min(self.translateTimeline.timestamps) <= t_ms <= max(self.translateTimeline.timestamps)

    def reset(self, t_ms):
        return min(self.translateTimeline.timestamps) <= t_ms <= max(self.translateTimeline.timestamps)