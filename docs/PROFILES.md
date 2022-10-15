# Profiles
You might be feeling creative when you think of Disrichie Profiles, it's like a file holding full of information to be read and put into the Rich Presence details.

Using them is an easy task compared to the command-line options:
```shell
# Imagine doing this
$ disrichie -i CLIENT_ID -d "Let's play some games!" \
	-s "Chilling out"

# When you can just do it in the easy way
$ disrichie myrpc.json
```

Big Con for the command-line options is the [Buttons!](#button) as they can only be set on profiles.

## What are they?
Disrichie profiles are stored in plain JSON files, containing various information about the details of Rich Presence.

For example:
```json
{
	"clientId": "CLIENT ID",
	"details": "Let's play some games!",
	"state": "Chilling out"
}
```

Here's an explanation about the example:
- `clientId` is the client ID of your Rich Presence, this will display the name, large image, and small image.
- `details` is where you put the details of your Rich Presence status.
- `state` is equivalent to `details`, but is placed below it and is a small text.

## Key references
| Key 	| Description 	| Type 	|
|---	|---	|---	|
| `clientId` 	| The ID that holds the name and icon of your Rich Presence. 	| `int` 	|
| `details` 	| Details of your Rich Presence, placed below it's name. 	| `str` 	|
| `state` 	| State of your Rich Presence, placed below the `details` key. 	| `str` 	|
| `elapsed` 	| Toggles the elapsed time of your Rich Presence | `bool` 	|
| `largeImageKey` 	| Used to retrieve the image from your Rich Presence, upload it on the Developer Portal first. 	| `str` 	|
| `largeImageText` 	| Used to display when large image is hovered, leaving this unset or blank may not display. 	| `str` 	|
| `smallImageKey` 	| Just like `largeImageKey`, but is placed in the bottom-right corner of it. 	| `str` 	|
| `buttons` 	| A list of buttons used to display on your Rich Presence, refer to [Button references](#button-references) if you want to see the structure. | `list[dict]` 	|

### Button
| Key 	| Description 	| Type 	|
|---	|---	|---	|
| `label` 	| The text that will be displayed on the button. 	| `str` 	|
| `url` 	| This will be used when the button is pressed. 	| `str` 	|