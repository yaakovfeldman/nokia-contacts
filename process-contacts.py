""" Cleanup Nokia contacts

Nokia feature phones such as Nokia 105 can backup contacts through Contacts>Settinss>Backup
(This may only back up phone contacts, not sim)
A file named similarly to backup.dat will be saved to the memory card

It is a VCF contacts backup with repeating blocks like

BEGIN:VCARD
VERSION:2.1
N;ENCODING=QUOTED-PRINTABLE;CHARSET=UTF-8:;=
<name>;;;
TEL;VOICE;CELL:<number>
END:VCARD

separated by blank lines, where <name> and <number> are the information to extract.
Everything else is boilerplate, as these phones do not support multiple numbers per contact or other contact types.
If a contact has more than one number the second is saved as a separate contact with '1' appended to the name.
The contacts are in alphabetical order.
Important: confirm all this is true of YOUR input file

This script will remove duplicate contacts, defined as those with the same number as the
contact immediately preceding. These contact lists often include duplicates whose name has a '1' suffix
despite the number being the same. It will not check for duplicate numbers with different names.

It will also optionally remove contacts with no number.
"""

# Params
input_path = r'input.dat'
output_path = r'output.dat'
# set to True to rmeove contacts without numbers - defaults to False as such contacts may be used eg as memos
remove_contacts_without_number = False

names = []
numbers = []
output = []
last_line_was_name = False

with open(input_path, mode='r') as vcf_:
    for line in vcf_:
        boilerplate = ['BEGIN', 'VERSION', 'CHARSET']
        if [ele for ele in boilerplate if(ele in line)]:
            continue
        
        if line[-4:-1] == ';;;':
            # this must be a contact
            # check if we have encountered a phone number since the previous contact
            # if not then delete the previous contact
            if last_line_was_name:
                if remove_contacts_without_number:
                    names.pop()
                else:
                    numbers.append('')
            last_line_was_name = True
            names.append(line[:-3])
        
        if line[:3] == 'TEL':
            # this must be a phone number
            last_line_was_name = False
            numbers.append(line.split(':')[1].strip())

for idx, x in enumerate(names):
    #check if same number as previous
    if idx and numbers[idx] == numbers[idx-1]:
        continue
    output.append('BEGIN:VCARD')
    output.append('VERSION:2.1')
    output.append('N;ENCODING=QUOTED-PRINTABLE;CHARSET=UTF-8:;=')
    output.append(names[idx] + ';;;')
    if numbers[idx]:
        output.append('TEL;VOICE;CELL:' + numbers[idx])
    output.append('END:VCARD')
    output.append('')

with open(output_path, 'w') as f:
    for line in output:
        f.write(f"{line}\n")
