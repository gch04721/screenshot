from PIL import ImageGrab, ImageTk, Image
from PIL import ImageStat, ImageChops
import os

class ImageControl():
    def __init__(self):
        self.image=None
        self.result=[]
        self.imgNum=0
        self.fullWidth, self.fullHeight=0,0

    def capture(self):
        self.image = ImageGrab.grab()
        return ImageTk.PhotoImage(self.image)
    
    def getImage(self, num):
        return ImageTk.PhotoImage(self.result[num])
    
    def capture_crop(self, x0=0, y0=0, width=0, height=0):
        area = (x0, y0, x0+width, y0+height)
        self.image = ImageGrab.grab()

        cropped_img = self.image.crop(area)
        if self.imgNum == 0:
            self.fullWidth = max(self.fullWidth, width)
            self.fullHeight += height
            self.result.append(cropped_img)
            self.imgNum += 1
        else:
            diff = ImageChops.difference(cropped_img, self.result[self.imgNum - 1])
            stat = ImageStat.Stat(diff)
            if stat.stddev > [8.0,8.0,8.0]:
                print('change detected: sum[%s]: %s' %(diff.getbands().__str__(), stat.stddev.__str__()))
                self.fullWidth = max(self.fullWidth, width)
                self.fullHeight += height
                self.result.append(cropped_img)
                self.imgNum += 1

        return ImageTk.PhotoImage(self.result[self.imgNum-1])

    def imageSave(self, fileLoc, fileName):
        canvas = Image.new("RGB", (self.fullWidth, min(self.fullHeight, 1600)), 'white')
        output_height = 0
        counter = 0
        for im in self.result:
            width, height = im.size
            canvas.paste(im, (0, output_height))
            output_height += height
            
            if output_height > 1450:
                canvas.save('{}/{}{}.jpg'.format(fileLoc, fileName, counter))
                counter += 1
                output_height =0
                canvas.close()
                canvas = Image.new("RGB", (self.fullWidth, min(self.fullHeight, 1600)), 'white')

        canvas.save('{}/{}{}.jpg'.format(fileLoc, fileName, counter))
