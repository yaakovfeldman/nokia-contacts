# Cleanup Nokia contacts

Nokia feature phones such as Nokia 105 can backup contacts through Contacts>Settings>Backup. (This may only back up phone contacts, not sim, so copy sim contacts to phone first.)

A file named similarly to backup.dat will be saved to the memory card. It is a VCF contacts backup with repeating blocks like

```
BEGIN:VCARD
VERSION:2.1
N;ENCODING=QUOTED-PRINTABLE;CHARSET=UTF-8:;=
<name>;;;
TEL;VOICE;CELL:<number>
END:VCARD
```

separated by blank lines, where `<name>` and `<number>` are the information to extract.
Everything else is boilerplate, as these phones do not support multiple numbers per contact or other contact types. If a contact has more than one number the second is saved as a separate contact with '1' appended to the name. The contacts are in alphabetical order.

**Important: confirm all this is true of YOUR input file**

This script will remove duplicate contacts, defined as those with the same number as the
contact immediately preceding. These contact lists often include duplicates whose name has a '1' suffix despite the number being the same. It will not check for duplicate numbers with different names.

It will also optionally remove contacts with no number.

## Warning

This script makes several assumptions around the format of the VCF input. Keep a backup copy of the contacts until you have verified the output is correct!

## Typical workflow

1. Copy all contacts from sim to phone using Contacts menu on phone
2. Backup all sim contacts to memory card using Contacts menu on phone
3. Use computer to process the `backup.dat` file from memory card with script (saving a backup copy first!)
4. Delete all sim and all phone contacts from phone using Contacts menu on phone (if asked for password default is `12345`)
5. Restore backup using Contacts menu on phone
