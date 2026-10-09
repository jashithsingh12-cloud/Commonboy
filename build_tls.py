import xml.etree.ElementTree as ET

net = ET.parse("junction.net.xml").getroot()
links = sorted(
    (int(c.get("linkIndex")), c.get("from"))
    for c in net.iter("connection") if c.get("tl") == "C"
)
NS_ = ["N_in", "S_in"]
EW_ = ["E_in", "W_in"]

def state(active, sig):
    return "".join(sig if frm in active else "r" for _, frm in links)

phases = [
    (state(NS_, "G"), 30),
    (state(NS_, "y"), 3),
    (state([], "r"), 2),
    (state(EW_, "G"), 30),
    (state(EW_, "y"), 3),
    (state([], "r"), 2),
]

out = ['<additional>',
       '  <tlLogic id="C" type="static" programID="fixed" offset="0">']
for s, d in phases:
    out.append(f'    <phase duration="{d}" state="{s}"/>')
out += ['  </tlLogic>', '</additional>']
open("tls.add.xml", "w").write("\n".join(out) + "\n")
print("links:", len(links), "tls.add.xml written")