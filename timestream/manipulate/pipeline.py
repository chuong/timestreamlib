#coding=utf-8
# Copyright (C) 2014
# Author(s): Joel Granados <joel.granados@gmail.com>
#            Chuong Nguyen <chuong.v.nguyen@gmail.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import absolute_import, division, print_function

import numpy as np

from timestream.manipulate.pipecomponents import *

class ImagePipeline ( object ):
    complist = {
                 Tester.actName:                Tester, \
                 ImageUndistorter.actName:      ImageUndistorter,
                 ColorCardDetector.actName:     ColorCardDetector, \
                 ImageColorCorrector.actName:   ImageColorCorrector, \
                 TrayDetector.actName:          TrayDetector, \
                 PotDetector.actName:           PotDetector, \
                 PlantExtractor.actName:        PlantExtractor, \
                 ResultingImageWriter.actName:  ResultingImageWriter \
               }

    def __init__(self, settings):
        self.pipeline = []
        # Add elements while checking for dependencies
        for i, setElem in enumerate(settings):
            # First elements expects [ndarray]
            if i > 0:
                compExpects = ImagePipeline.complist[setElem[0]].runExpects
                prevReturns = self.pipeline[-1].__class__.runReturns
                if ( not isinstance(compExpects, list) \
                        or not isinstance(prevReturns, list) \
                        or len(compExpects) is not len(prevReturns) \
                        or not compExpects == prevReturns ):
                    raise ValueError("Dependancy error in pipeline")

            self.pipeline.append( ImagePipeline.complist[setElem[0]](**setElem[1]) )

    # contArgs: struct/class containing context arguments.
    #           Name are predefined for all pipe components.
    # initArgs: argument list to get the pipeline going.
    def process(self, contArgs, initArgs, visualise = False):
        # First elem with input image
        res = initArgs
        for elem in self.pipeline:
            res = elem(contArgs, *res)
            if visualise:
                elem.show()
        return (res)

    @classmethod
    def printCompList(cls):
        for clKey, clVal in ImagePipeline.complist.iteritems():
            print (clVal.info())

#def test():
#    from timestream.parse import ts_iter_images
#    settingFile = "/home/chuong/Workspace/traitcapture-bin/unwarp_rectify/data/pipeline.yml"
#    imageRootPath = '/mnt/phenocam/a_data/TimeStreams/BorevitzTest/BVZ0036/BVZ0036-GC02L~fullres-orig/'
#
#    img_iter = ts_iter_images(imageRootPath)
#    for i in range(750):
#        img_iter.next()
#    currentImage = cv2.imread(img_iter.next())[:,:,::-1]
#
#    ipl = ImagePipeline(settingFile)
#    context = {"filePath": os.path.dirname(settingFile)}
#    args = [currentImage]
#    ipl.process(context, args)
#
#if __name__ == "__main__":
#    test()