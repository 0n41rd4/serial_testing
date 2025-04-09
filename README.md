commands.txt contains the messages for the serial interaction of the tests.
Lines in commands.txt are either of the form s:foo or e:foo1,foo2,foo3,... 
Here foo1, foo2 and foo3 are strings not containing commas.
Lines of the form s:foo send the string foo via the command line.
Lines of the form e:foo1,foo2,foo3,... wait until any of foo1, foo2, foo3,
... is read from the serial output. Once one of them is read, the next line
in commands.txt is processed.

Usage: power on the board and immediately issue 'python3 test.py'
