#!/usr/bin/python3
# -*- coding = utf-8 -*-

import os
import re

class Doxygen:
    @staticmethod
    def __setOutputFormat__(outFormat):
        if outFormat == 'xml':
            Out = 'GENERATE_XML'
        elif outFormat == 'rtf':
            Out = 'GENERATE_RTF'
        elif outFormat == 'html':
            Out = 'GENERATE_HTML'
        elif outFormat == 'latex':
            Out = 'GENERATE_LATEX'
        else:
            Out = None
        
        return Out

    @staticmethod
    def __addOutputFormat__(lines, outFormat):
        idx = 0
        Out = Doxygen.__setOutputFormat__(outFormat)
        if Out is not None:
            patten = '^' + Out + '\s+'
            for line in lines:
                if len(re.findall(patten, line)) > 0:
                    lines[idx] = Out + ' = ' + 'YES\n'
                idx = idx + 1
        else:
            print(outFormat + ' is not supported!! Use: xml, html, rtf or latex')

    @staticmethod
    def __delOutputFormat__(lines, outFormat):
        idx = 0
        Out = Doxygen.__setOutputFormat__(outFormat)
        if Out is not None:
            patten = '^' + Out + '\s+'
            for line in lines:
                if len(re.findall(patten, line)) > 0:
                    lines[idx] = Out + ' = ' + 'NO\n'
                idx = idx + 1
        else:
            print(outFormat + ' is not supported!! Use: xml, html, rtf or latex')

    @staticmethod
    def __setDirectory__(lines, inputDir, outputDir):  
        inputDirectoryName = 'INPUT'
        outDirectoryName   = 'OUTPUT_DIRECTORY'  
        idx = 0
        for line in lines:
            inputPatten  = '^' + inputDirectoryName + '\s+'
            outputPatten = '^' + outDirectoryName + '\s+'
            if len(re.findall(inputPatten, line)) > 0:
                lines[idx] =inputDirectoryName + ' = ' + inputDir + '\n'

            if len(re.findall(outputPatten, line)) > 0:
                lines[idx] = outDirectoryName + ' = ' + outputDir + "\n"

            idx = idx + 1

    @classmethod
    def __run__(cls, self):
        doxygenCmd = self.__elf__ + ' ' + self.__config__
        if os.path.isfile(self.__elf__) and os.path.isfile(self.__config__):
            os.system(doxygenCmd)
        else:
            print('Can not run doxygen command: ' + doxygenCmd)

    @classmethod
    def __generateConfig__(cls, self):
        doxygenCmd = self.__elf__ + ' -g ' + self.__config__
        if os.path.isfile(self.__elf__):
            os.system(doxygenCmd)
        else:
            print('Can not run doxygen command: ' + doxygenCmd)

    @classmethod
    def __modifyConfig__(cls, self): 
        try:      
            fp = open(self.__config__, 'r+')
        except:
            print('Can not open config file: ' + self.__config__)
            return

        lines = fp.readlines()
        fp.close()

        Doxygen.__setDirectory__(lines, self.__input__, self.__output__)
        Doxygen.__addOutputFormat__(lines, 'xml')
        Doxygen.__delOutputFormat__(lines, 'html')
        Doxygen.__delOutputFormat__(lines, 'rtf')
        Doxygen.__delOutputFormat__(lines, 'latex')

        try:      
            fp = open(self.__config__, 'w')
        except:
            print('Can not open config file: ' + self.__config__)
            return

        fp.writelines(lines)

        fp.close

    
    def __init__(self):
        self.__elf__    = ''
        self.__config__ = ''
        self.__input__  = ''
        self.__output__ = ''

    
    def setDirectory(self, elfPath, configPath, inputPath, outputPath):
        if os.path.exists(elfPath):
            self.__elf__    = elfPath
            self.__config__ = configPath
            self.__input__  = inputPath
            self.__output__ = outputPath
            return True
        else:
            print(elfPath + ' is NOT valid!!')
            return False

    @staticmethod
    def generateInputFiles(fileList):
        inputFiles = ''
        for file in fileList:
            inputFiles = inputFiles + ' ' + file
        return inputFiles
   
    def generateXML(self):
        Doxygen.__generateConfig__(self)
        Doxygen.__modifyConfig__(self)
        Doxygen.__run__(self)


if __name__ == '__main__':
    import config

    configFile = input('Please input path of configuration file: ')

    myConfig = config.Config(configFile)

    inputPath = ''
    for src in myConfig.__absSrcFileList__:
        inputPath = inputPath + src + ' '
    
    doxygen = Doxygen()
    
    doxygenPath = myConfig.getDoxygen()
    
    inputFiles  = Doxygen.generateInputFiles(myConfig.getAbsSrcFileList())

    srcDir      = myConfig.getSrcDir()

    doxygen.setDirectory(doxygenPath[0], doxygenPath[1], inputFiles, srcDir)

    doxygen.generateXML()

    
