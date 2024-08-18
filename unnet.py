import smolXML as xml
import os
import time

class LOG:
	INFO = 0
	WARN = 1
	ERR  = 2
	SUCC = 3
	STR_INFO = '\033[37m[INFO]: '
	STR_WARN = '\033[33m[WARN]: '
	STR_ERR  = '\033[31m[ERR]:  '
	STR_SUCC = '\033[32m[SUCC]: '
	COL_DONE = '\033[0m'

	@staticmethod
	def get_str(log_level: int, s: str) -> str:
		if log_level == LOG.INFO:
			s = LOG.STR_INFO + s + LOG.COL_DONE
		elif log_level == LOG.WARN:
			s = LOG.STR_WARN + s + LOG.COL_DONE
		elif log_level == LOG.ERR:
			s = LOG.STR_ERR  + s + LOG.COL_DONE
		elif log_level == LOG.SUCC:
			s = LOG.STR_SUCC + s + LOG.COL_DONE
		else:
			print(f"log() received unexpected value for log_level: {log_level}".ljust(max_line))
			assert(False)
		return s

max_line: int = 0
def log(log_level: int, s: str, new_line: bool = True):
	global max_line
	s = LOG.get_str(log_level, s)
	max_line = max(max_line, len(s))
	s = s.ljust(max_line)
	endc: str
	if new_line:
		max_line = 0
		endc = '\n'
	else:
		endc = '\r'
	print(s, end=endc)

def create_network(csv_path: str):
	csv = open(csv_path, "w", encoding="utf8")
	csv.write("from,to\n")

	files = []
	p1 = "data"
	for d1 in os.listdir(p1):
		p2 = os.path.join(p1, d1)
		if not os.path.isdir(p2):
			continue
		for d2 in os.listdir(p2):
			p3 = os.path.join(p2, d2)
			if not os.path.isdir(p2):
				continue
			for f in os.listdir(p3):
				fpath = os.path.join(p3, f)
				if fpath.endswith(".xml"):
					files.append(fpath)

	files_wo_edges = []
	edge_count     = 0
	files_count    = len(files)
	log(LOG.INFO, f"Found {files_count} XML files")

	for i in range(files_count):
		log(LOG.INFO, f"{100*(i/files_count):.3f}% done | {edge_count} edges found", False)
		fpath = files[i]
		root = xml.parseFile(fpath)
		docNums = root.getAllElementsOfType("docNumber")
		if len(docNums) == 0:
			log(LOG.ERR, f"No doc-number in {fpath}")
			continue
		if len(docNums[0].children) != 1:
			log(LOG.ERR, f"Found doc-number without exactly one string-child in {fpath}: {docNums[0]}")
			continue

		initial_edge_count = edge_count
		docNum = docNums[0].getStrVal()
		anchors = root.getAllElementsOfType("a")
		for anchor in anchors:
			if "href" not in anchor.attrs:
				log(LOG.WARN, f"anchor without href attribute in {fpath}: {anchor}")
				continue
			link: str = anchor.attrs["href"].strip()
			link_parts = link.split("undocs.org/")
			if len(link_parts) != 2:
				# log(LOG.WARN, f"Found link referring outside of undocs.org in {fpath}: '{link}'")
				continue
			other = "".join(link_parts[1].split("en/")).split("(")[0]
			csv.write(f"{docNum},{other}\n")
			edge_count += 1
		if edge_count == initial_edge_count:
			files_wo_edges.append(fpath)
	if len(files_wo_edges) > 0:
		log(LOG.WARN, f"{len(files_wo_edges)} files found without outgoing edges")
	csv.close()
	log(LOG.INFO, f"{edge_count} edges successfully written to {csv_path}")


def main():
	start_time = time.time()
	csv_path: str = os.path.join("data", "edges.csv")
	create_network(csv_path)

	elapsed = time.time() - start_time
	if elapsed > 60:
		minutes = int(elapsed/60)
		log(LOG.INFO, f"Program took {minutes}m {(elapsed - minutes*60):.3f}s")
	else:
		log(LOG.INFO, f"Program took {elapsed:.3f}s")


if __name__ == "__main__":
	main()