# studetf

Integracija [studentskih servisa](https://student.etf.bg.ac.rs) Elektrotehnickog fakulteta sa Google Calendar-om.

Aplikacija se konektuje na servise, dovlaci listu prijavljenih ispita, i zatim ih smesta u kalendar. Prepoznaju se ime ispita, datum, vreme i mesto odrzavanja. Osvezavanje vec dodati ispita (promena vremena, sale) je automatsko.

## Potrebno

- Python3
- `$ pip3 install -r requirements.txt`
- [GeckoDriver](https://github.com/mozilla/geckodriver/releases)
- Firefox

## Podesavanja

- Napravis aplikaciju u Google Developer Console
- Napravis klijenta sa rolom Project / Editor
- Dodas mejl tog naloga na zeljeni kalendar (share)
- Kredencijale (json fajl) smestis client_secret.json
- Popunis config.json (ili koristis env varijable)
- Calendar ID se nalazi u podesavanju kalendara

## Koriscenje

### Osvezavanje kalendara

`$ ./studetf.py`

### Popunjavanje anketa

`$ ./anketa.py`

## Roadmap

- [x] Integracija kalendara sa prijavljenim ispitima
- [x] Automatsko popunjavanje anketa
- [ ] Ubacivanje termina prijave ispita u kalendar
- [ ] Podsetnik za placanje rate

## Licenca

Copyright (c) 2019 Danilo Vidovic (vydd)

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is furnished
to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
