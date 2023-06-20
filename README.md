# Hyper Light Drifter Save Editor v2

This app supports importing/exporting data from Hyper Light Drifter savefiles, editing that data, and saving loading that data from an additional file format (.hlds). This format stores the decoded data in plaintext and does not contain the machine-specific header that savefiles do, so it's ideal for sharing savedata publically.

## Installation

For release builds, simply run the hld-editor executable. For other versions, use `python App/App.py`. Python version 3 is required.

## Usage

Menu Options:
- Load: Load savedata from either a savfile or hlds file.
- Save: Write savedata to a hlds file. If current data was loaded from a hlds file then saving defaults to that file.
- Save As: Write savedata to a hlds file, no default target.
- Export: Write savedata to one of the four default savefile slots.
- Set Header: Detect your machine-specific header by choosing a locally created savefile. This needs to be set before you can export savefiles.

## Other Notes

- Equipping an outfit through the editor also sets it as collected (this avoids an crash when swapping outfits ingame)