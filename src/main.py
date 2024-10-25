import json.tool
import os
import sys
import shutil
from PyQt5 import QtWidgets
from PyQt5.QtGui import QPixmap
from tkinter import filedialog
from ui import Ui_MainWindow
import json

class app():
    def __init__(self):
        super(app, self).__init__()
        
        self.blocks = {}
        self.texture = {"0": "", "1": "", "2": "", "3": "", "4": "", "5": ""}

        self.app = QtWidgets.QApplication(sys.argv)
        self.app.setStyle("Fusion")
        self.mainwindow = QtWidgets.QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.mainwindow)
        self.mainwindow.show()

        self.ui.actionImport_from_mrdt.triggered.connect(self.imported)
        self.ui.actionExport_to_mrdt_2.triggered.connect(self.export)

        self.checkAdd()
        self.checkRemove()
        self.checkGenerate()
        self.checkResourceEnabled()
        self.checkTextures()

        self.app.exec()
    
    def checkTextures(self):
        self.ui.topFaceBtn.clicked.connect(lambda: self.getTexture("4"))
        self.ui.bottomFaceBtn.clicked.connect(lambda: self.getTexture("5"))
        self.ui.rightFaceBtn.clicked.connect(lambda: self.getTexture("1"))
        self.ui.leftFaceBtn.clicked.connect(lambda: self.getTexture("3"))
        self.ui.frontFaceBtn.clicked.connect(lambda: self.getTexture("2"))
        self.ui.backFaceBtn.clicked.connect(lambda: self.getTexture("0"))
    
    def getTexture(self, id):
        self.id = id
        self.texture[self.id] = filedialog.askopenfile(filetypes=[("PNG File", "*.png")], defaultextension=[("PNG File", "*.png")]).name
        self.pixmap = QPixmap(self.texture[self.id]).scaled(41, 41, aspectRatioMode=True)
        if self.id == "0":
            self.ui.backFace.setPixmap(self.pixmap)
        elif self.id == "1":
            self.ui.rightFace.setPixmap(self.pixmap)
        elif self.id == "2":
            self.ui.frontFace.setPixmap(self.pixmap)
        elif self.id == "3":
            self.ui.leftFace.setPixmap(self.pixmap)
        elif self.id == "4":
            self.ui.topFace.setPixmap(self.pixmap)
        elif self.id == "5":
            self.ui.bottomFace.setPixmap(self.pixmap)
        
    
    def imported(self):
        self.iFile = filedialog.askopenfile(filetypes=[("mDirt File", "*.mdrt")], defaultextension=[("mDirt File", "*.mdrt")])  #.replace("/","\\")
        self.packProperties = json.load(self.iFile)
        self.ui.packName.setText(self.packProperties["packName"])
        self.ui.packNamespace.setText(self.packProperties["packNamespace"])
        self.ui.packDescription.setText(self.packProperties["packDescription"])
        self.ui.packVersion.setCurrentText(self.packProperties["packVersion"])
        self.blocks = self.packProperties["blcks"]
        for self.block in self.blocks:
            self.ui.blockList.addItem(self.blocks[self.block]["name"])
        
    def export(self):
        self.eFile = filedialog.asksaveasfile(filetypes=[("mDirt File", "*.mdrt")], defaultextension=[("mDirt File", "*.mdrt")])
        self.packProperties = {"packName": self.ui.packName.text(), "packNamespace": self.ui.packNamespace.text(), "packDescription": self.ui.packDescription.text(), "packVersion": self.ui.packVersion.currentText(), "blcks": self.blocks}
        self.eFile.write(str(self.packProperties).replace("'", '"'))
        self.eFile.close()
    
    def checkAdd(self):
        self.ui.buttonAddBlock.clicked.connect(self.addBlock)
    
    def checkRemove(self):
        self.ui.buttonRemoveBlock.clicked.connect(self.removeBlock)
    
    def checkGenerate(self):
        self.ui.buttonGeneratePack.clicked.connect(self.generate)

    def checkResourceEnabled(self):
        self.ui.blockResourceCheckBox.clicked.connect(self.toggleResource)
        if self.ui.blockResourceCheckBox.isChecked():
            self.ui.blockTextureLabel.setEnabled(True)
            self.ui.blockModelLabel.setEnabled(True)
            self.ui.blockModel.setEnabled(True)
        else:
            self.ui.blockTextureLabel.setEnabled(False)
            self.ui.blockModelLabel.setEnabled(False)
            self.ui.blockModel.setEnabled(False)
    
    def toggleResource(self):
        if self.ui.blockResourceCheckBox.isChecked():
            self.ui.blockTextureLabel.setEnabled(True)
            self.ui.blockModelLabel.setEnabled(True)
            self.ui.blockModel.setEnabled(True)
            self.ui.backFace.setEnabled(True)
            self.ui.backFaceBtn.setEnabled(True)
            self.ui.frontFace.setEnabled(True)
            self.ui.frontFaceBtn.setEnabled(True)
            self.ui.leftFace.setEnabled(True)
            self.ui.leftFaceBtn.setEnabled(True)
            self.ui.rightFace.setEnabled(True)
            self.ui.rightFaceBtn.setEnabled(True)
            self.ui.topFace.setEnabled(True)
            self.ui.topFaceBtn.setEnabled(True)
            self.ui.bottomFace.setEnabled(True)
            self.ui.bottomFaceBtn.setEnabled(True)
        else:
            self.ui.blockTextureLabel.setEnabled(False)
            self.ui.blockModelLabel.setEnabled(False)
            self.ui.blockModel.setEnabled(False)
            self.ui.backFace.setEnabled(False)
            self.ui.backFaceBtn.setEnabled(False)
            self.ui.frontFace.setEnabled(False)
            self.ui.frontFaceBtn.setEnabled(False)
            self.ui.leftFace.setEnabled(False)
            self.ui.leftFaceBtn.setEnabled(False)
            self.ui.rightFace.setEnabled(False)
            self.ui.rightFaceBtn.setEnabled(False)
            self.ui.topFace.setEnabled(False)
            self.ui.topFaceBtn.setEnabled(False)
            self.ui.bottomFace.setEnabled(False)
            self.ui.bottomFaceBtn.setEnabled(False)

    def addBlock(self):
        self.textureNames = {"0": "", "1": "", "2": "", "3": "", "4": "", "5": ""}
        for text in self.texture.keys():
            self.val = self.texture[text]
            self.textureNames[text] = os.path.splitext(os.path.basename(str(self.val)))[0]
        
        self.blockProperties = {
            "name": self.ui.blockName.text(),
            "displayName": self.ui.blockDisplayName.text(),
            "customModelData": self.ui.blockCMD.text(),
            "baseBlock": self.ui.blockBase.text(),
            "blockDrop": self.ui.blockDrop.text(),
            "texturePaths": self.texture,
            "textures": self.textureNames
        }

        self.blocks[self.ui.blockName.text()] = self.blockProperties
        
        self.ui.blockList.addItem(self.blockProperties["name"])
    
    def removeBlock(self):
        self.curItem = self.ui.blockList.currentRow()
        self.blocks.pop(self.ui.blockList.item(self.curItem).text())
        self.ui.blockList.takeItem(self.curItem)
    
    def generateResourcePack(self):
        self.outputDir = filedialog.askdirectory().replace("/", "\\")
        self.packDir = os.path.join(self.outputDir, self.ui.packName.text() + "Resource Pack")
        os.mkdir(self.packDir)
        os.mkdir(self.packDir + "\\assets")
        os.mkdir(self.packDir + "\\assets\\minecraft")
        os.mkdir(self.packDir + "\\assets\\minecraft\\models")
        os.mkdir(self.packDir + "\\assets\\minecraft\\textures")
        os.mkdir(self.packDir + "\\assets\\minecraft\\textures\\item")
        os.mkdir(self.packDir + "\\assets\\minecraft\\models\\item")
        os.mkdir(self.packDir + "\\assets\\minecraft\\models\\" + self.nameSpace)
        with open(f'{self.packDir}\\pack.mcmeta', 'w') as pack:
            pack.write('{\n    "pack": {\n        "pack_format": 42,\n        "description": "' + self.ui.packDescription.text() + '"\n    }\n}\n')
            pack.close()
        with open(f'{self.packDir}\\assets\\minecraft\\models\\item\\item_frame.json', 'a') as file:
            file.write('{"parent": "minecraft:item/generated","textures": {"layer0": "minecraft:item/item_frame"},"overrides":[')
            for block in self.blocks:
                file.write('{ "predicate": { "custom_model_data": ' + self.blocks[block]["customModelData"] + '}, "model": "' + self.nameSpace + '/' + self.blocks[block]["name"] + '"}')
                if block != next(reversed(self.blocks.keys())):
                    file.write(',')
            file.write(']}')
            file.close()
        for self.block in self.blocks:
            self.texture = self.packDir + "\\assets\\minecraft\\textures\\item\\" #+ self.blocks[block]["name"] + ".png"
            for path in self.blocks[block]["texturePaths"].values():
                if not os.path.exists(os.path.join(self.texture, os.path.splitext(os.path.basename(str(path)))[-2] + ".png")):
                    shutil.copy(path, os.path.join(self.texture, os.path.splitext(os.path.basename(str(path)))[-2] + ".png"))
            with open(f'{self.packDir}\\assets\\minecraft\\models\\'+ self.nameSpace + '\\' + self.blocks[block]["name"] + '.json', 'w') as file:
                file.write('{"credit": "Made with mDirt","textures": {"0": "' + self.blocks[block]["textures"][0] + '","1": "' + self.blocks[block]["textures"][1] + '","2": "' + self.blocks[block]["textures"][2] + '","3": "' + self.blocks[block]["textures"][3] + '","4": "' + self.blocks[block]["textures"][4] + '","5": "' + self.blocks[block]["textures"][5] + '","particle": "' + self.blocks[block]["textures"][0] + '"},"elements": [{"from": [0, 0, 0],"to": [16, 16, 16],"faces": {"north": {"uv": [0, 0, 16, 16], "texture": "#0"},"east": {"uv": [0, 0, 16, 16], "texture": "#1"},"south": {"uv": [0, 0, 16, 16], "texture": "#2"},"west": {"uv": [0, 0, 16, 16], "texture": "#3"},"up": {"uv": [0, 0, 16, 16], "texture": "#4"},"down": {"uv": [0, 0, 16, 16], "texture": "#5"}}}],"display": {"thirdperson_righthand": {"rotation": [0, 0, -55],"translation": [0, 2.75, -2.5],"scale": [0.4, 0.4, 0.4]},"thirdperson_lefthand": {"rotation": [0, 0, -55],"translation": [0, 2.75, -2.5],"scale": [0.4, 0.4, 0.4]},"firstperson_righthand": {"rotation": [0, 45, 0],"scale": [0.4, 0.4, 0.4]},"ground": {"translation": [0, 3.25, 0],"scale": [0.4, 0.4, 0.4]},"gui": {"rotation": [28, 45, 0],"scale": [0.6, 0.6, 0.6]}}}')
                file.close()
        
    
    def generate(self):

        self.nameSpace = self.ui.packNamespace.text()

        if self.ui.blockResourceCheckBox.isChecked():
            self.generateResourcePack()

        self.outputDir = filedialog.askdirectory().replace("/", "\\")
        self.packDir = os.path.join(self.outputDir, self.ui.packName.text())
        os.mkdir(self.packDir)
        os.mkdir(self.packDir + "\\data")
        self.packNamespace = os.path.join(self.packDir, "data", self.nameSpace)
        self.minecraft = os.path.join(self.packDir, "data", "minecraft")
        os.mkdir(self.minecraft)
        os.mkdir(self.packNamespace)
        with open(f'{self.packDir}\\pack.mcmeta', 'w') as pack:
            pack.write('{\n    "pack": {\n        "pack_format": 57,\n        "description": "' + self.ui.packDescription.text() + '"\n    }\n}\n')
            pack.close()
        
        os.mkdir(self.packNamespace + "\\function")
        os.mkdir(self.packNamespace + "\\loot_table")
        os.mkdir(self.packNamespace + "\\advancement")

        os.mkdir(self.minecraft + "\\tags")
        os.mkdir(self.minecraft + "\\tags" + "\\function")

        with open(f'{self.packNamespace}\\function\\tick.mcfunction', 'w') as tick:
            tick.write('# Generated by mDirt!\nexecute as @e[type=item_display,tag=' + self.nameSpace + ".custom_block] at @s run function " + self.nameSpace + ":as_blocks")
            tick.close()
        with open(f'{self.packNamespace}\\function\\load.mcfunction', 'w') as load:
            load.write('# Generated by mDirt!\ntellraw @a {"text":"[mDirt] - Successfully loaded pack!","color":"red"}')
            load.close()
        with open(f'{self.minecraft}\\tags\\function\\tick.json', 'w') as tickJS:
            tickJS.write('{\n    "values":[\n        ' + f'"{self.nameSpace}' + ':tick"\n        ]\n    }')
            tickJS.close()
        with open(f'{self.minecraft}\\tags\\function\\load.json', 'w') as loadJS:
            loadJS.write('{\n    "values":[\n        ' + f'"{self.nameSpace}' + ':load"\n        ]\n    }')
            loadJS.close()
        
        # Placed Item Frame Advancement

        with open(f'{self.packNamespace}\\advancement\\placed_item_frame.json', 'w') as file:
            file.write('{"criteria": {"requirement": {"trigger": "minecraft:item_used_on_block","conditions": {"location": [{"condition": "minecraft:match_tool","predicate": {"items": ["minecraft:item_frame"]}}]}}},"rewards": {"function": "' + self.nameSpace + ':placed_item_frame"}}')
            file.close()
        
        # Placed Item Frame Function

        with open(f'{self.packNamespace}\\function\\placed_item_frame.mcfunction', 'w') as file:
            file.write('advancement revoke @s only ' + self.nameSpace + ':placed_item_frame\nexecute as @e[tag=' + self.nameSpace + '.item_frame_block,distance=..10] at @s run function ' + self.nameSpace + ':check_placed_item_frame')
            file.close()

        # Check Placed Item Frame, block/place Functions

        with open(f'{self.packNamespace}\\function\\check_placed_item_frame.mcfunction', 'a') as file:
            for self.blck in self.blocks.keys():
                os.mkdir(self.packNamespace + "\\function" + f"\\{self.blck}")
                with open(f'{self.packNamespace}\\function\\{self.blck}\\place.mcfunction', 'w') as file2:
                    file2.write("setblock ~ ~ ~ " + self.blocks[self.blck]["baseBlock"] + ' keep\nsummon item_display ~ ~ ~ {brightness:{sky:15,block:0},Tags:["' + self.nameSpace + f'.{self.blocks[self.blck]["name"]}","' + self.nameSpace + '.custom_block"],transformation:{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],translation:[0f,0.469f,0f],scale:[1.001f,1.001f,1.001f]},item:{id:"minecraft:item_frame",count:1,components:{"minecraft:custom_model_data":' + self.blocks[self.blck]["customModelData"] + '}}}\n')
                    file2.close()
                file.write('execute as @s[tag=' + self.nameSpace + '.' + self.blocks[self.blck]["name"] + '] run function ' + self.nameSpace + ':' + self.blocks[self.blck]["name"] + '/place\n')
            
            file.write('\nkill @s')
            file.close()
        
        # As Blocks block/block, block/break Functions

        with open(f'{self.packNamespace}\\function\\as_blocks.mcfunction', 'a') as file:
            for self.blck in self.blocks.keys():
                with open(f'{self.packNamespace}\\function\\{self.blck}\\{self.blck}.mcfunction', 'w') as file2:
                    file2.write('execute unless block ~ ~ ~ ' + self.blocks[self.blck]["baseBlock"] + ' run function ' + self.nameSpace + ':' + self.blocks[self.blck]["name"] + '/break')
                    file2.close()
                with open(f'{self.packNamespace}\\function\\{self.blck}\\break.mcfunction', 'a') as file3:
                    file3.write('execute as @e[type=item,sort=nearest,limit=1,distance=..2,nbt={OnGround:0b,Age:0s,Item:{id:"' + self.blocks[self.blck]["baseBlock"] + '"}}] run kill @s\n')
                    file3.write('loot spawn ~ ~ ~ loot ' + self.nameSpace + ':' + self.blocks[self.blck]["name"] + '\n')
                    file3.write('kill @s')
                    file3.close()
                
                file.write('execute as @s[tag=' + self.nameSpace + '.' + self.blocks[self.blck]["name"] + '] run function ' + self.nameSpace + ':' + self.blocks[self.blck]["name"] + '/' + self.blocks[self.blck]["name"] + '\n')
            file.close()
        
        # Give Items Function

        with open(f'{self.packNamespace}\\function\\give_items.mcfunction', 'a') as file:
            for self.blck in self.blocks.keys():
                file.write('give @s item_frame[custom_name=\'{"italic":false,"text":"' + self.blocks[self.blck]["displayName"] + '"}\',custom_model_data=' + self.blocks[self.blck]["customModelData"] + ',entity_data={id:"minecraft:item_frame",Fixed:1b,Invisible:1b,Silent:1b,Invulnerable:1b,Facing:1,Tags:["' + self.nameSpace + '.item_frame_block","' + self.nameSpace + '.' + self.blocks[self.blck]["name"] + '"]}] 1\n')
            file.close()
        
        # Loot Tables

        for self.blck in self.blocks.keys():
            with open(f'{self.packNamespace}\\loot_table\\{self.blocks[self.blck]["name"]}.json', 'w') as file:
                if self.blocks[self.blck]["blockDrop"] == "":
                    file.write('{"pools": [{"rolls": 1,"entries": [{"type": "minecraft:item","name": "minecraft:item_frame"}],"functions": [{"function": "minecraft:set_components","components": {"minecraft:custom_model_data": ' + self.blocks[self.blck]["customModelData"] + ',"minecraft:custom_name": "{\\"italic\\":false,\\"text\\":\\"' + self.blocks[self.blck]["displayName"] + '\\"}","minecraft:entity_data": {"id": "minecraft:item_frame","Fixed": true,"Invisible": true,"Silent": true,"Invulnerable": true,"Facing": 1,"Tags": ["' + self.nameSpace + '.item_frame_block","' + self.nameSpace + '.' + self.blocks[self.blck]["name"] + '"]}}}]}]}')
                else:
                    file.write('{"pools": [{"rolls": 1,"entries": [{"type": "minecraft:item","name": "' + self.blocks[self.blck]["blockDrop"] + '"}]}]}')
                
                file.close()
        

    
if __name__ == '__main__':
    app()