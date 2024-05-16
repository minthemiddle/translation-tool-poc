## 2405162152

Turns out that Haiku runs into problems with language detection as soon as there are some words in other languages in it.
Example: "Compania QSW QUALITÄTS SERVICE WELZBACHER GMBH, este o societate Prestatar de servicii, creată în anul 2009, care își desfășoară activitatea în domeniul Testarea produselor si a materialelor. De asemenea, activează în aceeași măsură și în domeniile Quality test, Reworking, Sorting, quality control, Checking, Industrial service, Labelling, Assembly, și Quality service. Are sediul în Aschaffenburg, Germania."

Now, it will think it's German (despite being Romanian with a German company name).

## 2405161844

With Claude Haiku, you don't seem to need a source language.
And you could also mix languages in the input, it does not care.

## 2405160958

Test cases:

- Pass terms in quotation marks and check whether it's verbatim in the output (rule 3)
- Pass company information and check whether it's verbatim in the output (rule 4)
- Check whether it has `'` quotation marks (rule 5)

## 2405160952

Claude's Haiku does a lot better with the "don't translate x" rule.


## 2405152218

The rule for "Never translate company name" or even "Don't translate what is enclosed in quotation marks" gets always ignored by GPT3.5.
I'm considering treating it deterministically: extracting it via Python before passing the prompt, replace with placeholders and reconstruct after LLM.
But this would add complexity.

The problem with that solution would be that it would not work properly for existing translations.
