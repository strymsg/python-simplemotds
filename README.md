# Simple motds

Simple module to get the message of the day (motd), every motd should be in a separate file inside (by default) `messages/` folder.

The module returns a different motd every day, month, week, hour or minute, the time period which the message should be changed is defined in the simple configuration file `config.json`.

## Initialization

A `SimpleMotd` object should be created and use its attributes.

```python
from simple_motd import SimpleMotd
simplemotd = SimpleMotd()
# optional oarguments: config_json_file
```

* `config_json_file`: See [configuration file details](#modifying-configuration-file).

### SimpleMotd methods

* `getMotdContent()`: returns the contents of the current message by reading it's file inside the `messages` folder. Contents are returned as a python string using utf-8 enconding by default.
* `getMotdFile()`: returns a python file object (opened) to the current message.
* `getMotdFileName()`: returns the file name of the current message.
* `ForceNextMessage()`: Forces to change the message by selecting another file inside `messages` or other configured folder, returns the new filename.

## Modifying configuration file

All is done in the file `config.json`, defaults:

```javascript
{
   "time-period": "day",
   "folder": "./messages",
   "selection-type": "random"
}
```
* **time-period**: Specifies the time period to change the message returned. Valid values:
 * month
 * week
 * hour
 * day
 * minute
 
* **folder**: The folder where to look for the messages, every message must be in a separate file of any extansion.
 
* **selection-type**: How to get the messages, it can be:
 * random
 * alphabetically-desc
 * alphabetically-asc
 * modification-asc
 * modification-desc
 * formula <numeric formula> (not implemented yet)

`alphabetically-desc` gets files by its name in a descendent order (a first and z last), `alphabetically-asc` (z first, a last). `modification-asc/desc` considers the last time of modification of the files as ordering rule.


