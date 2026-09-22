from pathlib import Path
import sys,json
B=Path(__file__).resolve().parent
sys.path.insert(0,str(B.parent))
from conditional_audit import main
reviews=json.loads((B/'sense_reviews.json').read_text())
lookup={(x['pack'],x['overall'],x['word']):x for x in reviews}
if __name__=='__main__':main(sense_reviews=lookup,output_base=B)
