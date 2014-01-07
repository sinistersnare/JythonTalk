'''
If I was too stupid to get the live demo working :p

Mostly working, OK formatted, not very pythonic code!

@author: sinistersnare
'''

from contextlib import contextmanager

from com.badlogic.gdx import Application, ApplicationAdapter, Screen, Game
from com.badlogic.gdx.backends.lwjgl import LwjglApplication, LwjglApplicationConfiguration
from com.badlogic.gdx.utils import TimeUtils, Array
from com.badlogic.gdx.math import MathUtils, Rectangle, Vector3
from com.badlogic.gdx import ApplicationListener, Gdx, Input
from com.badlogic.gdx.graphics.g2d import SpriteBatch, BitmapFont
from com.badlogic.gdx.graphics import Texture, OrthographicCamera, GL10

WIDTH = 800
HEIGHT = 480
SPEED = 200
IMGLEN = 64

class DropGame(Game):

    def __init__(self):
        self.batch = None
        self.font = None

    def create(self):
        self.batch = SpriteBatch()
        self.font = BitmapFont()
        self.setScreen(MainMenuScreen(self))

   # def render(self):
    #    super(Game, self).render() # needs more python3!

    def dispose(self):
        self.batch.dispose()
        self.font.dispose()


class GameScreen(Screen):

    def __init__(self, game):
        """Dont need `create` in Screen instances. Constructor will do
         (even though __init__ isnt really a constructor...)
        """
        self.game = game

        self.dropimg = Texture("assets/droplet.png")
        self.bucketimg = Texture("assets/bucket.png")

        self.dropsound = Gdx.audio.newSound(Gdx.files.internal("assets/drop.wav"))
        self.rainmusic = Gdx.audio.newMusic(Gdx.files.internal("assets/rain.mp3"))
        self.rainmusic.setLooping(True)

        self.camera = OrthographicCamera()
        self.camera.setToOrtho(False, WIDTH, HEIGHT)

        self.bucket = Rectangle()
        self.bucket.x = 800 / 2 - 64 / 2 # initial starting point @ center of screen
        self.bucket.y = 20

        self.raindrops = Array()
        self.spawndrop()

        self.lastdroptime = 0
        self.dropsgathered = 0


    def spawndrop(self):
        raindrop = Rectangle() # no self! :p
        raindrop.x = MathUtils.random(0, WIDTH - 64) # screen X co-ords
        raindrop.y = HEIGHT # always spawns on top
        raindrop.width = raindrop.height = 64
        self.raindrops.add(raindrop)
        self.lastdroptime = TimeUtils.nanoTime()


    def render(self, delta):
        Gdx.gl.glClearColor(0, 0, 0.2, 1)
        Gdx.gl.glClear(GL10.GL_COLOR_BUFFER_BIT)

        self.camera.update()

        self.game.batch.setProjectionMatrix(self.camera.combined)

        SECOND = 1000000000 # nano-seconds
        DROPTIME = SECOND


        self.game.batch.begin() # much less verbose with a context manager....
        self.game.batch.draw(self.bucketimg, self.bucket.x, self.bucket.y)
        self.game.batch.end()
        with rend(self.game.batch) as btch: # don't add an "i"!
            self.game.font.draw(btch, "Drops Collected: {}".format(self.dropsgathered), 0, HEIGHT)
            btch.draw(self.bucketimg, self.bucket.x, self.bucket.y)
            for drop in self.raindrops:
                btch.draw(self.dropimg, drop.x, drop.y)


        if Gdx.input.isTouched():
            touchpos = Vector3()
            touchpos.set(Gdx.input.getX(), Gdx.input.getY(), 0)
            self.camera.unproject(touchpos)
            self.bucket.x = touchpos.x - (IMGLEN / 2)
        if Gdx.input.isKeyPressed(Input.Keys.LEFT):
            self.bucket.x -= self.SPEED * Gdx.graphics.getDeltaTime()
        if Gdx.input.isKeyPressed(Input.Keys.RIGHT):
            self.bucket.x += self.SPEED * Gdx.graphics.getDeltaTime()

        if self.bucket.x < 0: self.bucket.x = 0
        if self.bucket.x > (WIDTH - 64): self.bucket.x = WIDTH - 64

        if (TimeUtils.nanoTime() - self.lastdroptime) > DROPTIME: self.spawndrop()


        iterator = self.raindrops.iterator()
        while iterator.hasNext():
            raindrop = iterator.next()
            raindrop.y -= SPEED * Gdx.graphics.getDeltaTime();
            if (raindrop.y + IMGLEN) < 0: iterator.remove()
            if raindrop.overlaps(self.bucket):
                self.dropsound.play()
                iterator.remove()


    def resize(self, width, height):
        pass

    def show(self):
        self.rainmusic.play()

    def hide(self):
        pass

    def pause(self):
        pass

    def resume(self):
        pass

    def dispose(self):
        self.dropimg.dispose()
        self.bucketimg.dispose()
        self.dropsound.dispose()
        self.rainmusic.dispose()



class MainMenuScreen(Screen):
    def __init__(self, game):
        self.game = game

        self.camera = OrthographicCamera()
        self.camera.setToOrtho(False, 800, 400)


    def render(self, delta):
        Gdx.gl.glClearColor(0, 0, 0.2, 1)
        Gdx.gl.glClear(GL10.GL_COLOR_BUFFER_BIT)

        self.camera.update()
        self.game.batch.setProjectionMatrix(self.camera.combined)

        with rend(self.game.batch) as btch:
            self.game.font.draw(btch, "Welcome to Drop!", 100, 150)
            self.game.font.draw(btch, "Tap Anywhere to begin!", 100, 100)

        if Gdx.input.isTouched():
            self.game.setScreen(GameScreen(self.game))
            self.dispose()

    def resize(self, w, h):
        pass

    def show(self):
        pass

    def hide(self):
        pass

    def pause(self):
        pass

    def resume(self):
        pass

    def dispose(self):
        pass

class PyGDX(ApplicationAdapter):
    def __init__(self):
        self.camera = None
        self.batch = None
        self.texture = None
        self.bucketimg = None
        self.dropsound = None
        self.rainmusic = None
        self.bucket = None
        self.raindrops = None

        self.IMGLEN = 64 # width and height of bucket and drop
        self.SPEED = 200

        self.lastdrop = 0
        self.width = 800
        self.height = 480

    def spawndrop(self):
        raindrop = Rectangle()
        raindrop.x = MathUtils.random(0, self.width - self.IMGLEN) # can't be outside screen
        raindrop.y = self.height
        raindrop.width = self.IMGLEN
        raindrop.height = self.IMGLEN
        self.raindrops.add(raindrop)
        self.lastdrop = TimeUtils.nanoTime()

    def create(self):
        self.camera = OrthographicCamera()
        self.camera.setToOrtho(False, self.width, self.height)
        self.batch = SpriteBatch()

        self.dropimg = Texture("assets/droplet.png")
        self.bucketimg = Texture("assets/bucket.png")
        self.dropsound = Gdx.audio.newSound(Gdx.files.internal("assets/drop.wav"))
        self.rainmusic = Gdx.audio.newSound(Gdx.files.internal("assets/rain.mp3"))

        self.bucket = Rectangle()
        self.bucket.x = (self.width / 2) - (self.IMGLEN / 2) # center of screen
        self.bucket.y = 20 # how far up it is
        self.bucket.width = self.IMGLEN
        self.bucket.height = self.IMGLEN

        self.raindrops = Array()
        self.spawndrop()

        self.rainmusic.setLooping(True, True)
        self.rainmusic.play()

    def render(self):
        SECOND = 1000000000
        DROPTIME = SECOND / 6
        Gdx.gl.glClearColor(0, 0, 0.2, 0)
        Gdx.gl.glClear(GL10.GL_COLOR_BUFFER_BIT)

        self.camera.update()

        self.batch.setProjectionMatrix(self.camera.combined)
        self.batch.begin()
        self.batch.draw(self.bucketimg, self.bucket.x, self.bucket.y)
        for drop in self.raindrops:
            self.batch.draw(self.dropimg, drop.x, drop.y)
        self.batch.end()

        if Gdx.input.isTouched():
            touchpos = Vector3()
            touchpos.set(Gdx.input.getX(), Gdx.input.getY(), 0)
            self.camera.unproject(touchpos)
            self.bucket.x = touchpos.x - (self.IMGLEN / 2)
        if Gdx.input.isKeyPressed(Input.Keys.LEFT):
            self.bucket.x -= self.SPEED * Gdx.graphics.getDeltaTime()
        if Gdx.input.isKeyPressed(Input.Keys.RIGHT):
            self.bucket.x += self.SPEED * Gdx.graphics.getDeltaTime()

        if self.bucket.x < 0: self.bucket.x = 0
        if self.bucket.x > (self.width - self.IMGLEN): self.bucket.x = self.width - self.IMGLEN

        if (TimeUtils.nanoTime() - self.lastdrop) > DROPTIME: self.spawndrop()


        # rip from java, don't hate me ;)
        iterator = self.raindrops.iterator()
        while iterator.hasNext():
            raindrop = iterator.next()
            raindrop.y -= self.SPEED * Gdx.graphics.getDeltaTime();
            if (raindrop.y + self.IMGLEN) < 0: iterator.remove()
            if raindrop.overlaps(self.bucket):
                self.dropsound.play()
                iterator.remove()


    def dispose(self):
        self.batch.dispose()
        self.dropimg.dispose()
        self.bucketimg.dispose()
        self.dropsound.dispose()
        self.rainmusic.dispose()



@contextmanager
def rend(batch):
    """
    Really simple context manager to remove a ton of unnecessary clutter
    """
    try:
        batch.begin()
        yield batch
    finally:
        batch.end()



def main():

    cfg = LwjglApplicationConfiguration()
    cfg.title = "PyGdx";
    cfg.width = WIDTH
    cfg.height = HEIGHT

    LwjglApplication(DropGame(), cfg)

if __name__ == '__main__':
    main()
