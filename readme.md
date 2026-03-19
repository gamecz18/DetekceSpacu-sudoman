# 👨‍💻 Sudo-man's Sleep Detector (LGTM 🚀)

**Author:** sudo-man (Promtfesor of Prompt Engineering)  
**Current Status:** "Waiting for Docker to build"

---

## 🚀 Architektura & Toolchain

Našel jsem na StackOverflow, že na detekci obličeje se používá něco, co se jmenuje OpenCV.  
Napsal jsem `pip install opencv-python`, chvíli jsem se modlil, a prošlo to.

Prej to používá nějaké Haarovy kaskády. Nevím, kdo je Haar, ale stáhnul jsem jeho XML soubory (`haarcascade_frontalface_default.xml`) a tváří se to, že to funguje.

---

## 🛠 Error-Driven Development (EDD) v praxi

### Problém 1: Barevné pixely jsou moc složité

Kaskády nechtěly fungovat na barvách. Tak jsem prostě udělal:

```python
cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
```

Grayscale. Hotovo. Stejně to vidím černobíle, když kódím ve 3 ráno.

---

### Problém 2: Pusa není oko (WTF?)

Kaskáda na oči mi pořád označovala koutky úst jako oči.  
Mohl jsem si přečíst dokumentaci a zjistit, jak správně nastavit parametry.

Místo toho jsem prostě vzal ten obličej a usekl ho v půlce:

```python
int(h / 2)
```

Hledám jen nahoře.  
Modern problems require modern `y:y + roiHalfH`.

Šach mat, false positives.

---

### Problém 3: Nemám čas čekat 5 sekund

Zadání říká 5 sekund. Testovat 5 sekund zírání do webkamery je ale strašná nuda, tak jsem to natvrdo nastavil na `0.4s`.

Pak jsem to těsně před pushem na main přepsal na `> 5.0`.

**PLS Compile 🙏**

---

## 📊 Bonus: Počítadlo bdělých

Přidal jsem počítadlo lidí, co nespí (`pocetBdelich`).

Prostě:
- `+= 1`, když je vidím  
- `-= 1`, když to dropne do `saveBusted`

Nechápu, jak to, že to funguje na první pokus. Asi jsem ve špatném repozitáři.

**Ale works on my machine! 🚀**

---

# 📚 Dokumentace k projektu: Detekce spánku

## Použité technologie a struktura

Pro práci s počítačovým viděním a Haarovými kaskádami jsem využil knihovnu **OpenCV**.

Ta obsahuje funkci:

```python
cv2.CascadeClassifier
```

která umožňuje snadné načtení předtrénovaných modelů z XML souborů  
(využil jsem výchozí kaskády pro obličej a pro oči).

Kód jsem rozdělil do:
- hlavní funkce `main`
- pomocné funkce `processFaceEye`

Pro bezpečné uchování stavu hlídání očí (čas poslední detekce a informace, zda už byl uložen důkazní snímek) jsem si vytvořil vlastní datovou třídu:

```python
@dataclass
class State:
    ...
```

---

## 🖼 Postup zpracování obrazu

V hlavní smyčce `while` procházím video po jednotlivých snímcích.

Každý snímek:
1. převedu do stupňů šedi pomocí:
   ```python
   cv2.COLOR_BGR2GRAY
   ```
2. zavolám pomocnou funkci pro detekci

Haarovy kaskády pracují s rozdíly jasu, nikoliv s barvami.

---

## ⚙️ Optimalizace a řešení falešných detekcí

Během vývoje jsem zjistil, že kaskáda na oči občas generuje falešně pozitivní výsledky (false positives), například detekuje:
- ústa  
- stíny kolem nosu  

Řešení:
- po nalezení obličeje oříznu oblast (ROI)
- prohledávám pouze horní polovinu obličeje

Tím se spolehlivost detekce očí výrazně zvýšila.

---

## 😴 Logika usínání a bonusové rozšíření

Jakmile program detekuje oči v horní polovině obličeje:
- resetuje se časovač

Pokud oči detekovány nejsou:
- začne se počítat čas

Během vývoje:
- testovací limit: `0.4 s`
- finální limit: `5 s`

Po překročení limitu:
- program vyhodnotí stav jako usnutí
- uloží důkazní snímek

---

### Bonus

Program obsahuje počítadlo bdělých osob:
- dynamicky sleduje počet lidí s otevřenýma očima
- při detekci spánku jednoho z nich hodnotu sníží
# Dokumentace k projektu: Detekce spánku

## Použité technologie a struktura

Pro práci s počítačovým viděním a Haarovými kaskádami jsem využil knihovnu **OpenCV**. Ta obsahuje funkci `cv2.CascadeClassifier`, která umožňuje snadné načtení předtrénovaných modelů z XML souborů (využil jsem výchozí kaskády pro obličej a pro oči).

Kód jsem rozdělil do:
- hlavní funkce `main`
- pomocné funkce `processFaceEye`

Pro bezpečné uchování stavu hlídání očí (čas poslední detekce a informace, zda už byl uložen důkazní snímek) jsem si vytvořil vlastní datovou třídu `@dataclass State`.

## Postup zpracování obrazu

V hlavní smyčce `while` procházím video po jednotlivých snímcích. Každý snímek nejprve převedu do stupňů šedi pomocí `cv2.COLOR_BGR2GRAY`, protože Haarovy kaskády pracují s rozdíly jasu, nikoliv s barvami. Poté zavolám svou pomocnou funkci.

## Optimalizace a řešení falešných detekcí

Během vývoje jsem zjistil, že kaskáda na oči občas generuje falešně pozitivní výsledky (tzv. *false positives*) – například detekovala ústa nebo stíny kolem nosu. Tento problém jsem vyřešil tak, že po nalezení obličeje oříznu prohledávanou oblast (ROI) pouze na **horní polovinu obličeje**. Tím se spolehlivost detekce očí razantně zvýšila.

## Logika usínání a bonusové rozšíření

Jakmile program v horní polovině obličeje detekuje oči, resetuje se časovač. Pokud oči nejsou detekovány, začne se počítat čas.

Z důvodu chybějícího dlouhého videa pro testování jsem si logiku původně zkoušel na limitu **0,4 s**, ale finální kód je podle zadání nastaven na **5 sekund**. Jakmile tento limit uplyne, program vyhodnotí stav jako usnutí a uloží důkazní snímek.

Jako bonus jsem do programu přidal **počítadlo bdělých osob**. Program dynamicky počítá lidi v záběru s otevřenýma očima a při detekci spánku jednoho z nich hodnotu aktuálně bdělých sníží.