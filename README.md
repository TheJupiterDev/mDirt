# Blockker

A tool for easily creating custom blocks using Minecraft Datapacks.
**Only Supported for 1.21.3 and up! No previous versions will be added!**

## How to use
Download the latest release, and run it.
Fill in all the details, press "Generate Pack" when you are ready.
Note that this will not work properly if you do not have a resource pack properly set up for it.

## How to setup a resource pack
1. Go to `assets/minecraft/models/item` and create a file called `item_frame.json`.
2. Paste the following, but modify where it says to:
```
{
    "parent": "minecraft:item/generated",
    "textures": {
        "layer0": "minecraft:item/item_frame"
    },
    "overrides":
    [
        { "predicate": { "custom_model_data": YOUR_CUSTOM_MODEL_DATA}, "model": "YOUR_RESOURCEPACK_NAMESPACE/YOUR_MODEL_NAME"}
    ]
}
```
3. Go to `assets/minecraft/models` and create a folder. It should be named the same as `YOUR RESOURCEPACK NAMESPACE` from above.
4. Go to said folder, and create a file called `YOUR_MODEL_NAME.json`.
5. Paste the following, but modify where it says to:
```
{
	"textures": {
		"0": "item/YOUR_TEXTURE_NAME",
		"particle": "item/YOUR_TEXTURE_NAME"
	},
	"elements": [
		{
			"from": [0, 0, 0],
			"to": [16, 16, 16],
			"faces": {
				"north": {"uv": [0, 0, 16, 16], "texture": "#0"},
				"east": {"uv": [0, 0, 16, 16], "texture": "#0"},
				"south": {"uv": [0, 0, 16, 16], "texture": "#0"},
				"west": {"uv": [0, 0, 16, 16], "texture": "#0"},
				"up": {"uv": [0, 0, 16, 16], "texture": "#0"},
				"down": {"uv": [0, 0, 16, 16], "texture": "#0"}
			}
		}
	],
	"display": {
		"thirdperson_righthand": {
			"rotation": [0, 0, -55],
			"translation": [0, 2.75, -2.5],
			"scale": [0.4, 0.4, 0.4]
		},
		"thirdperson_lefthand": {
			"rotation": [0, 0, -55],
			"translation": [0, 2.75, -2.5],
			"scale": [0.4, 0.4, 0.4]
		},
		"firstperson_righthand": {
			"rotation": [0, 45, 0],
			"scale": [0.4, 0.4, 0.4]
		},
		"ground": {
			"translation": [0, 3.25, 0],
			"scale": [0.4, 0.4, 0.4]
		},
		"gui": {
			"rotation": [28, 45, 0],
			"scale": [0.6, 0.6, 0.6]
		}
	}
}
```
6. Go to `assets/minecraft/textures/item` place your texture there. Note that the texture must be a PNG file.

### How to add more blocks to the resource pack
Duplicate the model file, and link it to another texture file.
In the `item_frame.json` file, add a `,` to the end of the first predicate, and add another:
`{ "predicate": { "custom_model_data": ANOTHER_CUSTOM_MODEL_DATA}, "model": "YOUR_RESOURCEPACK_NAMESPACE/ANOTHER_MODEL_NAME"}`

### Known Issues
None now! I fixed them all :)

The tool was made entirely by me, but the method for adding custom blocks was developed by https://youtube.com/@WASDBuildTeam and improved upon by me!
