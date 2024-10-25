import os
import sys
import shutil
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from tkinter import filedialog
from ui import Ui_MainWindow

class app():
    def __init__(self):
        super(app, self).__init__()
        
        self.blocks = {}

        self.app = QtWidgets.QApplication(sys.argv)
        self.mainwindow = QtWidgets.QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.mainwindow)
        self.mainwindow.show()

        self.checkAdd()
        self.checkRemove()
        self.checkGenerate()
        self.checkResourceEnabled()

        self.app.exec()
    
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
            self.ui.blockTexturePath.setEnabled(True)
            self.ui.blockModel.setEnabled(True)
        else:
            self.ui.blockTextureLabel.setEnabled(False)
            self.ui.blockModelLabel.setEnabled(False)
            self.ui.blockTexturePath.setEnabled(False)
            self.ui.blockModel.setEnabled(False)
    
    def toggleResource(self):
        if self.ui.blockResourceCheckBox.isChecked():
            self.ui.blockTextureLabel.setEnabled(True)
            self.ui.blockModelLabel.setEnabled(True)
            self.ui.blockTexturePath.setEnabled(True)
            self.ui.blockModel.setEnabled(True)
        else:
            self.ui.blockTextureLabel.setEnabled(False)
            self.ui.blockModelLabel.setEnabled(False)
            self.ui.blockTexturePath.setEnabled(False)
            self.ui.blockModel.setEnabled(False)

    def addBlock(self):
        self.blockProperties = {
            "name": self.ui.blockName.text(),
            "displayName": self.ui.blockDisplayName.text(),
            "customModelData": self.ui.blockCMD.text(),
            "baseBlock": self.ui.blockBase.text(),
            "texturePath": self.ui.blockTexturePath.text(),
            "blockDrop": self.ui.blockDrop.text()
        }
        self.blocks[self.ui.blockName.text()] = self.blockProperties
        
        self.ui.blockList.addItem(self.blockProperties["name"])
    
    def removeBlock(self):
        self.curItem = self.ui.blockList.currentRow()
        self.blocks.pop(self.ui.blockList.item(self.curItem).text())
        self.ui.blockList.takeItem(self.curItem)
        print(self.blocks)
    
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
        os.mkdir(self.packDir + "\\assets\\minecraft\\models\\" + self.ui.packNamespace.text())
        with open(f'{self.packDir}\\pack.mcmeta', 'w') as pack:
            pack.write('{\n    "pack": {\n        "pack_format": 42,\n        "description": "' + self.ui.packDescription.text() + '"\n    }\n}\n')
            pack.close()
        with open(f'{self.packDir}\\assets\\minecraft\\models\\item\\item_frame.json', 'a') as file:
            file.write('{"parent": "minecraft:item/generated","textures": {"layer0": "minecraft:item/item_frame"},"overrides":[')
            for block in self.blocks:
                file.write('{ "predicate": { "custom_model_data": ' + self.blocks[block]["customModelData"] + '}, "model": "' + self.ui.packNamespace.text() + '/' + self.blocks[block]["name"] + '"}')
                if block != next(reversed(self.blocks.keys())):
                    file.write(',')
            file.write(']}')
            file.close()
        for block in self.blocks:
            self.texture = self.packDir + "\\assets\\minecraft\\textures\\item\\" + self.blocks[block]["name"] + ".png"
            shutil.copy(self.blocks[block]["texturePath"], self.texture)
            with open(f'{self.packDir}\\assets\\minecraft\\models\\'+ self.ui.packNamespace.text() + '\\' + self.blocks[block]["name"] + '.json', 'w') as file:
                file.write('{"credit": "Made with mDirt","textures": {"0": "item/' + self.blocks[block]["name"] + '","particle": "item/' + self.blocks[block]["name"] + '"},"elements": [{"from": [0, 0, 0],"to": [16, 16, 16],"faces": {"north": {"uv": [0, 0, 16, 16], "texture": "#0"},"east": {"uv": [0, 0, 16, 16], "texture": "#0"},"south": {"uv": [0, 0, 16, 16], "texture": "#0"},"west": {"uv": [0, 0, 16, 16], "texture": "#0"},"up": {"uv": [0, 0, 16, 16], "texture": "#0"},"down": {"uv": [0, 0, 16, 16], "texture": "#0"}}}],"display": {"thirdperson_righthand": {"rotation": [0, 0, -55],"translation": [0, 2.75, -2.5],"scale": [0.4, 0.4, 0.4]},"thirdperson_lefthand": {"rotation": [0, 0, -55],"translation": [0, 2.75, -2.5],"scale": [0.4, 0.4, 0.4]},"firstperson_righthand": {"rotation": [0, 45, 0],"scale": [0.4, 0.4, 0.4]},"ground": {"translation": [0, 3.25, 0],"scale": [0.4, 0.4, 0.4]},"gui": {"rotation": [28, 45, 0],"scale": [0.6, 0.6, 0.6]}}}')
                file.close()
        
    
    def generate(self):

        if self.ui.blockResourceCheckBox.isChecked():
            self.generateResourcePack()

        self.outputDir = filedialog.askdirectory().replace("/", "\\")
        self.packDir = os.path.join(self.outputDir, self.ui.packName.text())
        os.mkdir(self.packDir)
        os.mkdir(self.packDir + "\\data")
        self.packNamespace = os.path.join(self.packDir, "data", self.ui.packNamespace.text())
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
            tick.write('# Generated by mDirt!\nexecute as @e[type=item_display,tag=' + self.ui.packNamespace.text() + ".custom_block] at @s run function " + self.ui.packNamespace.text() + ":as_blocks")
            tick.close()
        with open(f'{self.packNamespace}\\function\\load.mcfunction', 'w') as load:
            load.write('# Generated by mDirt!\ntellraw @a {"text":"[mDirt] - Successfully loaded pack!","color":"red"}')
            load.close()
        with open(f'{self.minecraft}\\tags\\function\\tick.json', 'w') as tickJS:
            tickJS.write('{\n    "values":[\n        ' + f'"{self.ui.packNamespace.text()}' + ':tick"\n        ]\n    }')
            tickJS.close()
        with open(f'{self.minecraft}\\tags\\function\\load.json', 'w') as loadJS:
            loadJS.write('{\n    "values":[\n        ' + f'"{self.ui.packNamespace.text()}' + ':load"\n        ]\n    }')
            loadJS.close()
        
        # Placed Item Frame Advancement

        with open(f'{self.packNamespace}\\advancement\\placed_item_frame.json', 'w') as file:
            file.write('{"criteria": {"requirement": {"trigger": "minecraft:item_used_on_block","conditions": {"location": [{"condition": "minecraft:match_tool","predicate": {"items": ["minecraft:item_frame"]}}]}}},"rewards": {"function": "' + self.ui.packNamespace.text() + ':placed_item_frame"}}')
            file.close()
        
        # Placed Item Frame Function

        with open(f'{self.packNamespace}\\function\\placed_item_frame.mcfunction', 'w') as file:
            file.write('advancement revoke @s only ' + self.ui.packNamespace.text() + ':placed_item_frame\nexecute as @e[tag=' + self.ui.packNamespace.text() + '.item_frame_block,distance=..10] at @s run function ' + self.ui.packNamespace.text() + ':check_placed_item_frame')
            file.close()

        # Check Placed Item Frame, block/place Functions

        with open(f'{self.packNamespace}\\function\\check_placed_item_frame.mcfunction', 'a') as file:
            for self.blck in self.blocks.keys():
                os.mkdir(self.packNamespace + "\\function" + f"\\{self.blck}")
                with open(f'{self.packNamespace}\\function\\{self.blck}\\place.mcfunction', 'w') as file2:
                    file2.write("setblock ~ ~ ~ " + self.blocks[self.blck]["baseBlock"] + ' keep\nsummon item_display ~ ~ ~ {brightness:{sky:15,block:0},Tags:["' + self.ui.packNamespace.text() + f'.{self.blocks[self.blck]["name"]}","' + self.ui.packNamespace.text() + '.custom_block"],transformation:{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],translation:[0f,0.469f,0f],scale:[1.001f,1.001f,1.001f]},item:{id:"minecraft:item_frame",count:1,components:{"minecraft:custom_model_data":' + self.blocks[self.blck]["customModelData"] + '}}}\n')
                    file2.close()
                file.write('execute as @s[tag=' + self.ui.packNamespace.text() + '.' + self.blocks[self.blck]["name"] + '] run function ' + self.ui.packNamespace.text() + ':' + self.blocks[self.blck]["name"] + '/place\n')
            
            file.write('\nkill @s')
            file.close()
        
        # As Blocks block/block, block/break Functions

        with open(f'{self.packNamespace}\\function\\as_blocks.mcfunction', 'a') as file:
            for self.blck in self.blocks.keys():
                with open(f'{self.packNamespace}\\function\\{self.blck}\\{self.blck}.mcfunction', 'w') as file2:
                    file2.write('execute unless block ~ ~ ~ ' + self.blocks[self.blck]["baseBlock"] + ' run function ' + self.ui.packNamespace.text() + ':' + self.blocks[self.blck]["name"] + '/break')
                    file2.close()
                with open(f'{self.packNamespace}\\function\\{self.blck}\\break.mcfunction', 'a') as file3:
                    file3.write('execute as @e[type=item,sort=nearest,limit=1,distance=..2,nbt={OnGround:0b,Age:0s,Item:{id:"' + self.blocks[self.blck]["baseBlock"] + '"}}] run kill @s\n')
                    file3.write('loot spawn ~ ~ ~ loot ' + self.ui.packNamespace.text() + ':' + self.blocks[self.blck]["name"] + '\n')
                    file3.write('kill @s')
                    file3.close()
                
                file.write('execute as @s[tag=' + self.ui.packNamespace.text() + '.' + self.blocks[self.blck]["name"] + '] run function ' + self.ui.packNamespace.text() + ':' + self.blocks[self.blck]["name"] + '/' + self.blocks[self.blck]["name"] + '\n')
            file.close()
        
        # Give Items Function

        with open(f'{self.packNamespace}\\function\\give_items.mcfunction', 'a') as file:
            for self.blck in self.blocks.keys():
                file.write('give @s item_frame[custom_name=\'{"italic":false,"text":"' + self.blocks[self.blck]["displayName"] + '"}\',custom_model_data=' + self.blocks[self.blck]["customModelData"] + ',entity_data={id:"minecraft:item_frame",Fixed:1b,Invisible:1b,Silent:1b,Invulnerable:1b,Facing:1,Tags:["' + self.ui.packNamespace.text() + '.item_frame_block","' + self.ui.packNamespace.text() + '.' + self.blocks[self.blck]["name"] + '"]}] 1\n')
            file.close()
        
        # Loot Tables

        for self.blck in self.blocks.keys():
            with open(f'{self.packNamespace}\\loot_table\\{self.blocks[self.blck]["name"]}.json', 'w') as file:
                if self.blocks[self.blck]["blockDrop"] == "":
                    file.write('{"pools": [{"rolls": 1,"entries": [{"type": "minecraft:item","name": "minecraft:item_frame"}],"functions": [{"function": "minecraft:set_components","components": {"minecraft:custom_model_data": ' + self.blocks[self.blck]["customModelData"] + ',"minecraft:custom_name": "{\\"italic\\":false,\\"text\\":\\"' + self.blocks[self.blck]["displayName"] + '\\"}","minecraft:entity_data": {"id": "minecraft:item_frame","Fixed": true,"Invisible": true,"Silent": true,"Invulnerable": true,"Facing": 1,"Tags": ["' + self.ui.packNamespace.text() + '.item_frame_block","' + self.ui.packNamespace.text() + '.' + self.blocks[self.blck]["name"] + '"]}}}]}]}')
                else:
                    file.write('{"pools": [{"rolls": 1,"entries": [{"type": "minecraft:item","name": "' + self.blocks[self.blck]["blockDrop"] + '"}]}]}')
                
                file.close()
        

    
if __name__ == '__main__':
    app()