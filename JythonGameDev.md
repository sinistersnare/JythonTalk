% Creating Games With Python And Java
% Davis Silverman



About Me
==================

* Amateur programmer and game developer
* High school now, college in the future
* Seeking a job as a developer! *wink wink, nudge nudge*

Jython
======

* CPython is the reference implementation for Python.
* Jython is a Python implementation in Java
* Offers superb interoperability with Java libraries, along with the amazing benefits of the JVM
* 2.7 betas are out!

Comparisons of CPython and Jython
=================================

```
#Jython                  |  #CPython
def fibonacci():         |  def fibonacci():
    a, b = 0, 1          |      a, b = 0, 1  
    while True:          |      while True:
        yield a          |          yield a
        a, b = b, a + b  |          a, b = b, a + b
```



LibGDX
======

* A cross-platform Java game development framework based on OpenGL (ES) that works on Windows, Linux, Mac OS X, Android, your WebGL enabled browser and iOS.


![libgdx png][gdx.png]

doesnt work :(

My Work with LibGDX
===================

* Translated the LibGDX wiki (GoogleCode -> Github)
* Worked on Polyglot LibGDX (as shown in this very talk!)
* Regular on IRC
* Started Game-dev club at my school to teach and create games with LibGDX


LibGDX Classes Of Use
=====================

* `ApplicationListener` is the base java interface for a LibGDX game
* `OrthographicCamera` for camera magic
* `SpriteBatch` to draw on the screen
* Standard math classes `Vector2`, `Rectangle`, etc.


Small example!
==============

* Small game from wiki translated to Python
* To the demo! (lets hope this works!)


Limitations of LibGDX with Jython
=================================

* GWT
   * This backend is java only, so HTML LibGDX backend is a pipe dream


Future
======

* Android Support
   * Once jython can attain DynamicProxy support, it might be possible to have Jython on android!

* iOS support
    * the RoboVM backend runs the Android class library, so if it can anddroid, theres a good chance it can iOS!

* packaging
    * There has been some work on compiling/packaging jython into jars, this will make distribution of your awesome Python games very easy!


   

Links!
======

* Jython: http://jython.org
* Jython Book: http://www.jython.org/jythonbook/en/1.0/
* LibGDX: http://libgdx.badlogicgames.com/
* LibGDX Wiki: https://github.com/libgdx/libgdx/wiki







