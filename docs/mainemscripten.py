from panda3d.core import loadPrcFileData
loadPrcFileData("", "textures-power-2 up")
loadPrcFileData("", "show-frame-rate-meter f")
loadPrcFileData("", "win-size 1000 800")
loadPrcFileData("", "preload-textures 0")
loadPrcFileData("", "compressed-textures 1")
loadPrcFileData("", "allow-incomplete-render 1")
from direct.showbase.ShowBase import ShowBase
from panda3d.core import *
from direct.gui.OnscreenText import OnscreenText
from direct.gui.DirectGui import *
from direct.task import Task
from direct.showbase.DirectObject import DirectObject
import sys
import emscripten

class MyApp(ShowBase):

    def __init__(self):
        ShowBase.__init__(self)
        wp = WindowProperties()
        wp.setSize(1000,800)
        self.win.requestProperties(wp)
        self.loadingText=OnscreenText("Loading...",1,fg=(1,1,1,1),pos=(0,0),align=TextNode.ACenter,scale=.07,mayChange=1)
        base.graphicsEngine.renderFrame()
        base.graphicsEngine.renderFrame()
        base.graphicsEngine.renderFrame() 
        base.graphicsEngine.renderFrame()
        url = "JohnPsalms.mf"
        handle = emscripten.async_wget2(url, "JohnPsalms.mf", onload=self.onload, onerror=self.onerror, onprogress=self.onprogress)
    def onload(self, handle, file):
        vfs = VirtualFileSystem.getGlobalPtr()
        vfs.mount(Filename("JohnPsalms.mf"), ".", VirtualFileSystem.MFReadOnly)
        self.loadingText.removeNode()
        self.LoadUpApp()
    def onprogress(self, handle, progress):
        print("Downloading files for the program")
    def onerror(self, handle, code):
        print("Download Error")       
    def LoadUpApp(self):
        # setup the scene
        self.scene = self.loader.loadModel("models/book.bam")
        self.scene.reparentTo(self.render)
        self.scene.setScale(2, 2, 2)
        self.scene.setTwoSided(True)
        self.scene.setLightOff(True)
        self.scene.setPos(0, 4.5, 0)
        self.scene.setHpr(0, 80, 0)
        # current page int
        self.currentpage = 1;
        # for bible image viewer
        self.currentbibleimage = 1;
        # load up first 2 pages
        tex = loader.loadTexture("psalms/PsalmsJohn1.jpg")
        self.scene.find("**/pageone").setTexture(tex, 1)
        tex = loader.loadTexture("psalms/PsalmsJohn2.jpg")
        self.scene.find("**/pagetwo").setTexture(tex, 1)
        # keyboard input
        self.accept("arrow_right", self.NextPage)
        self.accept("arrow_left", self.PreviousPage)
        self.accept("escape", self.ShowSettings)
        # buttons
        self.b = DirectButton(text=("<--"),pos=(-1.12,-0.95,-0.95), scale=.15, command=self.PreviousPage)
        self.b2 = DirectButton(text=("-->"),pos=(1.12,-0.95,-0.95), scale=.15, command=self.NextPage)
        self.b3 = DirectButton(text=("Settings"),pos=(0,0.85,0.85), scale=.08, command=self.ShowSettings)
        self.b12 = DirectButton(text=("Reset View"),pos=(0,0.85,-0.95), scale=.08, command=self.ResetView)
        
        # stuff for 2d viewer
        self.PsalmsFrame = DirectScrolledFrame()
        self.PsalmsFrame.hide()
        # update task
        taskMgr.add(self.update, "Update")
    def ResetView(self):
        self.trackball.node().set_pos(0, 0, 0)
        self.trackball.node().set_hpr(0, 0, 0)
    def ShowSettings(self):
         self.scene.hide()
         self.b.hide()
         self.b2.hide()
         self.b3.hide()
         self.b12.hide()
         
         self.b4 = DirectButton(text=("Hide Settings"),pos=(0,0.85,0.85), scale=.08, command=self.HideSettings)
         self.b5 = DirectButton(text=("View This Document In 2D (like a pdf)"),pos=(0,0.85,0.65), scale=.08, command=self.Show2DViewer)
         self.b6 = DirectButton(text=("View Bible Image Gallery"),pos=(0,0.85,0.45), scale=.08, command=self.ShowBibleImageGallery)
         self.b7 = DirectButton(text=("Hide All Buttons (you can use the escape key to show this menu)"),pos=(0,0.85,0.25), scale=.08, command=self.HideNavButtons)
         self.b8 = DirectButton(text=("Quit"),pos=(0,0.85,-0.05), scale=.08, command=sys.exit)
    def HideSettings(self):
        self.scene.show()
        self.b.show()
        self.b2.show()
        self.b3.show()
        self.b4.hide()
        self.b5.hide()
        self.b6.hide()
        self.b7.hide()
        self.b8.hide()
        self.b12.show()
        
    def HideNavButtons(self):
        self.scene.show()
        self.b.hide()
        self.b2.hide()
        self.b3.hide()
        self.b4.hide()
        self.b5.hide()
        self.b6.hide()
        self.b7.hide() 
        self.b8.hide()
        self.b12.hide()
        
    def Show2DViewer(self):        
        self.b.hide()
        self.b2.hide()
        self.b3.hide()
        self.b4.hide()
        self.b5.hide()
        self.b6.hide()
        self.b7.hide() 
        self.b8.hide()
        self.b12.hide()
        
        self.scene.hide()
        self.LoadPsalmsFrame()
        self.b9 = DirectButton(text=("Back"),pos=(1,0.85,0.85), scale=.08, command=self.Hide2DViewer)
        for x in range(148):
            if x != 0:
                self.image = self.loadImageAsPlane("psalms/PsalmsJohn" + str(x) + ".jpg")
                self.image.reparentTo(aspect2d)
                self.image.reparentTo(self.PsalmsFrame.getCanvas())    
                offset = 722.5
                self.image.setPos(1.4,0,offset + (-5 * x))
                self.image.setScale(1)
    def ShowBibleImageGallery(self):        
        self.b.hide()
        self.b2.hide()
        self.b3.hide()
        self.b4.hide()
        self.b5.hide()
        self.b6.hide()
        self.b7.hide() 
        self.b8.hide()
        self.b12.hide()
        
        self.scene.hide()
        self.b9 = DirectButton(text=("Back"),pos=(1,0.85,0.85), scale=.08, command=self.HideBibleImageGallery)  
        self.b10 = DirectButton(text=("<--"),pos=(-1.12,-0.95,-0.95), scale=.15, command=self.PreviousBibleImage)
        self.b11 = DirectButton(text=("-->"),pos=(1.12,-0.95,-0.95), scale=.15, command=self.NextBibleImage) 
        self.currentbibleimage = 1;
        self.image = self.loadImageAsPlane("psalms/BibleImages/" + str(self.currentbibleimage) + ".jpg")
        self.image.reparentTo(render)    
        self.image.setPos(0,7.5,0)   
        base.camera.setPos(0,0,0)
        base.camera.setHpr(0,0,0)
    def PreviousBibleImage(self):
        self.currentbibleimage = self.currentbibleimage - 1;
        if self.currentbibleimage <= 0:
            self.currentbibleimage = 1
        self.image.removeNode()
        self.image = self.loadImageAsPlane("psalms/BibleImages/" + str(self.currentbibleimage) + ".jpg")
        self.image.reparentTo(render) 
        self.image.setPos(0,7.5,0)   
        base.camera.setPos(0,0,0)
        base.camera.setHpr(0,0,0) 
    def NextBibleImage(self):
        self.currentbibleimage = self.currentbibleimage + 1;
        if self.currentbibleimage >= 12:
            self.currentbibleimage = 11
        self.image.removeNode()
        self.image = self.loadImageAsPlane("psalms/BibleImages/" + str(self.currentbibleimage) + ".jpg")
        self.image.reparentTo(render)
        self.image.setPos(0,7.5,0)   
        base.camera.setPos(0,0,0)
        base.camera.setHpr(0,0,0)
    def Hide2DViewer(self):        
       self.PsalmsFrame.hide()
       self.scene.show()
       self.b.show()
       self.b2.show()
       self.b3.show()
       self.b12.show()
       
       self.b9.hide()
       base.camera.setPos(0,0,0)
       base.camera.setHpr(0,0,0)
    def HideBibleImageGallery(self):        
       self.image.removeNode()
       self.scene.show()
       self.b.show()
       self.b2.show()
       self.b3.show()
       self.b12.show()
       
       self.b9.hide()
       self.b10.hide()
       self.b11.hide()
       base.camera.setPos(0,0,0)
       base.camera.setHpr(0,0,0)
    def NextPage(self):
         self.currentpage = self.currentpage + 2
         if self.currentpage >= 146:
             self.currentpage = 146
         tex = loader.loadTexture("psalms/PsalmsJohn" + str(self.currentpage) + ".jpg")
         self.scene.find("**/pageone").setTexture(tex, 1)
         tex = loader.loadTexture("psalms/PsalmsJohn" + str(self.currentpage + 1) + ".jpg")
         self.scene.find("**/pagetwo").setTexture(tex, 1)
    def PreviousPage(self):
       self.currentpage = self.currentpage - 2
       if self.currentpage <= 1:
           self.currentpage = 1
       tex = loader.loadTexture("psalms/PsalmsJohn" + str(self.currentpage) + ".jpg")
       self.scene.find("**/pageone").setTexture(tex, 1)
       tex = loader.loadTexture("psalms/PsalmsJohn" + str(self.currentpage + 1) + ".jpg")
       self.scene.find("**/pagetwo").setTexture(tex, 1)
    def LoadPsalmsFrame(self):
        self.PsalmsFrame.show()
        self.PsalmsFrame.removeNode()
        self.PsalmsFrame = DirectScrolledFrame(canvasSize=(0, 0, -20, 720), frameSize=(-1.45, 1.45, -1.5, 1.5),verticalScroll_resizeThumb=(False))
        #self.PsalmsFrame.setPos(-1.2, 0, -0)
        self.PsalmsFrame.setScale(0.6) 
    def loadImageAsPlane(self, filepath, yresolution = 600):
        tex = loader.loadTexture(filepath)
        tex.setBorderColor(Vec4(0,0,0,0))
        tex.setWrapU(Texture.WMBorderColor)
        tex.setWrapV(Texture.WMBorderColor)
        cm = CardMaker(filepath + " card")
        cm.setFrame(-tex.getOrigFileXSize(), tex.getOrigFileXSize(), -tex.getOrigFileYSize(), tex.getOrigFileYSize())
        card = NodePath(cm.generate())
        card.setTexture(tex)
        card.setTransparency(1)
        card.setScale(card.getScale()/ yresolution)
        card.flattenLight()
        return card
    def update(self, task):
       dt = globalClock.get_dt()
       is_down = self.mouseWatcherNode.is_button_down 
       if is_down(KeyboardButton.ascii_key("s")):
           if (self.scene.getP() >= 10):
               self.scene.set_p(self.scene, -20 * dt)  
           else:
               self.scene.setP(10)     
       if is_down(KeyboardButton.ascii_key("w")):
           if (self.scene.getP() >= 10):
               self.scene.set_p(self.scene, +20 * dt)
           else:
               self.scene.setP(10)
       if is_down(KeyboardButton.down()):
           if (self.scene.getP() >= 10):
               self.scene.set_p(self.scene, -20 * dt)  
           else:
               self.scene.setP(10)     
       if is_down(KeyboardButton.up()):
           if (self.scene.getP() >= 10):
               self.scene.set_p(self.scene, +20 * dt)
           else:
               self.scene.setP(10)
       return Task.cont 
app = MyApp()
app.run()