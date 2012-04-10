#  Licensed to the Apache Software Foundation (ASF) under one
#  or more contributor license agreements.  See the NOTICE file
#  distributed with this work for additional information
#  regarding copyright ownership.  The ASF licenses this file
#  to you under the Apache License, Version 2.0 (the
#  "License"); you may not use this file except in compliance
#  with the License.  You may obtain a copy of the License at
#
#  http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing,
#  software distributed under the License is distributed on an
#  "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
#  KIND, either express or implied.  See the License for the
#  specific language governing permissions and limitations
#  under the License.


from xml.sax.handler import ContentHandler,EntityResolver
from ComponentParameters import ComponentParameters
from ConnectorParameters import ConnectorParameters
from TemplateAssetParameters import TemplateAssetParameters
from Borg import Borg

def a2i(spLabel):
  if spLabel == 'Low':
    return 1
  elif spLabel == 'Medium':
    return 2
  elif spLabel == 'High':
    return 3
  else:
    return 0

def it2Id(itLabel):
  if itLabel == 'required':
    return 1
  else:
    return 0

class ComponentModelContentHandler(ContentHandler,EntityResolver):
  def __init__(self):
    self.theAssets = []
    self.theComponents = []
    self.theConnectors = []
    self.resetComponentAttributes()
    self.resetAssetAttributes()
    self.resetSecurityPropertyAttributes()
    self.resetConnectorAttributes()
    b = Borg()
    self.configDir = b.configDir

  def resolveEntity(self,publicId,systemId):
    return self.configDir + '/component_model.dtd'

  def assets(self):
    return self.theAssets

  def components(self):
    return self.theComponents

  def connectors(self):
    return self.theConnectors

  def resetComponentAttributes(self):
    self.inDescription = 0
    self.theName = ''
    self.theDescription = ''
    self.theInterfaces = []
    self.theStructure = []
    self.theRequirements = []
    self.resetStructure()
    self.resetRequirement()

  def resetStructure(self):
    self.theHeadName = ''
    self.theHeadAdornment = ''
    self.theHeadNav = ''
    self.theHeadNry = ''
    self.theHeadRole = ''
    self.theTailRole = ''
    self.theTailNry = ''
    self.theTailNav = ''
    self.theTailAdornment = ''
    self.theTailName = ''

  def resetRequirement(self):
    self.inDescription = 0
    self.inRationale = 0
    self.inFitCriterion = 0
    self.theAsset = ''
    self.theType = ''
    self.theReqName = ''
    self.theDescription = ''
    self.theRationale = ''
    self.theFitCriterion = ''

  def resetAssetAttributes(self):
    self.inDescription = 0
    self.inSignificance = 0
    self.theName = ''
    self.theShortCode = ''
    self.theAssetType = ''
    self.theDescription = ''
    self.theSignificance = ''
    self.theInterfaces = []
    self.theSecurityProperties = []

  def resetSecurityPropertyAttributes(self):
    self.thePropertyName = ''
    self.thePropertyValue = 'None'
    self.inRationale = 0
    self.theRationale = ''


  def resetConnectorAttributes(self):
    self.theName = ''
    self.theFromName = ''
    self.theFromInterface = ''
    self.theToName = ''
    self.theToInterface = ''


  def startElement(self,name,attrs):
    if (name == 'component'):
      self.theName = attrs['name']
    elif (name == 'description'):
      self.inDescription = 1
      self.theDescription = ''
    elif (name == 'fit_criterion'):
      self.inFitCriterion = 1
      self.theFitCriterion = ''
    elif name == 'significance':
      self.inSignificance = 1
      self.theSignificance = ''
    elif name == 'rationale':
      self.inRationale = 1
      self.theRationale = ''
    elif name == 'interface':
      self.theInterfaces.append((attrs['name'],it2Id(attrs['type'])))
    elif name == 'asset':
      self.theName = attrs['name']
      self.theShortCode = attrs['short_code']
      self.theAssetType = attrs['type']
      self.theSecurityProperties = []
    elif name == 'security_property':
      self.thePropertyName = attrs['property']
      self.thePropertyValue = attrs['value']
    elif (name == 'connector'):
      self.theName = attrs['name']
      self.theFromName = attrs['from_component']
      self.theFromInterface = attrs['from_interface']
      self.theToName = attrs['to_component']
      self.theToInterface = attrs['to_interface']
    elif name == 'structure':
      self.theHeadName = attrs['head_asset']
      self.theHeadAdornment = attrs['head_adornment']
      self.theHeadNav = attrs['head_nav']
      rawHeadNry = attrs['head_nry']
      if (rawHeadNry == 'a'):
        rawHeadNry = '*'
      elif (rawHeadNry == '1..a'):
        rawHeadNry = '1..*'
      self.theHeadNry = rawHeadNry
      self.theHeadRole = attrs['head_role']
      self.theTailRole = attrs['tail_role']
      rawTailNry = attrs['tail_nry']
      if (rawTailNry == 'a'):
        rawTailNry = '*'
      elif (rawTailNry == '1..a'):
        rawTailNry = '1..*'
      self.theTailNry = rawTailNry
      self.theTailNav = attrs['tail_nav']
      self.theTailAdornment = attrs['tail_adornment']
      self.theTailName = attrs['tail_asset']
    elif name == 'requirement':
      self.theReqName = attrs['name']
      self.theAsset = attrs['asset']
      rawType = attrs['type']
      self.theType = rawType.replace('_',' ')

  def characters(self,data):
    if self.inDescription:
      self.theDescription += data
    elif self.inSignificance:
      self.theSignificance += data
    elif self.inRationale:
      self.theRationale += data
    elif self.inFitCriterion:
      self.theFitCriterion += data


  def endElement(self,name):
    if (name == 'component'):
      p = ComponentParameters(self.theName,self.theDescription,self.theInterfaces)
      self.theComponents.append(p)
      self.resetComponentAttributes() 
    elif name == 'asset':
      spDict = {}
      spDict['confidentiality'] = (0,'None')
      spDict['integrity'] = (0,'None')
      spDict['availability'] = (0,'None')
      spDict['accountability'] = (0,'None')
      spDict['anonymity'] = (0,'None')
      spDict['pseudonymity'] = (0,'None')
      spDict['unlinkability'] = (0,'None')
      spDict['unobservability'] = (0,'None')
      for sp in self.theSecurityProperties:
        spName = sp[0]
        spValue = a2i(sp[1])
        spRationale = sp[2]
        if spName in spDict:
          spDict[spName] = (spValue,spRationale)
      spValues = [] 
      spValues.append(spDict['confidentiality'])
      spValues.append(spDict['integrity'])
      spValues.append(spDict['availability'])
      spValues.append(spDict['accountability'])
      spValues.append(spDict['anonymity'])
      spValues.append(spDict['pseudonymity'])
      spValues.append(spDict['unlinkability'])
      spValues.append(spDict['unobservability'])
      p = TemplateAssetParameters(self.theName,self.theShortCode,self.theDescription,self.theSignificance,self.theAssetType,spValues,self.theInterfaces)
      self.theAssets.append(p)
      self.resetAssetAttributes()
    elif name == 'security_property':
      self.theSecurityProperties.append((self.thePropertyName,self.thePropertyValue,self.theRationale))
      self.resetSecurityPropertyAttributes()
    elif name == 'structure':
      self.theStructure.append((self.theHeadName,self.theHeadAdornment,self.theHeadNav,self.theHeadNry,self.theHeadRole,self.theTailRole,self.theTailNry,self.theTailNav,self.theTailAdornment,self.theTailName))
      self.resetStructure()
    elif name == 'requirement':
      self.theRequirements.append((self.theReqName,self.theDescription,self.theType,self.theRationale,self.theFitCriterion,self.theAsset))
      self.resetRequirement()
    elif name == 'connector':
      p = ConnectorParameters(self.theName,self.theFromName,self.theFromInterface,self.theToName,self.theToInterface)
      self.theConnectors.append(p)
      self.resetConnectorAttributes() 
    elif name == 'description':
      self.inDescription = 0
    elif name == 'rationale':
      self.inRationale = 0
    elif name == 'significance':
      self.inSignificance = 0
    elif name == 'fit_criterion':
      self.inFitCriterion = 0
