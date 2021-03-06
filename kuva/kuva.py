# -*- coding: UTF-8 -*-

import tila
from util import *
import os

def muunna(P):
	"""Muunna piirrettävä piste (2-tuple) pisteeksi kuvapinnalla."""
	x, y = P
	a1, b1 = tila.asetukset['xmuunnos']
	a2, b2 = tila.asetukset['ymuunnos']
	
	return (a1 * x + b1, a2 * y + b2)

def onkoSisapuolella(P):
	"""Onko piste 'P' rajojen sisäpuolella?"""
	
	X, Y = P
	
	ret = True
	ret &= X >= tila.asetukset['minX']
	ret &= X <= tila.asetukset['maxX']
	ret &= Y >= tila.asetukset['minY']
	ret &= Y <= tila.asetukset['maxY']
	
	return ret

def aloitaKuva():
	"""Aloita kuvan piirtäminen. Kutsuttava aina ennen muita operaatioita, 
	lopetettava kutsumalla lopeta(). LaTeX-ympäristö kutsuu yleensä aloitaKuva-
	ja lopetaKuva-funktioita automaattisesti."""
	
	try:
		os.unlink("kuva-tmp-output.txt")
	except OSError:
		pass
	tila.out = open("kuva-tmp-output.txt.tmp", "w")
	
	tila.out.write("\\begin{tikzpicture}\n")

def lopetaKuva():
	"""Lopeta kuvan, joka aloitettiin kutsulla aloita(), piirtäminen.
	LaTeX-ympäristö kutsuu yleensä aloitaKuva- ja lopetaKuva-funktioita
	automaattisesti."""
	
	tila.out.write("\\end{tikzpicture}\n")
	
	tila.out.close()
	os.rename("kuva-tmp-output.txt.tmp", "kuva-tmp-output.txt")

def nimeaPiste(P, nimi, suunta):
	"""Kirjoita LaTeX-koodina annettu 'nimi' pisteen P viereen, suunnilleen
	suuntaan 'suunta' (asteina)."""
	
	suunta = ((int(suunta) + 22) % 360) // 45
	nodedir = [(1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1)][suunta]
	
	nodepos = ""
	if nodedir[1] == -1:
		nodepos += "below "
	if nodedir[1] == 1:
		nodepos += "above "
	if nodedir[0] == -1:
		nodepos += "left "
	if nodedir[0] == 1:
		nodepos += "right "
	
	nodepos = nodepos[:-1]
	
	if nodedir[0] and nodedir[1]:
		nodepos += "=-0.05cm"
	else:
		nodepos += "=0.02cm"
	
	tila.out.write("\\draw[color={}] {} node[{}] {{{}}};\n".format(tila.asetukset['piirtovari'], tikzPiste(muunna(P)), nodepos, nimi))

class AsetusPalautin:
	"""Tallentaa konstruktorissaan asetukset ja palauttaa ne __exit__-funktiossaan."""
	
	def __init__(self):
		self.asetukset = tila.asetukset.copy()
	
	def __enter__(self):
		pass
	
	def __exit__(self, type, value, traceback):
		tila.asetukset = self.asetukset

def piste(P, nimi = "", suunta = 0):
	"""Piirrä piste 'P' kuvaan. Nimi laitetaan suuntaan 'suunta' (asteina)."""
	
	vari = tila.asetukset['piirtovari']
	tila.out.write("\\fill[color={}] {} circle (0.07);\n".format(vari, tikzPiste(muunna(P))))
	
	nimeaPiste(P, nimi, suunta)

# Funktiot piirtoasetusten muuttamiseen. Kaikkia funktioita voi käyttää
# with-lauseessa, jolloin with-blokin jälkeen asetukset palaavat ennalleen.

def skaalaaX(kerroin):
	"""Skaalaa X-koordinaatteja kertoimella 'kerroin'."""
	
	ret = AsetusPalautin()
	kerroin = float(kerroin)
	
	a, b = tila.asetukset['xmuunnos']
	tila.asetukset['xmuunnos'] = (kerroin * a, b)
	
	tila.asetukset['minX'] /= kerroin
	tila.asetukset['maxX'] /= kerroin
	
	return ret

def skaalaaY(kerroin):
	"""Skaalaa Y-koordinaatteja kertoimella 'kerroin'."""
	
	ret = AsetusPalautin()
	kerroin = float(kerroin)
	
	a, b = tila.asetukset['ymuunnos']
	tila.asetukset['ymuunnos'] = (kerroin * a, b)
	
	tila.asetukset['minY'] /= kerroin
	tila.asetukset['maxY'] /= kerroin
	
	return ret

def siirraX(siirto):
	"""Siirrä X-koordinaatteja."""
	
	ret = AsetusPalautin()
	
	a, b = tila.asetukset['xmuunnos']
	tila.asetukset['xmuunnos'] = (a, b + a * siirto)
	
	return ret

def siirraY(siirto):
	"""Siirrä Y-koordinaatteja."""
	
	ret = AsetusPalautin()
	
	a, b = tila.asetukset['ymuunnos']
	tila.asetukset['ymuunnos'] = (a, b + a * siirto)
	
	return ret

def skaalaa(kerroin):
	"""Skaalaa koordinaatteja kertoimella 'kerroin'."""
	ret = AsetusPalautin()
	
	skaalaaX(kerroin)
	skaalaaY(kerroin)
	
	return ret

def oletusasetukset():
	"""Palauttaa oletusasetukset."""
	
	ret = AsetusPalautin()
	
	tila.asetukset = tila.oletusasetukset.copy()
	
	return ret

def rajaa(minX = None, maxX = None, minY = None, maxY = None):
	"""Aseta X- tai Y-koordinaattien piirtoja rajaavia ala- ja ylärajoja."""
	
	ret = AsetusPalautin()
	
	if minX is not None:
		tila.asetukset['minX'] = minX
	
	if maxX is not None:
		tila.asetukset['maxX'] = maxX
	
	if minY is not None:
		tila.asetukset['minY'] = minY
	
	if maxY is not None:
		tila.asetukset['maxY'] = maxY
	
	return ret

def varaaRajaus():
	"""Varmista, että kuva käyttää ainakin koko nykyisen rajauksen. Kuvan on
	oltava rajattu sekä X- että Y-suunnassa."""
	
	def finite(x):
		return x != float("inf") and x != float("-inf")
	
	def valitse(a, b):
		if finite(a): return a
		return b
	
	x1 = valitse(tila.asetukset['minX'], tila.asetukset['maxX'])
	x2 = valitse(tila.asetukset['maxX'], tila.asetukset['minX'])
	y1 = valitse(tila.asetukset['minY'], tila.asetukset['maxY'])
	y2 = valitse(tila.asetukset['maxY'], tila.asetukset['minY'])
	
	if not finite(x1) or not finite(x2) or not finite(y1) or not finite(y2):
		raise ValueError("varaaRajaus: Kuvaa ei ole rajattu sekä X- että Y-suunnassa.")
	
	alku = muunna((x1, y1))
	loppu = muunna((x2, y2))
	tila.out.write("\\draw[opacity=0] {} -- {};\n".format(tikzPiste(alku), tikzPiste(loppu)))
	
	return AsetusPalautin()

def vari(uusivari):
	"""Aseta piirrossa käytettävä väri annettuun TiKZ-värikuvaukseen."""
	
	ret = AsetusPalautin()
	tila.asetukset['piirtovari'] = uusivari
	return ret

def paksuus(kerroin):
	"""Kerro piirrossa käytettävää viivan paksuutta kertoimella 'kerroin'."""
	
	ret = AsetusPalautin()
	tila.asetukset['piirtopaksuus'] *= kerroin
	return ret

def palautin():
	"""Ei tee mitään, mutta palauttaa AsetusPalauttimen, joten voidaan käyttää
	asetusten tallentamiseen withillä."""
	
	return AsetusPalautin()