# generation_arbre.py — Cercles compacts + noms multi-lignes (IDs sûrs, Graphviz only)

from __future__ import annotations
import json, re
import graphviz

def _norm_list2(lst):
    lst = list(lst or [])
    while len(lst) < 2:
        lst.append("Inconnu")
    return [x if x else "Inconnu" for x in lst[:2]]

def _fillcolor(sexe: str) -> str:
    return "#ADD8E6" if sexe == "H" else "#FFB6C1" if sexe == "F" else "#E6E6E6"

def _safe_id(raw: str, used: set, prefix: str = "n") -> str:
    """Fabrique un ID DOT sûr: [A-Za-z_][A-Za-z0-9_]*, unique."""
    base = re.sub(r"\W+", "_", (raw or "").strip()) or prefix
    if re.match(r"^\d", base):
        base = f"{prefix}_{base}"
    i, sid = 0, base
    while sid in used:
        i += 1
        sid = f"{base}_{i}"
    used.add(sid)
    return sid

def _labelize(name: str) -> str:
    """
    Réduit la largeur en écrivant les noms multi-mots sur plusieurs lignes.
    Exemple: 'Kévin Émile Bouchard' -> 'Kévin\\nÉmile\\nBouchard'
    On garde les traits d’union (Jean-Pierre) dans le même mot.
    """
    if not name:
        return ""
    # Nettoyage léger d'espaces multiples
    name = re.sub(r"\s+", " ", name.strip())
    # Remplace les espaces par des retours à la ligne
    return name.replace(" ", "\\n")

def creer_arbre_genealogique(data_json: str | dict) -> graphviz.Digraph:
    data = json.loads(data_json) if isinstance(data_json, str) else dict(data_json)

    dot = graphviz.Digraph(comment="Arbre Généalogique")
    dot.attr(rankdir="TB", splines="spline", concentrate="true")
    # Cercles compacts
    dot.attr(
        "node",
        shape="circle",
        style="filled",
        color="#39424e",
        fontname="DejaVu Sans",
        fontsize="11",
        width="0.45",          # cercle plus étroit (grandit si label très long)
        fixedsize="false",
        margin="0.02,0.02",    # bord fin
        labelloc="c"
    )
    dot.attr("edge", color="#555555")

    used_ids: set[str] = set()
    id_of: dict[str, str] = {}     # nom humain -> id DOT
    created_nodes: set[str] = set()
    couple_map: dict[frozenset[str], str] = {}  # {idA,idB} -> idCouple

    def ensure_person_node(name: str, sexe: str = "Inconnu"):
        if not name or name == "Inconnu":
            return None
        if name in id_of:
            return id_of[name]
        nid = _safe_id(name, used_ids, prefix="p")
        id_of[name] = nid
        if nid not in created_nodes:
            dot.node(nid, label=_labelize(name), fillcolor=_fillcolor(sexe))
            created_nodes.add(nid)
        return nid

    # 1) créer tous les nœuds connus
    for person, info in data.items():
        ensure_person_node(person, info.get("sexe", "Inconnu"))

    # 2) relations
    for person, info in data.items():
        pid = ensure_person_node(person, info.get("sexe", "Inconnu"))
        parents = _norm_list2(info.get("parent"))
        conjoint = (info.get("conjoint") or "").strip()

        mere, pere = parents
        mere_id = ensure_person_node(mere) if mere != "Inconnu" else None
        pere_id = ensure_person_node(pere) if pere != "Inconnu" else None

        # Parents -> enfant
        if mere_id and pere_id:
            key = frozenset({mere_id, pere_id})
            if key not in couple_map:
                cid = _safe_id("couple", used_ids, prefix="c")
                couple_map[key] = cid
                # Point-couple minuscule
                dot.node(cid, "", shape="point", width="0.01")
                dot.edge(mere_id, cid)
                dot.edge(pere_id, cid)
                # Partenaires au même niveau
                sg = graphviz.Digraph(name=f"rank_{cid}")
                sg.attr(rank="same")
                sg.node(mere_id); sg.node(pere_id)
                dot.subgraph(sg)
            dot.edge(couple_map[key], pid)
        elif mere_id or pere_id:
            dot.edge(mere_id or pere_id, pid)

        # Conjoint (pointillé) + même niveau
        if conjoint:
            cid2 = ensure_person_node(conjoint)
            if cid2:
                dot.edge(pid, cid2, style="dotted")
                sg2 = graphviz.Digraph(name=f"rank_pair_{min(pid,cid2)}_{max(pid,cid2)}")
                sg2.attr(rank="same")
                sg2.node(pid); sg2.node(cid2)
                dot.subgraph(sg2)

    return dot
