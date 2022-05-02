from time import time


class AnimationSystem:
    def __init__(self, duration=10000):
        self.duration = duration
        self.playing = False
        self.loop = False
        self.reversePlaying = False
        self.last_started_at = 0
        self.last_timestamp = 0
        self.animatable_objects = []
        self.speed = 1

    def get_current_timestamp(self):
        return (time() * 1000 - self.last_started_at) if self.playing else self.last_timestamp

    def play(self, reverse=False):
        self.last_started_at = time() * 1000 - self.last_timestamp
        self.playing = True

    def pause(self):
        self.last_timestamp = self.get_current_timestamp()
        self.playing = False

    def stop(self):
        self.last_timestamp = 0
        self.playing = False
        [i.clear_footsteps() for i in self.animatable_objects]
        self.update()

    def update(self):
        if self.playing:
            t = self.get_current_timestamp()
            [i.update(t) for i in self.animatable_objects]
        elif self.last_timestamp == 0:
            [i.update(0) for i in self.animatable_objects]

    def draw(self, screen):
        [i.draw(screen, self.get_current_timestamp()) for i in self.animatable_objects]

    def add_animatable(self, model):
        self.animatable_objects.append(model)

    def set_speed(self, speed):
        self.speed = speed

    def get_speed(self):
        return self.speed

    def increase_speed_by(self, value):
        self.speed += value

    def decrease_speed_by(self, value):
        self.speed -= value

    def is_playing(self):
        return self.playing

    def is_paused(self):
        return not self.playing and self.last_timestamp

    def remove_objects(self):
        self.animatable_objects = []
        self.stop()