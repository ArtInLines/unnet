import smolXML as xml
import os

p1 = "data"
for d1 in os.listdir(p1):
	p2 = p1 + "/" + d1
	for d2 in os.listdir(p2):
		p3 = p2 + "/" + d2
		for f in os.listdir(p3):
			fpath = p3 + "/" + f
			if not fpath.endswith(".xml"):
				continue
			print(fpath)
			root = xml.parseFile(fpath)
			docNumbers = root.getAllElementsOfType("docNumber")
			if len(docNumbers) == 0:
				print("No doc-number in " + fpath)