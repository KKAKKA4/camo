from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.camera import Camera
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
import glob
import time

def export_to_png(self, filename, *args):
    '''Saves an image of the widget and its children in png format at the
    specified filename. Works by removing the widget canvas from its
    parent, rendering to an :class:`~kivy.graphics.fbo.Fbo`, and calling
    :meth:`~kivy.graphics.texture.Texture.save`.
    .. note::
        The image includes only this widget and its children. If you want to
        include widgets elsewhere in the tree, you must call
        :meth:`~Widget.export_to_png` from their common parent, or use
        :meth:`~kivy.core.window.Window.screenshot` to capture the whole
        window.
    .. note::
        The image will be saved in png format, you should include the
        extension in your filename.
    .. versionadded:: 1.8.1
    '''

    if self.parent is not None:
        canvas_parent_index = self.parent.canvas.indexof(self.canvas)
        self.parent.canvas.remove(self.canvas)

    fbo = Fbo(size=self.size)

    with fbo:
        ClearColor(0, 0, 0, 1)
        ClearBuffers()
        Translate(-self.x, -self.y, 0)

    fbo.add(self.canvas)
    fbo.draw()
    fbo.texture.save(filename)
    fbo.remove(self.canvas)

    if self.parent is not None:
        self.parent.canvas.insert(canvas_parent_index, self.canvas)

    return True


class MirrorCamera(Camera):
    def _camera_loaded(self, *largs):
        self.texture = self._camera.texture
        self.texture_size = list(self.texture.size)
        self.texture.flip_vertical()
   
class CameraWidget(BoxLayout):
    pass

class Image_Gallery(GridLayout):
    def __init__(self, **kwargs):
        super(Image_Gallery, self).__init__(**kwargs)
        images = glob.glob('./*.png') 
        self.cols = 3
        for img in images:
            print(1, img)
            thumb = MyImage(source=img)
            self.add_widget(thumb)
           

class MyImage(Image):
    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            print(self.source)


class Demo(ScreenManager):
    def capture(self):
        camera = self.ids['camera1']
        timestr = time.strftime("%Y%m%d_%H%M%S")
        camera.export_to_png("IMG_{}.png".format(timestr))
        print("Captured")

    def refresh(self):
        gallery = self.ids['gallery']
        gallery.__init__(gallery)


class DemoApp(App):

	def build(self):
		return Demo()

DemoApp().run()