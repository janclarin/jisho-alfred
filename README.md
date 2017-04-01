# Jisho Alfred Workflow
An [Alfred](https://www.alfredapp.com/) workflow to easily search
[Jisho.org](http://jisho.org/), a powerful Japanese-English online dictionary.
It uses the Jisho.org API to retrieve search results and instantly display them
within Alfred's search results.

**[DOWNLOAD](https://github.com/janclarin/jisho-alfred-workflow/releases/download/1.6/jisho.alfredworkflow)**

<img src="https://raw.githubusercontent.com/janclarin/jisho-alfred-workflow/master/screenshots/usage.gif" width="480">

## Usage
### Searching
Type `ji ` or `じ` followed by the word you want to search for. Note that there
is a space after `ji` and not after `じ`.

As [stated by Jisho.org](http://jisho.org/docs), searches for English words can
be surrounded with *double quotes* to prevent searching for the word as romaji.
e.g. `ji "date"` would search for the English word "date" and `ji date` would
search for "だて".

### Open search result in browser
Press `Enter` on a selection to open the result on Jisho.org.

### Display large version of search result
Press `CMD`+`L` on a selection to display a large version of the kanji or kana
search result title. This is useful for looking at detailed kanji.

## Credits
Thank you to the people at [Jisho.org](http://jisho.org/about) for making a
great service and an
[API](http://jisho.org/forum/54fefc1f6e73340b1f160000-is-there-any-kind-of-search-api).

This workflow uses the
[Alfred-Workflow library](https://github.com/deanishe/alfred-workflow),
licensed under
[The MIT License](https://github.com/deanishe/alfred-workflow/blob/master/LICENCE.txt).

The
[icon](https://github.com/janclarin/jisho-alfred-workflow/blob/master/icon.png)
is a slightly modified version of
[Book icon](https://www.iconfinder.com/icons/285636/book_icon#size=128) by
[Paomedia](https://www.iconfinder.com/paomedia), licensed under
[CC BY 3.0](https://creativecommons.org/licenses/by/3.0).

Inspired by [alfred-jisho](https://github.com/kylesezhi/alfred-jisho), but
found that it was really slow between searches and no longer maintained.
