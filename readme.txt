Anonimiz�l� algoritmus 
J�nis P�ter DHBYLZ

A program fel�p�tes�, haszn�lt f�jlok:
A program python 3-ban �r�dott, a f� modul az anonimyze.py python f�jjlel ind�that�. 
Ha bemeneti param�ter n�lk�l h�vjuk meg, akkor az alap�rtelmezett be�ll�t�sokat �s f�jlokat haszn�lja a program, ezek a k�vetkez�k:
	'-d','--DATADIR', az a k�nyvt�r, ahova az adatokat tartalmaz� fajlok ker�lnek
	'-c','--CONFIGDIR', a be�ll�t�sokat tartalmaz� k�nyvt�r
	'-o','--OUTDIR', az anonimiz�lt adatok ide ker�lnek kiment�sre
	'-s','--STRUCTFILE', a bemeneti adat strukt�r�j�t �rja le, �s a haszn�land� generaliz�l� algoritmusokat
	'-x','--XMLFILE' : az anonimiz�l�shoz haszn�lhatunk egy f�t ami a generaliz�l�shoz sz�ks�ges strukt�r�t tartalmazza
	'-w','--WOKRDIR' : ebbe a k�nyvt�rba m�sol�dni ki a datadir-b�l a m�r feldolgozott f�jlok
	

A configdir k�nyvt�r tartalma:
	-	recordstruct.json : le�rja a bemenetei adatszerkezetet(id mez�ket, nem generaliz�land� mez�ket, �s a generaliz�lt mez�kh�z haszn�lt algoritmusokat)
	-	mod.py : ebbe a f�jlba lettek kiszervezve a generaliz�l� algoritmusokat
	-	treedata.xml : azt a fa strukt�r�t tartalmazza ami alapj�n a sz�veges mez�k �ltal�nos�that�ak, jelen esetben csak 1-et tud kezelni a program
	-	anonimData.txt : a program fut�sa sor�n keletkezik, azokat a csoportokat tartalmazza, amelyeket m�r anonimiz�ltunk, 
	�s vagy teljes�tik a k anonym felt�telt, vagy nem 
	-	algorithm.txt : az els� futtat�s ut�n keletkez� anonimiz�l� algoritmust tartalmazza, a k�s�bbi futtat�sokban ezzel az algoritmussal dolgozik a program
	
Az outdir k�nyvt�r tartalma:
	-	outfile*.txt : az anonimiz�l�s v�geredm�nye
	-	notanonymcoll.txt : seg�df�jl, ami tartamazza azokat a sorokat, amelyeket nem tudtuk m�g az eredm�nyf�jlba betenni, mert nem felelnek meg k anonymak