# -*- coding: utf-8 -*-
from inits import *
from debug import printDEBUG
from translate import _
from os import listdir
import xml.etree.cElementTree as ET
from Tools.LoadPixmap import LoadPixmap

def getWidgetsDefinitions(fileXML): #/usr/local/e2/lib/enigma2/python/Plugins/Extensions/UserSkin//LCDskin/rec.widget.xml
    wDict = {}
    for fileName in listdir(fileXML):
        widgetActiveState='X'
        previewXML=None
        widgetXML=None
        widgetInitscript=None
        widgetName=None
        widgetPic='widget.png' #config.png
        widgetInfo=''
        printDEBUG(fileName)
        widgetFaultyAttrib=''
        if fileName.startswith('widget-') and fileName.endswith('.xml'):
            wgetfileName= PluginPath + '/LCDskin/' + fileName
            try:
                root = ET.parse(wgetfileName).getroot()
            except Exception, e:
                printDEBUG("ERROR loading widget data %s" % str(e))
                continue
            if 1:
                for child in root.findall('*'):
                    if child.tag == 'widgetInit' and 'script' in child.attrib :
                        widgetInitscript = child.attrib['script'].strip()
                    elif child.tag == 'previewXML' and 'name' in child[0].attrib :
                        widgetName = child[0].attrib['name']
                        if 'pixmap' in child[0].attrib :
                            child[0].attrib['pixmap'] = getPixmapPath(child[0].attrib['pixmap'])
                            widgetPic='pixmap.png'
                            if child[0].attrib['pixmap'].endswith('config.png'):
                                widgetInfo = _('pixmap path is incorrect')
                                widgetActiveState='?' #if ? needs configuration
                                widgetFaultyAttrib = 'pixmap'
                        if 'font' in child[0].attrib :
                            widgetPic='label.png'
                        previewXML = ET.tostring(child[0]).strip()
                    elif child.tag == 'widgetXML':
                        widgetXML = ET.tostring(child[0]).strip()
            if previewXML is not None and widgetXML is not None and widgetInitscript is not None and widgetName is not None:
                #widgetActiveState=X then widget disabled, ?-when attrib has wrong value
                #widgetPic = LoadPixmap(getPixmapPath(widgetPic)
                wDict[widgetName] = {'widgetPic': widgetPic,
                              'widgetActiveState':widgetActiveState,
                              'widgetDisplayName': _(widgetName),
                              'widgetInfo':widgetInfo,
                              'widgetInitscript':widgetInitscript,
                              'previewXML':previewXML,
                              'widgetXML':widgetXML,
                              'wgetfileName':wgetfileName,
                              'widgetParams':getWidgetParams(previewXML),
                              'widgetFaultyAttrib':widgetFaultyAttrib
                              }
    return wDict

def getWidgetParams(previewXML):
    params = [(_('Widget attributes:'),)]
    root = ET.ElementTree(ET.fromstring(previewXML)).getroot()
    knownAttribs=('position','size','pixmap')
    hiddenAttributes=('name')
    for param in knownAttribs:
        if param in root.attrib:
            params.append((param + ' = ' + root.attrib[param],))
    for param in root.attrib:
        if param not in knownAttribs and param not in hiddenAttributes:
            params.append((param + ' = ' + root.attrib[param],))
            
    return params