#!/usr/bin/python3
# -*- coding:utf-8 -*-

import xml.etree.ElementTree as ET
import os
import re

class Brief:
    @staticmethod
    def getText(briefElement):
        text = 'N/A'
        try:
            context = ''.join(briefElement.itertext())
            context = context.strip()             
            if len(context) > 0:
                text = context

        except (TypeError, AttributeError) as e:
            print(e)

        return text
    
    def __init__(self, briefElement):
        self.text = Brief.getText(briefElement)
    
    def __str__(self):
        string = "briefdescription: ".join(self.text)
        
        return string
        
class Detail:
    @staticmethod
    def getText(element, match):
        text = 'N/A'
        description = ''   
        try:    
            subs = element.findall(match)                
            for sub in subs:
                description = description + os.linesep + ''.join(sub.itertext())
            
            description = description.strip()            
            if len(description) > 0:
                text = description

        except (TypeError, AttributeError) as e:
            print(e)
                
        return text 
    
    def setDescription(self, detailElement):
        self.descrTitle = 'Description'
        self.descrText  = 'N/A'      
        try:
            subs = detailElement.findall('.//simplesect[@kind="par"]')
            for sub in subs:
                title = sub.findtext('./title')
                if title is not None: 
                    if re.search('^\s*[dD]escription[sS]*.*', title):
                        self.descrText = Detail.getText(sub, './para')                                            
            
        except (TypeError, AttributeError) as e:
            print(e)
            
        #print(self.descrTitle + ' : ' + os.linesep + self.descrText + os.linesep)
        
    def setBasicFlow(self, detailElement):
        self.basicTitle = 'Basic Flows'
        self.basicText  = 'N/A'      
        try:
            subs = detailElement.findall('.//simplesect[@kind="par"]')
            for sub in subs:
                title = sub.findtext('./title')
                if title is not None: 
                    if re.search('^\s*[bB]asic\s*[fF]low[sS]*.*', title):
                        self.basicText = Detail.getText(sub, './para')                                            
            
        except (TypeError, AttributeError) as e:
            print(e)
            
        #print(self.basicTitle + ' : ' + os.linesep + self.basicText + os.linesep)            

        
    def setFaultCase(self, detailElement):
        self.faultTitle = 'Fault Cases'
        self.faultText  = 'N/A'      
        try:
            subs = detailElement.findall('.//simplesect[@kind="par"]')
            for sub in subs:
                title = sub.findtext('./title')
                if title is not None: 
                    if re.search('^\s*[fF]ault[sS]*\s*[cC]ase[sS]*.*', title):
                        self.faultText = Detail.getText(sub, './para')                                            
            
        except (TypeError, AttributeError) as e:
            print(e)
            
        #print(self.faultTitle + ' : ' + os.linesep + self.faultText + os.linesep) 
           
    def setNote(self, detailElement):
        self.noteTitle = 'Note'
        self.noteText  = 'N/A'      
        try:
            self.noteText = Detail.getText(detailElement, './/simplesect[@kind="note"]/para')
                                      
            
        except (TypeError, AttributeError) as e:
            print(e)
            
        #print(self.noteTitle + ' : ' + os.linesep + self.noteText + os.linesep)  
        
    def setReturn(self, detailElement):        
        self.returnTitle = 'Return'
        self.hasReturn   = False
        self.returnType  = 'N/A'
        self.returnText  = 'N/A'      
        try:
            context = detailElement.findtext('.//simplesect[@kind="return"]/para', 'N/A')
            typeList = re.findall('^\s*([^\s:]*)[\s:*]', context)
            if len(typeList) > 0:
                self.returnType = typeList[0]
                self.hasReturn  = True
            
            self.returnText = Detail.getText(detailElement,'.//simplesect[@kind="return"]/para')   
        except (TypeError, AttributeError) as e:
            print(e)
            
        #print(self.returnTitle + ' : ' + os.linesep + self.returnType + os.linesep + self.returnText + os.linesep) 

    def setParamList(self, detailElement):        
        self.paramDict = {}  
        try:
            paramElement = detailElement.find('.//parameterlist[@kind="param"]')
            if paramElement is not None:                
                paramItems = paramElement.findall('./parameteritem')
                for paramItem in paramItems:
                    paraName      = paramItem.findtext('./parameternamelist/parametername', 'N/A')
                    
                    paraRange     = 'N/A'
                    paraDirection = 'N/A'

                                                              
                    parameterdescription = paramItem.findtext('./parameterdescription/para', 'N/A')
                    reList = re.findall('\[([^\]]*)\]', parameterdescription)
                    if len(reList)  == 1:
                        paraRange     = reList[0]
                    elif len(reList) == 2:
                        paraDirection = reList[0]
                        paraRange     = reList[1]
                    else:
                        pass
                    
                    paraDescr = 'N/A'
                    context = ''                    
                    descrElement = paramItem.findall('./parameterdescription/para/*')
                    
                    for elem in descrElement:
                        if elem.text is not None:
                            context = context + elem.text
                        if elem.tail is not None:
                            context = context + elem.tail
                    
                    context = context.strip()
                    if len(context) != 0:
                        paraDescr = context                                        
                                              
                    if paraName != 'N/A' and paraName != '' and paraName not in self.paramDict:
                        dictItem = {'name':paraName, 'range':paraRange, 'direction':paraDirection, 'descr':paraDescr}
                        self.paramDict[paraName] = dictItem
                    
        except (TypeError, AttributeError) as e:
            print('f', e)
            
                       
    def __init__(self, detailedElement):
        self.descrption = Detail.getText(detailedElement, '.') 
        Detail.setDescription(self, detailedElement)
        Detail.setBasicFlow(self, detailedElement)
        Detail.setFaultCase(self, detailedElement)
        Detail.setNote(self, detailedElement)
        Detail.setReturn(self, detailedElement)
        Detail.setParamList(self, detailedElement)
        Detail.setParamList(self, detailedElement)
        
    def __str__(self):        
        return self.descrption
           
class Item:
    @staticmethod
    def getAttrib(element, attrib):
        text = 'N/A'
        try:
            value = element.get(attrib)
            if value is not None:
                text = value
                
        except (TypeError, AttributeError, KeyError):
            print('can not get attributes: ' + attrib)

        return text
     
    @staticmethod
    def isStatic(element):      
        static = Item.getAttrib(element, 'static')
        if static == 'yes':
            isStatic = True
        else:
            isStatic = False

        return isStatic 
    
    @staticmethod
    def getText(element, match):
        text    = 'N/A'
        try:
            subs = element.findall(match)
            context = ''
            for sub in subs:
                context = context + ''.join(sub.itertext())
                context = context.strip()             
                if len(context) > 0:
                    text = context

        except (TypeError, AttributeError) as e:
            print(e)

        return text

    @staticmethod
    def getParamList(element):
        paramList = []
        try:
            childs = element.findall('param')
            if len(childs) > 0:
                for child in childs:
                    paraName = Item.getText(child, './declname')
                    if paraName == 'N/A':
                        paraName = Item.getText(child, './defname')
                       
                    paraType = Item.getText(child, './type')

                    if paraName != 'N/A':
                        paramList.append({'name': paraName, 'type':paraType})
                        
        except (TypeError, IndexError, AttributeError) as e:
            print(e)          
        
        return paramList 
    
    def __init__(self, element):
        self.isStatic   = Item.isStatic(element)
        
        self.id         = Item.getAttrib(element, 'id')
        self.kind       = Item.getAttrib(element, 'kind')
        
        self.name       = Item.getText(element, './name')
        self.type       = Item.getText(element, './type')
        self.definition = Item.getText(element, './definition')
        self.argString  = Item.getText(element, './argsstring')
        self.initializer= Item.getText(element, './initializer')
        self.paramList  = Item.getParamList(element)
        
        briefElement    = element.find('./briefdescription')
        if briefElement is not None:
            self.brief  = Brief(briefElement)
        else:
            self.brief  = None
            
        detailElement   = element.find('./detaileddescription')
        if detailElement is not None:
            self.detail = Detail(detailElement)
        else:
            self.detail = None


    def __str__(self):
        string = str(type(self)) + ':' 
        string = string + os.linesep + 'kind \t\t: ' + self.kind
        string = string + os.linesep + 'id \t\t: '   + self.id
        string = string + os.linesep + 'static \t\t: ' + str(self.isStatic)
        string = string + os.linesep + 'type \t\t: ' + self.type
        string = string + os.linesep + 'name \t\t: ' + self.name
        string = string + os.linesep + 'definition \t: ' + self.definition
        if self.kind == 'function' and self.argString != 'N/A':
            string = string + self.argString
        string = string + os.linesep + 'parameters \t: '
        
        if len(self.paramList) > 0:
            for param in self.paramList:
                string = string + param['type'] + ' ' + param['name'] + ' \t'
        else:
            string = string + 'N/A'
                
        string = string + os.linesep + 'initializer \t: ' + self.initializer
        
        string = string + os.linesep + 'brief \t\t: '
        if self.brief is not None:
            string = string + self.brief.text
        else:
            string = string + 'N/A'
            
        if self.detail is not None:    
            string = string + os.linesep + self.detail.__str__()
            
            
        return string

class Enum(Item):
    
    def __init__(self, element):
        Item.__init__(self, element)
        self.enumList = []
        try:
            enumValues = element.findall('./enumvalue')
            for each  in enumValues:
                enum = Item(each)
                self.enumList.append(enum)
                
        except (TypeError, AttributeError) as e:
            print(e)
        
        
    def __str__(self):
        string = ''.join(Item.__str__(self))
        for enum in self.enumList:
            string = string  + os.linesep + 'Enum Value \t: ' + enum.name + '\t\t' + enum.initializer
        return string 

if __name__ == '__main__':
    #xmlFile = './src/xml/um__rbuffer_8h.xml'
    #xmlFile = './src/xml/um__timer_8h.xml'
    xmlFile = './src/xml/um__isolation_8c.xml'
    tree = ET.parse(xmlFile)
    root = tree.getroot()
    
    D = {}
    for elem in root.findall('compounddef/sectiondef/memberdef[@kind="function"]/detaileddescription'):
        newItem = Detail(elem)
        print(newItem)
    
    

