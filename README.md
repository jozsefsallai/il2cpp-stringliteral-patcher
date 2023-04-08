# IL2CPP StringLiteral Patcher

This repository contains two Python scripts that you can use to extract string
literals from global-metadata.dat files and patch them into a new file.

## The Problem

Recently, many Unity games have been using IL2CPP to compile their C# code into
native binaries. Games that don't have support for localization and don't store
texts in MonoBehaviour objects that can be easily obtained, will usually have
a dictionary of hardcoded strings in the game's code. When using IL2CPP, these
hardcoded string literals will be stored in a byte chunk and a lookup table will
be used to determine the index and length of each string required by the game.

This is good for developers, as it offers faster and safer access to all string
literals, but for modders and translators, it can be a bit troublesome. While we
can see the string literals themselves in the global-metadata.dat file, editing
them is a bit more complicated. Using a hex editor to change the strings will
work as long as the new strings are the same length as the old ones, but this is
far from ideal.

## The Solution

Using the scripts from this repository, you can extract all string literals from
a global-metadata.dat file and store them in a JSON file that you can then edit.
Once you're done making changes to your strings, you can then create a new
global-metadata.dat file with the patches applied.

## Usage

### Extracting Strings

```
python3 extract.py -i /path/to/global-metadata.dat -o /path/to/output/strings.json
```

This will create a JSON file containing every string literal that can be found
in the binary. As expected, this file will be rather large, as it contains lots
of irrelevant strings, such as ones used by Unity, .NET, and other libraries.

Unfortunately, there is no way to reliably tell which strings are the ones that
the game actually displays to the player, however, they are usually located in
the same chunk of the file (usually towards the end). You can use your editor's
search function to find a string that you know is visible in the game, and then
look around that string to determine the chunk that contains the game's strings.

While you can keep the other strings in the JSON file, it is recommended that
you just remove any string that you don't actually need. The patcher script will
just copy the original string literal if it can't find a replacement in your
JSON file.

### Patching Strings

```
python3 patch.py -i /path/to/original-global-metadata.dat -p /path/to/strings.json -o /path/to/patched-global-metadata.dat
```

This will create a new global-metadata.dat file with the updated strings. If all
went well, the game will run without any errors and will also display the new
strings. The output path can not be the same as the input path.

## Troubleshooting and FAQ

**Q: Where can I find the global-metadata.dat file?**

A: The usual location in the game's directory is: `Managed/Metadata/global-metadata.dat`.
If you're trying to mod a Unity WebGL/WebAssembly game, you can find the
metadata file by extracting it from the game's data file using a tool such as
[unityweb][unityweb-url].

**Q: I'm getting "Invalid global-metadata file" errors when trying to extract strings.**

A: This error should only be thrown when your global-metadata.dat file doesn't
start with the correct magic header. This can either mean that the file is
encrypted, obfuscated, or actually not a global-metadata.dat file in the
first place.

**Q: I'm getting "Invalid StringLiteral object" errors when trying to patch strings.**

A: One of your strings in the JSON file does not follow the correct format. The
exported JSON file should be an array of objects, each object having two
keys: `index` (should never be changed, as it's used for identifying the
string) and `value` (the actual string literal). If any of these is missing,
the script will throw an error.

**Q: I'm getting a different error when extracting or the resulting strings are
all garbled.**

A: The global-metadata file is most likely obfuscated. Some game developers may
do this to prevent players from reverse engineering their games. If you're
sure the file is not obfuscated, please [open an issue][issue-tracker-url]
and I will look into it.

**Q: What version of global-metadata was this tool tested with?**

A: The scripts were only tested with version 29. In theory, version should not
affect the functionality of the scripts, as the offsets at which the string
literal information is stored should be the same. If you encounter any issues
with a particular version, please [open an issue][issue-tracker-url].

## License

MIT.

[issue-tracker-url]: https://github.com/jozsefsallai/il2cpp-stringliteral-patcher/issues
[unityweb-url]: https://github.com/jozsefsallai/unityweb
