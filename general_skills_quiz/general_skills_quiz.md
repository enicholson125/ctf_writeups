# General Skills Quiz

This was in the misc section and the initial instruction was `nc pwn-2021.duc.tf 31905`.

Connecting to the port told you that you were doing the quiz, that you had 30 seconds and started asking you questions.

The first question was 1+1 which was pretty doable. The second was to convert a value in hex to decimal which I, personally, am terrible at doing in my head, so at that point I gave up on trying to manually complete the quiz and started looking at alternative options.

Just in case, I had a quick go at code injection but got nothing and given the challenge was in the misc section, it seemed pretty unlikely. I decided to script answers to the quiz and see if that got me the flag.

I wrote [netcat.py](./netcat.py) to connect to the socket and answer the questions for me. The questions were simple, particularly in python, as they were all converting between various different formats.

Completing the quiz got me the flag!

This was a fun starting challenge and I enjoyed completing it. I just wish I'd converted to Python 3 when I realised I'd started out in Python 2, as the script I've ended up with is a useful toolbox of all those little conversion functions that I always have to look up and which differ quite a lot between Python 2 and 3. It would have been much more useful to have the toolbox in Python 3!
