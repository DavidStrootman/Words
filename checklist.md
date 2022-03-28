=== README CHECKLIST ===


Gekozen taal:

Eigen taal (Words)

Turing-compleet omdat:

 

Code is geschreven in functionele stijl. ✓

 

Taal ondersteunt:

Loops? Voorbeeld:  
While loop:  
examples/words/loop.word
Recursie:  
examples/words/rec.word  
examples/words/fibonacci.word

Goto-statements? Voorbeeld: [file] - [regel]

Lambda-calculus? Voorbeeld:
Lambdas zijn niet expliciet toegevoegd, maar functions kunnen een voor een over elkaar uitgevoerd worden, wat 
nesten van functies mogelijk maakt

examples/words/rec.word - regel 11

Bevat:

Classes met inheritance:  
src/words/token_types/lexer_token.py
src/words/token_types/parser_token.py

Object-printing voor elke class: ja, elke class inherit van src/words/helper/PrintableABC, wat str en repr methods toevoegd.

Decorator: src/words/helper/trace.py - Wordt als voorbeeld gebruikt om alle calls naar _parse_exhaustive te loggen in src/words/parser/parse.py op regel 27

Type-annotatie: Haskell-stijl in comments: [nee]; Python-stijl in functiedefinities: [ja]

Minstens drie toepassingen van hogere-orde functies:

1. src/words/token_types/lexer_token.py - regel 231

2. src/words/token_types/lexer_token.py - regel 236

3. src/words/helper/TokenTypeEnum.py  - regel 9

 

Interpreter-functionaliteit Must-have:

Functies: [meer per file]

Functie-parameters kunnen aan de interpreter meegegeven worden door:

een initiele stack mee te geven

Functies kunnen andere functies aanroepen: zie voorbeeld

examples/words/fibonacci.word - regel 14, 15 (roept zichzelf recursief aan)
examples/words/rec.word - regel 6, 15


Functie resultaat wordt op de volgende manier weergegeven:
Via de `__PRINT__` macro wordt naar de stdout geschreven

 

Interpreter-functionaliteit (should/could-have):

[Error messaging] geïmplementeerd in de bestanden src/words/exceptions/lexer_exceptions.py en src/words/exceptions/parser_exceptions.py

Deze exceptions worden tijdens het lexen en parsen gebruikt om de gebruiker te duiden op fouten zijn de source code.
Door middel van de Debuggable base class in src/words/helper/Debuggable.py. Tokens inheriten van Debuggable, waardoor ze
meer informatie kunnen printen als dat nodig is. Als je bijvoorbeeld een source file inleest met `ELSE ELSE`, wat 
incorrecte syntax is, krijg je de volgende trace:
```txt
  File "/home/david/repos/Words/src/words/parser/parse_util.py", line 42, in eat_until_discarding
    parsed_token = token.parse(tokens)
  File "/home/david/repos/Words/src/words/token_types/lexer_token.py", line 182, in parse
    raise InvalidTokenError(self)
words.exceptions.lexer_exceptions.InvalidTokenError: Got an invalid token "Types.ELSE" at line 10.
```
Aan de laatste regel in de trace kun je dus zien waar je syntaxfout zit.

[zelf-recursie] Functies kunnen op zichzelf recursen zoals te zien in het fibonacci voorbeeld.
[Gekozen functionaliteit] geïmplementeerd door middel van de volgende functies: a) [functie] in [file] op regel [regel]
[Gekozen functionaliteit] geïmplementeerd door middel van de volgende functies: a) [functie] in [file] op regel [regel]
[Gekozen functionaliteit] geïmplementeerd door middel van de volgende functies: a) [functie] in [file] op regel [regel]

[Extra functionaliteit overlegd met docent, goedkeuring: datum e-mail; overeengekomen max. aantal punten: X]