#!/usr/bin/python3
# -*- coding = utf-8 -*-

import sys
import os
import re

class Config:
    @staticmethod
    def __findAttriValue__(lines, attri):
        value = None
        patten = '^' + attri + '\s*=\s*(.*\S)\s*'
        for line in lines:
            temp = re.findall(patten, line)
            if len(temp) > 0:
                value = temp[0]
                #print(temp, value)
        return value

    @staticmethod
    def __setModuleNameList__(moduleName):
        moduleNameList = re.findall("([^\s,]+)[\s,]*",moduleName)
        #print(moduleNameList)
        return moduleNameList
    
    @staticmethod
    def __isSrcFileExist__(fileName, srcDir):
        srcFile = srcDir + '/' + fileName
        if os.path.isfile(srcFile):
            return True
        else:
            print('Can not find source file: ' + srcFile)
            return False

    @staticmethod
    def __setSrcFileList__(moduleNameList, srcDir):
        srcFileList = []
        for moduleName in moduleNameList:
            module, fileType = os.path.splitext(moduleName)
            fileType = fileType.lower()
            if len(fileType) > 0:
                srcFileName = module + fileType
                if Config.__isSrcFileExist__(srcFileName, srcDir):
                    srcFileList.append(srcFileName)
            else:
                srcFileName = moduleName + '.c'
                if Config.__isSrcFileExist__(srcFileName, srcDir):
                    srcFileList.append(srcFileName)

                srcFileName = moduleName + '.h'
                if Config.__isSrcFileExist__(srcFileName, srcDir):
                    srcFileList.append(srcFileName)

        return srcFileList;
    

    @staticmethod
    def __setXmlFileList__(srcFileList):
        xmlFileList = []
        for srcFile in srcFileList:
            src, fileType = os.path.splitext(srcFile)
            src = src.replace('_', '__')
            fileType = fileType.replace('.', '_8')
            xmlName = src + fileType + '.xml'
            xmlFileList.append(xmlName)

        return xmlFileList;
    
    @classmethod
    def __setProjectName__(cls, self, lines):
        value = cls.__findAttriValue__(lines, 'PROJECT_NAME')
        if value is not None:
            self.__projectName__ = value
        else:
            print('Can not find PROJECT_NAME in config file. Use default : ' + self.__projectName__)  

    @classmethod
    def __setBoardType__(cls, self, lines):
        value = cls.__findAttriValue__(lines, 'BOARD_TYPE')
        if value is not None:
            self.__boardType__ = value   
        else:
            print('Can not find BOARD_TYPE in config file. Use default : ' + self.__boardType__)

    @classmethod
    def __setDoxygen__(cls, self, lines):
        value = cls.__findAttriValue__(lines, 'DOXYGEN_PATH')
        if value is not None:
            if os.path.isdir(value):
                self.__doxygenPath__   = value
                self.__doxygen__       = value + '/doxygen'
                self.__doxygenConfig__ = value + '/doxygen.config'
            else:
                print(value + ' is not a valid dirctory. Use default dir for doxygen : ' + self.__doxygenPath__)
        else:
            print('Can not find DOXYGEN_PATH in config file.Use default dir for doxygen : ' + self.__doxygenPath__)

    @classmethod
    def __setModules__(cls, self, lines):
        value = cls.__findAttriValue__(lines, 'SRC_PATH')
        if value is not None:
            if os.path.isdir(value):
                self.__srcDir__ = value
                self.__xmlDir__ = value + '/xml'
            else:
                print(value + ' is not a valid dirctory. Use default dir for source file : ' + self.__srcDir__)
        else:
            print('Can not find SRC_PATH in config file.Use default dir for source file : ' + self.__srcDir__)

        value = cls.__findAttriValue__(lines, 'MODULE_NAME')
        if value is not None:
            self.__moduleName__     = value
            self.__moduleNameList__ = cls.__setModuleNameList__(self.__moduleName__)
        else:
            print('Can not file module name. Using all .c or .h file in dirctory : ', self.__srcDir__)
            self.__moduleName__  = ''
            for rootDir, subDir, fileList in os.walk(self.__srcDir__):
                for file in fileList:
                    if re.search('\.[cChH]', file):
                        self.__moduleNameList__.append(file)

        self.__srcFileList__ = cls.__setSrcFileList__(self.__moduleNameList__, self.__srcDir__)
        for src in self.__srcFileList__:
            absSrc = self.__srcDir__ + '/' + src
            self.__absSrcFileList__.append(absSrc)

        self.__xmlFileList__ = cls.__setXmlFileList__(self.__srcFileList__)
        for xml in self.__xmlFileList__:
            absXml = self.__xmlDir__ + '/' + xml
            self.__absXmlFileList__.append(absXml)


    @classmethod
    def __setDocx__(cls, self, lines):
        value = cls.__findAttriValue__(lines, 'DOCX_PATH')
        if value is not None:
            if os.path.isdir(value):
                self.__docxDir__ = value
            else:
                print(value + ' is not a valid dirctory. Use default dir for docx files : ' + self.__docxDir__)
        else:
            print('Can not find DOXC_PATH in config file.Use default dir for docx file : ' + self.__docxDir__)

        value = cls.__findAttriValue__(lines, 'TEMPLATE_DOC')
        if value is not None:
            absFilePath = self.__docxDir__ + '/' + value
            if os.path.isfile(absFilePath):
                self.__templateDocx__ = absFilePath
            else:
                print(value + ' is not valid. Use default file name for template files : ' + self.__templateDocx__)
        else:
            print('Can not find TEMPLATE_DOC in config file.Use default dir for source file : ' + self.__templateDocx__)
            

        value  = cls.__findAttriValue__(lines, 'OUTPUT_DOC')
        if value is not None:
            absFilePath = self.__docxDir__ + '/' + value
            self.__outputDocx__ = absFilePath
        else:
            print('Can not find OUTPUT_DOC in config file.Use default dir for source file : ' + self.__OutputDocx__)

    
    def __init__(self, configFile):
        self.__projectName__      = 'PROJECT'
        self.__boardType__        = 'BOARD'
        self.__doxygenPath__      = './bin'
        self.__doxygen__          = self.__doxygenPath__ + '/doxygen'
        self.__doxygenConfig__    = self.__doxygenPath__ + '/doxygen.config'
        self.__srcDir__           = '.'
        self.__xmlDir__           = './xml'
        self.__docxDir__          = '.'
        self.__moduleName__       = ''
        self.__moduleNameList__   = []
        self.__srcFileList__      = []
        self.__xmlFileList__      = []
        self.__absSrcFileList__   = []
        self.__absXmlFileList__   = []
        self.__templateDocx__     = self.__docxDir__ + '/template.docx'
        self.__outputDocx__       = self.__docxDir__ + '/default.docx'

        try:
            fp = open(configFile, 'r')
        except:
            print('Can not find configuration: ' + configFile)
            return
        else:
            lines = fp.readlines()
            fp.close()
        
        Config.__setProjectName__(self, lines)
        Config.__setBoardType__(self, lines)  
        Config.__setDoxygen__(self, lines)
        Config.__setModules__(self, lines)
        Config.__setDocx__(self, lines)
        
    def __str__(self):
        string = ''
        string = string + 'project name    : ' + self.__projectName__ + os.linesep
        string = string + 'borad type      : ' + self.__boardType__ + os.linesep
        string = string + 'doxygen path    : ' + self.__doxygen__+ os.linesep
        string = string + 'source path     : ' + self.__srcDir__ + os.linesep
        string = string + 'docx path       : ' + self.__docxDir__ + os.linesep
        string = string + 'template docx   : ' + self.__templateDocx__ + os.linesep
        string = string + 'Output docx     : ' + self.__outputDocx__ + os.linesep

        string = string + 'source files    : '
        for name in self.__srcFileList__:
            string = string + name + ' '
        string = string + os.linesep

        string = string + 'xml files       : '
        for name in self.__xmlFileList__:
            string = string + name + ' '

        return string
    
    def getProjectName(self):
        return self.__projectName__

    def getBoardType(self):
        return self.__boardType__

    def getDoxygen(self):
        return (self.__doxygen__, self.__doxygenConfig__)
    
    def getSrcDir(self):
        return (self.__srcDir__)

    def getSrcFileList(self):
        return self.__srcFileList__

    def getXmlFileList(self):
        return tuple(self.__xmlFileList__)
    
    def getAbsSrcFileList(self):
        return self.__absSrcFileList__

    def getAbsXmlFileList(self):
        return self.__absXmlFileList__

    def getTemplateDocx(self):
        return self.__templateDocx__

    def getOutputDocx(self):
        return self.__outputDocx__

if __name__ == '__main__':
    myConfig = Config('config.txt')
    print(myConfig)
