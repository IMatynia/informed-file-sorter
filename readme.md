# Informed file sorter
Consider the following hypothetical scenario: You have a folder of pictures in various formats and you need to sort them all into some number
of arbitrary folders. How would you do that? Open each file one by one, see what it is, close the program you used to preview
the file, manually navigate to the folder, move the file over and, at last, you are done. Time for the next one. That's a bit time consuming,
dont you think? Well, at least I do. That's why i created this app!

![sort the cat](https://imgur.com/uyyogvp.png)

## Dependencies
- python-3.10
- [pyside6](https://pypi.org/project/PySide6/)

## How to use
1. Drag and drop (to the upper portion of the window) or use tool bar buttons to select a source folder, from which the
files will be moved.
2. Drag and drop (to the bottom portion of the window) destination folder(s) or use the toolbar button.
3. Select a destination by clicking on the correct folder, or (if there is less than 10) press numbers 1,2,3,4...,0 on the keyboard.
There can 0..1 destinations per image.
4. Use left and right arrows or buttons on the tool bar to move between files in the source directory.
5. When you are satisfied with your selection, apply the assignments using the green button on the toolbar or press ctrl+s. 

## Features
- Supports previews of many image formats and in the case of PDF files, shows the first page.
- The program supports Addons. By default, the program comes with an addon for converting webp images to png files which can be a template for creating new ones.
- Double-clicking on the preview opens the file using `xdg-open`
- By pressing +/- you can zoom in and out the preview
- Files can be filtered by reg-ex. Press ctrl+f or the button on the keyboard to modify it.