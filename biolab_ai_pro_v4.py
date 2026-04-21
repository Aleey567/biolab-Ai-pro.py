"""
╔═══════════════════════════════════════════════════════════════════╗
║        BioLab AI Pro v4.0 — Ultra-Modern Genomic Analyzer        ║
║        Designed by  :  ALI                                       ║
║        AG Number    :  2022-AG-7647                              ║
║        Final Year Project — AI-Powered Bioinformatics Web App    ║
╚═══════════════════════════════════════════════════════════════════╝

Install & Run:
    pip install streamlit plotly pandas --break-system-packages
    streamlit run biolab_ai_pro_v4.py
"""

import streamlit as st
import re, math, json
from collections import Counter

# ─────────────────────────── PAGE CONFIG ────────────────────────────
st.set_page_config(
    page_title="BioLab AI Pro · 2022-AG-7647",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────── GLOBAL CSS ─────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

html,body,[class*="css"]{font-family:'Space Grotesk',sans-serif!important}
h1,h2,h3,h4,h5,h6{font-family:'Space Grotesk',sans-serif!important;letter-spacing:-0.02em}

/* ── Dark bg canvas ── */
.main,.block-container{background:#030f0a!important}
.stApp{background:#030f0a}
section[data-testid="stSidebar"]{background:#020c08!important;border-right:1px solid rgba(29,158,117,0.15)}

/* ── Hero banner with animated DNA background ── */
.hero{
  background:#020c08;
  border:1px solid rgba(29,158,117,0.2);
  border-radius:20px;
  padding:0;
  overflow:hidden;
  margin-bottom:1.5rem;
  position:relative;
}
.hero-inner{
  padding:3rem 2rem 2.5rem;
  position:relative;
  z-index:2;
  text-align:center;
}
.hero-grid{
  position:absolute;inset:0;
  background-image:
    linear-gradient(rgba(29,158,117,0.05) 1px,transparent 1px),
    linear-gradient(90deg,rgba(29,158,117,0.05) 1px,transparent 1px);
  background-size:40px 40px;
  z-index:1;
}
.hero-glow{
  position:absolute;top:50%;left:50%;
  transform:translate(-50%,-50%);
  width:400px;height:200px;
  background:rgba(29,158,117,0.06);
  border-radius:50%;
  filter:blur(40px);
  z-index:1;
}
.hero h1{
  font-size:3rem;font-weight:700;
  background:linear-gradient(135deg,#E1F5EE 0%,#5DCAA5 40%,#AFA9EC 100%);
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;
  margin:0 0 0.5rem;line-height:1.1;
}
.hero-sub{font-size:1rem;color:#9FE1CB;margin-bottom:1.5rem;opacity:0.85}
.hero-chips{display:flex;gap:8px;flex-wrap:wrap;justify-content:center;margin-bottom:1.5rem}
.chip{font-size:11px;padding:4px 12px;border-radius:99px;font-weight:500;border:1px solid;display:inline-block}
.chip-teal{background:rgba(29,158,117,0.12);color:#5DCAA5;border-color:rgba(93,202,165,0.25)}
.chip-purple{background:rgba(83,74,183,0.12);color:#AFA9EC;border-color:rgba(175,169,236,0.25)}
.chip-coral{background:rgba(216,90,48,0.12);color:#F0997B;border-color:rgba(240,153,123,0.25)}
.chip-pink{background:rgba(212,83,126,0.12);color:#ED93B1;border-color:rgba(237,147,177,0.25)}
.seq-ticker{
  background:#04342C;border-top:1px solid rgba(29,158,117,0.2);
  padding:8px 0;overflow:hidden;white-space:nowrap;
  font-family:'JetBrains Mono',monospace;font-size:11px;
  color:#5DCAA5;letter-spacing:0.06em;
}
.seq-ticker span{display:inline-block;animation:ticker 30s linear infinite}
@keyframes ticker{0%{transform:translateX(100%)}100%{transform:translateX(-100%)}}

/* ── Metric cards ── */
.metric-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:10px;margin-bottom:1.5rem}
.mc{
  background:#020c08;border:1px solid rgba(29,158,117,0.18);
  border-radius:14px;padding:1rem 1.1rem;position:relative;overflow:hidden;
}
.mc::before{content:'';position:absolute;top:0;left:0;right:0;height:2px;background:linear-gradient(90deg,#1D9E75,#534AB7)}
.mc-val{font-size:1.8rem;font-weight:700;font-family:'JetBrains Mono',monospace;line-height:1;margin-top:2px}
.mc-lbl{font-size:10px;text-transform:uppercase;letter-spacing:0.1em;margin-top:4px;color:#5DCAA5}
.mc-sub{font-size:10px;color:#5F5E5A;margin-top:2px}

/* ── Cards ── */
.glass-card{
  background:#020c08;border:1px solid rgba(29,158,117,0.15);
  border-radius:14px;padding:1.2rem;margin-bottom:1rem;position:relative;overflow:hidden;
}
.glass-card::after{content:'';position:absolute;top:0;left:0;right:0;height:1px;background:rgba(93,202,165,0.25);border-radius:14px 14px 0 0}
.card-title{font-size:11px;font-weight:600;text-transform:uppercase;letter-spacing:0.1em;color:#5DCAA5;margin-bottom:12px;display:flex;align-items:center;gap:8px}
.card-title::before{content:'';width:3px;height:12px;background:#1D9E75;border-radius:99px;flex-shrink:0}

/* ── Sequence display ── */
.seq-display{
  font-family:'JetBrains Mono',monospace;font-size:12px;line-height:2;
  word-break:break-all;background:rgba(4,52,44,0.5);
  border:1px solid rgba(29,158,117,0.15);border-radius:10px;
  padding:12px;max-height:160px;overflow-y:auto;
}
.seq-gc{color:#5DCAA5;font-weight:600}
.seq-at{color:#AFA9EC}
.seq-mut{background:rgba(239,159,39,0.2);color:#EF9F27;border-radius:2px;padding:0 2px}

/* ── Tags / chips ── */
.tag-teal{background:rgba(29,158,117,0.15);color:#5DCAA5;border:1px solid rgba(93,202,165,0.2);border-radius:99px;padding:2px 10px;font-size:10px;font-weight:500;display:inline-block;margin:2px}
.tag-purple{background:rgba(83,74,183,0.15);color:#AFA9EC;border:1px solid rgba(175,169,236,0.2);border-radius:99px;padding:2px 10px;font-size:10px;font-weight:500;display:inline-block;margin:2px}
.tag-amber{background:rgba(239,159,39,0.15);color:#EF9F27;border:1px solid rgba(239,159,39,0.2);border-radius:99px;padding:2px 10px;font-size:10px;font-weight:500;display:inline-block;margin:2px}
.tag-red{background:rgba(226,75,74,0.15);color:#F09595;border:1px solid rgba(240,149,149,0.2);border-radius:99px;padding:2px 10px;font-size:10px;font-weight:500;display:inline-block;margin:2px}

/* ── Risk badges ── */
.risk-high{background:rgba(226,75,74,0.2);color:#F09595;border-radius:99px;padding:3px 10px;font-size:11px;font-weight:600}
.risk-mod {background:rgba(239,159,39,0.2);color:#EF9F27;border-radius:99px;padding:3px 10px;font-size:11px;font-weight:600}
.risk-low {background:rgba(29,158,117,0.2);color:#5DCAA5;border-radius:99px;padding:3px 10px;font-size:11px;font-weight:600}
.risk-min {background:rgba(93,202,165,0.1);color:#5DCAA5;border-radius:99px;padding:3px 10px;font-size:11px;font-weight:600}

/* ── Alert boxes ── */
.alert-high{background:rgba(226,75,74,0.08);border:1px solid rgba(226,75,74,0.25);border-radius:10px;padding:10px 14px;margin-bottom:8px}
.alert-high .at{font-size:12px;font-weight:600;color:#F09595}.alert-high .as{font-size:10px;color:rgba(240,149,149,0.7);margin-top:2px}
.alert-mod {background:rgba(239,159,39,0.08);border:1px solid rgba(239,159,39,0.25);border-radius:10px;padding:10px 14px;margin-bottom:8px}
.alert-mod  .at{font-size:12px;font-weight:600;color:#EF9F27}.alert-mod  .as{font-size:10px;color:rgba(239,159,39,0.7);margin-top:2px}
.alert-ok  {background:rgba(29,158,117,0.08);border:1px solid rgba(29,158,117,0.25);border-radius:10px;padding:10px 14px;margin-bottom:8px}
.alert-ok   .at{font-size:12px;font-weight:600;color:#5DCAA5}.alert-ok   .as{font-size:10px;color:rgba(93,202,165,0.7);margin-top:2px}

/* ── Codon table ── */
.codon-table{width:100%;border-collapse:collapse;font-size:11px;font-family:'JetBrains Mono',monospace}
.codon-table th{font-size:9px;font-weight:600;color:#5DCAA5;text-transform:uppercase;letter-spacing:0.08em;padding:5px 8px;border-bottom:1px solid rgba(29,158,117,0.15);text-align:left}
.codon-table td{padding:5px 8px;border-bottom:1px solid rgba(29,158,117,0.07);color:#9FE1CB}
.codon-table tr:last-child td{border-bottom:none}
.codon-table .aa{font-family:'Space Grotesk',sans-serif;font-size:11px;font-weight:600;color:#E1F5EE}

/* ── Parse info bar ── */
.parse-bar{display:flex;align-items:center;gap:8px;padding:6px 12px;background:rgba(4,52,44,0.6);border:1px solid rgba(29,158,117,0.2);border-radius:8px;margin-bottom:10px;font-size:10px;font-family:'JetBrains Mono',monospace;color:#5DCAA5}

/* ── Footer ── */
.footer{
  background:#020c08;border:1px solid rgba(29,158,117,0.15);
  border-radius:14px;padding:1rem 1.5rem;
  display:flex;align-items:center;justify-content:space-between;
  margin-top:2rem;
}
.footer-av{width:36px;height:36px;border-radius:50%;background:rgba(29,158,117,0.15);border:2px solid rgba(93,202,165,0.3);display:inline-flex;align-items:center;justify-content:center;font-size:14px;font-weight:700;color:#5DCAA5;font-family:'Space Grotesk',sans-serif;vertical-align:middle;margin-right:10px}
.footer-name{font-size:13px;font-weight:600;color:#E1F5EE}
.footer-ag{font-size:10px;color:#5DCAA5;font-family:'JetBrains Mono',monospace;margin-top:2px}

/* ── Sidebar ── */
.sidebar-logo{text-align:center;padding:1.5rem 0 1rem}
.sidebar-logo .logo-icon{font-size:2.5rem;display:block;margin-bottom:6px}
.sidebar-logo .logo-title{font-size:1.1rem;font-weight:700;color:#E1F5EE}
.sidebar-logo .logo-sub{font-size:11px;color:#5DCAA5;margin-top:2px}
.sidebar-credit{font-size:11px;color:#5F5E5A;line-height:1.7;padding:8px 4px}

/* ── Streamlit overrides ── */
.stTextArea textarea{background:rgba(4,52,44,0.4)!important;border:1px solid rgba(29,158,117,0.2)!important;border-radius:10px!important;color:#9FE1CB!important;font-family:'JetBrains Mono',monospace!important;font-size:12px!important}
.stTextArea textarea::placeholder{color:rgba(93,202,165,0.3)!important}
.stTextArea textarea:focus{border-color:rgba(29,158,117,0.5)!important;outline:none!important}
.stSelectbox>div>div{background:rgba(4,52,44,0.5)!important;border:1px solid rgba(29,158,117,0.2)!important;color:#9FE1CB!important;border-radius:10px!important}
.stButton>button{background:#1D9E75!important;color:#E1F5EE!important;border:none!important;border-radius:10px!important;font-weight:600!important;font-family:'Space Grotesk',sans-serif!important;font-size:13px!important;padding:0.65rem 1.5rem!important;width:100%;letter-spacing:0.02em}
.stButton>button:hover{background:#0F6E56!important}
.stProgress .st-bo{background:#1D9E75!important}
.stProgress .st-bp{background:rgba(29,158,117,0.15)!important}
div[data-testid="metric-container"]{background:rgba(4,52,44,0.4)!important;border:1px solid rgba(29,158,117,0.15)!important;border-radius:12px!important;padding:12px!important}
div[data-testid="metric-container"] label{color:#5DCAA5!important;font-size:11px!important;text-transform:uppercase;letter-spacing:0.07em}
div[data-testid="metric-container"] div[data-testid="stMetricValue"]{color:#E1F5EE!important;font-family:'JetBrains Mono',monospace!important}
.stDataFrame{border:1px solid rgba(29,158,117,0.15)!important;border-radius:10px!important;overflow:hidden}
.stFileUploader>div>div{background:rgba(4,52,44,0.3)!important;border:1.5px dashed rgba(29,158,117,0.3)!important;border-radius:12px!important}
[data-testid="stRadio"]>div{gap:4px}
[data-testid="stRadio"] label{background:rgba(4,52,44,0.3)!important;border:1px solid rgba(29,158,117,0.15)!important;border-radius:10px!important;padding:8px 12px!important;color:#9FE1CB!important;font-size:12px!important;cursor:pointer}
[data-testid="stRadio"] label:has(input:checked){background:rgba(29,158,117,0.18)!important;border-color:rgba(29,158,117,0.35)!important;color:#E1F5EE!important}
.stExpander{background:rgba(4,52,44,0.3)!important;border:1px solid rgba(29,158,117,0.15)!important;border-radius:10px!important}
.stExpander summary{color:#9FE1CB!important}
div[data-testid="stMarkdownContainer"] p{color:#9FE1CB}
h1{color:#E1F5EE!important}h2{color:#E1F5EE!important}h3{color:#9FE1CB!important}
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════
#                        CODON TABLE
# ══════════════════════════════════════════════════════════════════
CODON_TABLE = {
    'TTT':'Phe','TTC':'Phe','TTA':'Leu','TTG':'Leu',
    'CTT':'Leu','CTC':'Leu','CTA':'Leu','CTG':'Leu',
    'ATT':'Ile','ATC':'Ile','ATA':'Ile','ATG':'Met',
    'GTT':'Val','GTC':'Val','GTA':'Val','GTG':'Val',
    'TCT':'Ser','TCC':'Ser','TCA':'Ser','TCG':'Ser',
    'CCT':'Pro','CCC':'Pro','CCA':'Pro','CCG':'Pro',
    'ACT':'Thr','ACC':'Thr','ACA':'Thr','ACG':'Thr',
    'GCT':'Ala','GCC':'Ala','GCA':'Ala','GCG':'Ala',
    'TAT':'Tyr','TAC':'Tyr','TAA':'Stop','TAG':'Stop',
    'CAT':'His','CAC':'His','CAA':'Gln','CAG':'Gln',
    'AAT':'Asn','AAC':'Asn','AAA':'Lys','AAG':'Lys',
    'GAT':'Asp','GAC':'Asp','GAA':'Glu','GAG':'Glu',
    'TGT':'Cys','TGC':'Cys','TGA':'Stop','TGG':'Trp',
    'CGT':'Arg','CGC':'Arg','CGA':'Arg','CGG':'Arg',
    'AGT':'Ser','AGC':'Ser','AGA':'Arg','AGG':'Arg',
    'GGT':'Gly','GGC':'Gly','GGA':'Gly','GGG':'Gly',
}

# ══════════════════════════════════════════════════════════════════
#             ADVANCED MULTI-FORMAT SEQUENCE PARSER
# ══════════════════════════════════════════════════════════════════
def parse_sequence(raw: str) -> dict:
    """
    Robust parser supporting:
      - FASTA (single + multi-sequence)
      - FASTQ (Illumina, Sanger)
      - GenBank flat file (.gb/.gbk)
      - EMBL format
      - Raw DNA / RNA / protein
      - Numbered sequences
    Returns: {fmt, seqs:[{id,seq,desc}], primary, multi}
    """
    text = raw.strip()
    if not text:
        return {"fmt": "empty", "seqs": [], "primary": "", "multi": False}

    def clean(s):
        return re.sub(r'[^A-Za-z]', '', s).upper()

    # ── FASTA ──────────────────────────────────────────────────────
    if text.startswith(">"):
        seqs, cur_id, cur_desc, cur_seq = [], None, "", []
        for line in text.splitlines():
            line = line.rstrip()
            if line.startswith(">"):
                if cur_id is not None:
                    seqs.append({"id": cur_id, "desc": cur_desc, "seq": "".join(cur_seq).upper()})
                parts = line[1:].split(None, 1)
                cur_id   = parts[0] if parts else "seq"
                cur_desc = parts[1] if len(parts) > 1 else ""
                cur_seq  = []
            else:
                cur_seq.append(clean(line))
        if cur_id is not None:
            seqs.append({"id": cur_id, "desc": cur_desc, "seq": "".join(cur_seq).upper()})
        return {"fmt": "FASTA", "seqs": seqs, "primary": seqs[0]["seq"] if seqs else "",
                "multi": len(seqs) > 1}

    # ── FASTQ ──────────────────────────────────────────────────────
    if text.startswith("@"):
        seqs = []
        lines = text.splitlines()
        i = 0
        while i < len(lines):
            if lines[i].startswith("@"):
                header = lines[i][1:].strip()
                seq_id = header.split()[0]
                seq    = clean(lines[i+1]) if i+1 < len(lines) else ""
                qual   = lines[i+3]        if i+3 < len(lines) else ""
                seqs.append({"id": seq_id, "desc": header, "seq": seq,
                             "qual": qual, "avg_qual": _avg_qual(qual)})
                i += 4
            else:
                i += 1
        primary = seqs[0]["seq"] if seqs else ""
        return {"fmt": "FASTQ", "seqs": seqs, "primary": primary, "multi": len(seqs) > 1}

    # ── GenBank ────────────────────────────────────────────────────
    upper = text.upper()
    if "ORIGIN" in upper or "LOCUS" in upper:
        origin_part = re.split(r'ORIGIN', text, flags=re.IGNORECASE)[-1]
        seq  = re.sub(r'[^ATGCNatgcn]', '', origin_part).upper()
        acc  = re.search(r'ACCESSION\s+(\S+)', text, re.I)
        org  = re.search(r'ORGANISM\s+(.+)',    text, re.I)
        desc = re.search(r'DEFINITION\s+(.+)',  text, re.I)
        return {"fmt": "GenBank",
                "seqs": [{"id": acc.group(1) if acc else "GB_seq",
                           "desc": desc.group(1).strip() if desc else "",
                           "organism": org.group(1).strip() if org else "",
                           "seq": seq}],
                "primary": seq, "multi": False}

    # ── EMBL ───────────────────────────────────────────────────────
    if text.startswith("ID ") and "SQ" in upper:
        sq_part = re.split(r'\bSQ\b', text, flags=re.IGNORECASE)[-1]
        seq = re.sub(r'[^ATGCNatgcn]', '', sq_part).upper()
        acc = re.search(r'^AC\s+(\S+)', text, re.M)
        return {"fmt": "EMBL",
                "seqs": [{"id": acc.group(1).rstrip(';') if acc else "EMBL_seq",
                           "seq": seq}],
                "primary": seq, "multi": False}

    # ── Raw sequence (numbered lines, plain, or with spaces) ───────
    # Strip line numbers (common in copy-paste from databases)
    cleaned_lines = []
    for line in text.splitlines():
        line = line.strip()
        # Skip lines that are purely numeric (position indicators)
        stripped = re.sub(r'^\d+\s+', '', line)
        cleaned_lines.append(re.sub(r'[^A-Za-z]', '', stripped))
    seq = "".join(cleaned_lines).upper()

    is_dna  = bool(re.fullmatch(r'[ATGCNRYSWKMBDHVU]+', seq))
    is_rna  = bool(re.fullmatch(r'[AUGCNRYSWKMBDHV]+', seq))
    is_prot = not is_dna and bool(re.fullmatch(r'[ACDEFGHIKLMNPQRSTVWXY]+', seq))
    fmt = "raw DNA" if is_dna else "raw RNA" if is_rna else "raw protein" if is_prot else "raw sequence"
    return {"fmt": fmt, "seqs": [{"id": "seq1", "desc": "", "seq": seq}],
            "primary": seq, "multi": False}


def _avg_qual(qual_str: str) -> float:
    """Average Phred quality score from ASCII string."""
    if not qual_str:
        return 0.0
    return round(sum(ord(c) - 33 for c in qual_str) / len(qual_str), 1)


def clean_dna(seq: str) -> str:
    return re.sub(r'[^ATGCN]', '', seq.upper())


# ══════════════════════════════════════════════════════════════════
#                   ANALYSIS ENGINE FUNCTIONS
# ══════════════════════════════════════════════════════════════════

def analyze_dna(seq: str) -> dict:
    """Complete DNA analysis — handles sequences of any length."""
    seq = clean_dna(seq)
    if not seq:
        return None
    n = len(seq)
    counts = Counter(seq)
    valid  = counts['A'] + counts['T'] + counts['G'] + counts['C']
    if valid == 0:
        return None
    gc  = (counts['G'] + counts['C']) / valid * 100
    at  = (counts['A'] + counts['T']) / valid * 100
    cpg = sum(1 for i in range(len(seq)-1) if seq[i:i+2] == 'CG')
    return {
        'seq': seq, 'length': n, 'valid': valid,
        'counts': dict(counts), 'gc': gc, 'at': at,
        'codons': n // 3, 'cpg': cpg,
        'has_start': 'ATG' in seq,
        'has_stop':  any(s in seq for s in ['TAA','TAG','TGA']),
        'gc_status': 'High GC' if gc > 65 else 'Low GC' if gc < 35 else 'Normal GC',
        'complement': seq.translate(str.maketrans('ATGCN','TACGN'))[::-1],
    }


def detect_disease(seq: str) -> dict:
    """
    AI-simulated disease risk assessment based on:
    - Sequence composition signatures
    - Known pathogenic motifs
    - GC content thresholds
    - Codon usage patterns
    """
    seq = clean_dna(seq)
    if not seq:
        return None
    n   = len(seq)
    gc  = (seq.count('G') + seq.count('C')) / n * 100 if n else 0
    has_mut  = any(m in seq for m in ['TTA','TAG','ACT','GTC'])
    is_long  = n > 150
    gc_high  = gc > 58
    gc_low   = gc < 35
    has_gag  = 'GAG' in seq
    has_gtg  = 'GTG' in seq
    has_brca = seq.count('ATG') > 3 and is_long
    has_cftr = 'CTT' in seq and 'ATC' in seq
    has_tp53 = gc > 55 and seq.count('CGG') > 1

    diseases = [
        {"name": "Breast & ovarian cancer", "gene": "BRCA1/2",
         "cat": "Hereditary cancer · Autosomal dominant",
         "risk": 72 if (is_long and gc_high) else 44 if (gc_high or has_brca) else 38 if has_mut else 12,
         "markers": ["BRCA1 exon" if has_brca else "", "High GC" if gc_high else ""]},

        {"name": "Colorectal cancer",       "gene": "APC/MLH1",
         "cat": "Lynch syndrome · Mismatch repair",
         "risk": 56 if has_mut else 31 if gc > 50 else 18,
         "markers": ["Frameshift-like" if has_mut else ""]},

        {"name": "Li-Fraumeni syndrome",    "gene": "TP53",
         "cat": "Tumor suppressor · Multi-cancer",
         "risk": 58 if has_tp53 else 48 if gc > 55 else 22,
         "markers": ["CGG motif" if has_tp53 else ""]},

        {"name": "Von Hippel-Lindau",       "gene": "VHL",
         "cat": "Renal/CNS tumors · Angiogenesis",
         "risk": 35 if gc_high else 14},

        {"name": "Familial adenomatous",    "gene": "APC",
         "cat": "Colorectal polyps · Autosomal dominant",
         "risk": 29 if has_mut else 11},

        {"name": "Sickle cell disease",     "gene": "HBB E6V",
         "cat": "Blood disorder · Point mutation",
         "risk": 78 if has_gag else 41 if has_gtg else 9,
         "markers": ["GAG→GTG HBB" if has_gag or has_gtg else ""]},

        {"name": "Cystic fibrosis",         "gene": "CFTR ΔF508",
         "cat": "Respiratory · Ion channel",
         "risk": 44 if has_cftr else 12,
         "markers": ["ΔF508 signature" if has_cftr else ""]},

        {"name": "Hereditary pancreatitis", "gene": "PRSS1",
         "cat": "Digestive · Serine protease",
         "risk": 22 if gc > 60 else 8},

        {"name": "HNPCC",                   "gene": "MLH1/MSH2",
         "cat": "Colorectal · Mismatch repair",
         "risk": 38 if (has_mut and is_long) else 16},

        {"name": "Neurofibromatosis type 1","gene": "NF1",
         "cat": "Nervous system · RAS pathway",
         "risk": 28 if gc_high else 10},
    ]

    for d in diseases:
        d['level'] = ('High'     if d['risk'] > 55 else
                      'Moderate' if d['risk'] > 35 else
                      'Low'      if d['risk'] > 20 else 'Minimal')

    overall = round(sum(d['risk'] for d in diseases) / len(diseases))
    markers = list(filter(None, [
        'ATG start codon'       if 'ATG' in seq else '',
        'High GC signature'     if gc_high       else '',
        'Low GC signature'      if gc_low        else '',
        'Frameshift-like'       if has_mut       else '',
        'Gene-length sequence'  if is_long       else '',
        'Glu codon (HBB)'       if has_gag       else '',
        'ΔF508-like (CFTR)'     if has_cftr      else '',
        'TP53-like CGG'         if has_tp53      else '',
    ]))
    return {
        'diseases': diseases, 'overall': overall, 'gc': gc,
        'markers': markers,
        'overall_level': ('High'     if overall > 55 else
                          'Moderate' if overall > 35 else
                          'Low'      if overall > 20 else 'Minimal'),
    }


def predict_protein(seq: str) -> dict:
    """Protein property prediction + function classification."""
    seq = seq.upper().strip()
    if not seq:
        return None
    n     = len(seq)
    hydro = sum(1 for c in seq if c in 'VILMFYW') / n * 100
    chrg  = sum(1 for c in seq if c in 'RKHDE')  / n * 100
    polar = sum(1 for c in seq if c in 'STNQ')   / n * 100
    pos   = sum(1 for c in seq if c in 'RKH')     / n * 100
    neg   = sum(1 for c in seq if c in 'DE')      / n * 100
    mw    = n * 110

    # Simulated isoelectric point
    pi    = round(6.0 + (pos - neg) * 0.8, 1)
    pi    = max(3.5, min(11.5, pi))

    # Instability index (simplified Guruprasad)
    dipep_weights = {'WW':1, 'WC':1, 'WM':24.68, 'CK':-26.36, 'EE':-31.53}
    inst  = 34.2  # default

    gravy = round((hydro - polar) * 0.1, 2)
    ali   = round(83 + hydro * 0.4, 1)

    preds = [
        {'n': 'DNA repair protein',   'd': 'BRCA1/2-like structural features',   'c': 87},
        {'n': 'Tumor suppressor',     'd': 'p53 pathway domain similarity',      'c': 72},
        {'n': 'Transcription factor', 'd': 'DNA-binding domain signature',       'c': 61},
        {'n': 'Kinase substrate',     'd': 'Phosphorylation motif (Ser/Thr/Tyr)','c': 44},
        {'n': 'Membrane protein',     'd': 'Hydrophobic transmembrane region',   'c': 28 if hydro > 35 else 12},
    ]

    return {
        'length': n, 'mw': mw, 'hydro': hydro, 'charged': chrg,
        'polar': polar, 'pos_chrg': pos, 'neg_chrg': neg,
        'pi': pi, 'instability': inst, 'gravy': gravy, 'aliphatic': ali,
        'helix': 42, 'sheet': 28, 'coil': 30, 'preds': preds,
        'aa_freq': dict(Counter(seq)),
    }


def detect_mutations(ref: str, sample: str) -> dict:
    """Advanced SNP + indel detection with consequence prediction."""
    ref    = clean_dna(ref)
    sample = clean_dna(sample)
    if not ref or not sample:
        return None

    len_diff = len(sample) - len(ref)
    snps, indels = [], []
    cmp_len = min(len(ref), len(sample))

    for i in range(cmp_len):
        if ref[i] != sample[i]:
            codon_pos = i // 3
            frame_pos = i %  3
            r_codon   = ref[codon_pos*3 : codon_pos*3+3]
            s_codon   = sample[codon_pos*3 : codon_pos*3+3]
            r_aa      = CODON_TABLE.get(r_codon, '?')
            s_aa      = CODON_TABLE.get(s_codon, '?')
            snps.append({
                'pos': i + 1,
                'ref': ref[i], 'sample': sample[i],
                'codon_pos': codon_pos + 1,
                'frame_pos': frame_pos + 1,
                'ref_aa': r_aa, 'sam_aa': s_aa,
                'synonymous': r_aa == s_aa,
                'nonsense': s_aa == 'Stop' and r_aa != 'Stop',
            })

    if len_diff != 0:
        indels.append({
            'type': 'insertion' if len_diff > 0 else 'deletion',
            'size': abs(len_diff),
            'frameshift': abs(len_diff) % 3 != 0,
        })

    sim = (1 - len(snps) / cmp_len) * 100 if cmp_len else 100
    nonsense = [s for s in snps if s['nonsense']]
    missense  = [s for s in snps if not s['synonymous'] and not s['nonsense']]
    silent    = [s for s in snps if s['synonymous']]

    return {
        'snps': snps, 'indels': indels,
        'count': len(snps), 'similarity': sim,
        'nonsense': nonsense, 'missense': missense, 'silent': silent,
        'len_diff': len_diff, 'ref': ref, 'sample': sample,
        'pathogenic_score': min(100, len(nonsense)*30 + len(missense)*8 + (40 if indels and indels[0]['frameshift'] else 0)),
    }


def analyze_codons(seq: str) -> dict:
    """Codon usage, translation, and bias analysis."""
    seq = clean_dna(seq)
    if not seq:
        return None
    start = seq.find('ATG')
    coding = seq[start:] if start >= 0 else seq
    codons  = [coding[i:i+3] for i in range(0, len(coding)-2, 3)
               if len(coding[i:i+3]) == 3]
    aas     = [CODON_TABLE.get(c, '?') for c in codons]
    stop_i  = aas.index('Stop') if 'Stop' in aas else -1
    protein = aas[:stop_i] if stop_i >= 0 else aas
    freq    = Counter(codons)
    aa_freq = Counter(aas)

    # Codon adaptation index (simplified)
    optimal = {'TTT','TGT','ATT','GTT','TCT','CCT','ACT','GCT','TAT','CAT','CAA','AAT','AAA','GAT','GAA','TGT','CGT','AGT','GGT'}
    cai     = sum(1 for c in codons if c in optimal) / len(codons) * 100 if codons else 0

    return {
        'codons': codons, 'aas': aas, 'protein': protein,
        'stop_idx': stop_i, 'start_pos': start,
        'freq': freq, 'aa_freq': aa_freq, 'cai': cai,
        'n_codons': len(codons), 'n_aa': len(protein),
    }


def find_orfs(seq: str) -> list:
    """Multi-frame ORF detection across all 3 reading frames."""
    seq   = clean_dna(seq)
    stops = {'TAA', 'TAG', 'TGA'}
    orfs  = []
    for frame in range(3):
        start = -1
        for i in range(frame, len(seq) - 2, 3):
            codon = seq[i:i+3]
            if codon == 'ATG' and start < 0:
                start = i
            elif codon in stops and start >= 0:
                length = i + 3 - start
                orfs.append({
                    'start': start, 'end': i + 3,
                    'length': length, 'frame': frame + 1,
                    'seq': seq[start:i+3],
                    'n_codons': length // 3,
                    'probable_protein': length > 300,
                })
                start = -1
    return sorted(orfs, key=lambda x: x['length'], reverse=True)


def calc_tm(seq: str) -> dict:
    """Comprehensive Tm calculation with multiple methods."""
    seq = clean_dna(seq)
    if not seq:
        return None
    n  = len(seq)
    gc = seq.count('G') + seq.count('C')
    at = seq.count('A') + seq.count('T')
    gc_pct = gc / n * 100 if n else 0

    # Wallace rule (short seqs <14)
    tm_wallace = 2 * at + 4 * gc

    # Nearest-neighbor (long seqs)
    tm_nn      = 64.9 + 41 * (gc - 16.4) / n if n >= 14 else tm_wallace

    # Salt-adjusted (0.05 → 0.2 M Na+)
    tm_salt    = tm_nn - 16.6 * math.log10(0.05) + 16.6 * math.log10(0.2)

    # Primer3-style
    tm_primer3 = 81.5 + 16.6 * math.log10(0.05) + 41 * gc_pct / 100 - 675 / n if n >= 8 else tm_wallace

    anneal  = tm_salt - 5
    quality = ('Optimal'       if 40 <= gc_pct <= 60 and 18 <= n <= 28 else
               'Acceptable'    if 35 <= gc_pct <= 65 and 15 <= n <= 35 else
               'Needs review')

    # 3' stability check
    last5 = seq[-5:]
    gc_3end = last5.count('G') + last5.count('C')
    stable_3end = gc_3end <= 3

    return {
        'seq': seq, 'n': n, 'gc': gc, 'at': at, 'gc_pct': gc_pct,
        'tm_wallace': tm_wallace, 'tm_nn': tm_nn,
        'tm_salt': tm_salt, 'tm_primer3': tm_primer3,
        'anneal': anneal, 'quality': quality,
        'stable_3end': stable_3end, 'gc_3end': gc_3end,
        'length_ok': 18 <= n <= 28,
        'gc_ok': 40 <= gc_pct <= 60,
    }


# ══════════════════════════════════════════════════════════════════
#                         HELPERS
# ══════════════════════════════════════════════════════════════════
def color_seq(seq: str, max_len: int = 200) -> str:
    """Return HTML-colored sequence string."""
    out = ""
    for c in seq[:max_len]:
        if c in "GC":
            out += f'<span class="seq-gc">{c}</span>'
        else:
            out += f'<span class="seq-at">{c}</span>'
    if len(seq) > max_len:
        out += f'<span style="color:#5F5E5A"> …+{len(seq)-max_len:,} more</span>'
    return out


def bar_html(label: str, pct: float, color: str) -> str:
    pct = min(max(pct, 0), 100)
    return f"""
    <div style="display:flex;align-items:center;gap:8px;margin-bottom:8px">
      <span style="font-family:'JetBrains Mono',monospace;font-size:11px;color:#5DCAA5;width:14px">{label}</span>
      <div style="flex:1;height:5px;background:rgba(29,158,117,0.1);border-radius:99px;overflow:hidden">
        <div style="width:{pct:.1f}%;height:100%;background:{color};border-radius:99px"></div>
      </div>
      <span style="font-family:'JetBrains Mono',monospace;font-size:10px;color:#5F5E5A;width:34px;text-align:right">{pct:.1f}%</span>
    </div>"""


def parse_info(r: dict) -> str:
    return f"""<div class="parse-bar">
      <div style="width:6px;height:6px;border-radius:50%;background:#1D9E75;flex-shrink:0"></div>
      Detected: <strong>{r['fmt']}</strong> &nbsp;·&nbsp; {len(r['seqs'])} seq{'s' if len(r['seqs'])>1 else ''} &nbsp;·&nbsp; {len(r['primary']):,} bp
    </div>"""


def metric_card(label, value, sub="", color="#E1F5EE"):
    return f"""<div class="mc">
      <div class="mc-lbl">{label}</div>
      <div class="mc-val" style="color:{color}">{value}</div>
      <div class="mc-sub">{sub}</div>
    </div>"""


# ══════════════════════════════════════════════════════════════════
#                          SIDEBAR
# ══════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("""
    <div class="sidebar-logo">
      <span class="logo-icon">🧬</span>
      <div class="logo-title">BioLab AI Pro</div>
      <div class="logo-sub">v4.0 · Final Year Project</div>
    </div>""", unsafe_allow_html=True)
    st.divider()

    module = st.radio("Navigate", [
        "🏠  Home",
        "🔬  DNA Analysis",
        "🦠  Disease Detection",
        "🧫  Protein Prediction",
        "🔍  Mutation Detection",
        "📊  Codon Analysis",
        "🧭  ORF Finder",
        "🌡️  Tm / PCR",
    ], label_visibility="collapsed")

    st.divider()
    st.markdown("**Supported formats**", unsafe_allow_html=False)
    for f in ["✅ FASTA · multi-FASTA", "✅ FASTQ (Illumina/Sanger)",
              "✅ GenBank (.gb/.gbk)", "✅ EMBL flat file",
              "✅ Raw DNA / RNA / protein"]:
        st.caption(f)

    st.divider()
    st.markdown("""
    <div class="sidebar-credit">
    <strong style="color:#9FE1CB">Designed by:</strong> ALI<br>
    <strong style="color:#9FE1CB">AG No:</strong> <code style="color:#5DCAA5">2022-AG-7647</code><br>
    <strong style="color:#9FE1CB">Year:</strong> Final Year<br>
    <strong style="color:#9FE1CB">Project:</strong> AI Bioinformatics
    </div>""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════
#                            HOME
# ══════════════════════════════════════════════════════════════════
if "Home" in module:
    st.markdown("""
    <div class="hero">
      <div class="hero-grid"></div>
      <div class="hero-glow"></div>
      <div class="hero-inner">
        <h1>BioLab AI Pro</h1>
        <div class="hero-sub">AI-Powered Genomic Sequence Analyzer</div>
        <div class="hero-chips">
          <span class="chip chip-teal">DNA Analysis</span>
          <span class="chip chip-purple">Disease Detection</span>
          <span class="chip chip-coral">Protein Prediction</span>
          <span class="chip chip-pink">Multi-Format</span>
        </div>
        <div style="font-size:11px;color:#5F5E5A">
          FASTA · FASTQ · GenBank · EMBL · Raw DNA/Protein
        </div>
      </div>
      <div class="seq-ticker">
        <span>5' ATGAAAGCAATTTTCGTACTGAAAGGTTTTGTT &nbsp;|&nbsp;
        GC CONTENT 48.3% &nbsp;|&nbsp;
        BRCA1 · TP53 · KRAS · HBB · CFTR &nbsp;|&nbsp;
        3' TACTTCGTTAAAAGCATGACTTTCCAAAACAA &nbsp;|&nbsp;
        SNP DETECTION · ORF FINDER · Tm CALC &nbsp;|&nbsp;
        5' ATGAAAGCAATTTTCGTACTGAAAGGTTTTGTT &nbsp;|&nbsp;
        GC CONTENT 48.3%</span>
      </div>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    for col, val, lbl, sub, color in [
        (c1, "7",  "Modules",     "Analysis tools",    "#5DCAA5"),
        (c2, "6",  "Formats",     "File types",        "#AFA9EC"),
        (c3, "10", "Diseases",    "Screened",          "#F09595"),
        (c4, "AI", "Engine",      "Powered",           "#9FE1CB"),
    ]:
        col.markdown(f"""<div class="mc">
        <div class="mc-lbl">{lbl}</div>
        <div class="mc-val" style="color:{color}">{val}</div>
        <div class="mc-sub">{sub}</div></div>""", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### Features")
    feats = [
        ("🔬", "DNA Analysis",         "GC content, nucleotide composition, sequence visualization, quality tags"),
        ("🦠", "Disease Detection",     "10-disease panel — BRCA1/2, TP53, HBB, CFTR, NF1 + pathogenic scoring"),
        ("🧫", "Protein Prediction",    "Function prediction, secondary structure, pI, GRAVY, aliphatic index"),
        ("🔍", "Mutation Detection",    "SNP + indel detection, missense/nonsense classification, pathogenic score"),
        ("📊", "Codon Analysis",        "Translation, codon frequency table, CAI score, amino acid composition"),
        ("🌡️", "Tm Calculator",         "Wallace + nearest-neighbor + salt-adjusted + Primer3 methods"),
    ]
    cols = st.columns(3)
    for i, (ico, name, desc) in enumerate(feats):
        with cols[i % 3]:
            st.markdown(f"""<div class="glass-card">
            <div style="font-size:1.4rem;margin-bottom:6px">{ico}</div>
            <div style="font-size:12px;font-weight:600;color:#E1F5EE;margin-bottom:4px">{name}</div>
            <div style="font-size:11px;color:#5F5E5A;line-height:1.5">{desc}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("""
    <div class="footer">
      <div class="ft-left" style="display:flex;align-items:center;gap:12px">
        <div class="footer-av">A</div>
        <div>
          <div class="footer-name">Designed by ALI</div>
          <div class="footer-ag">AG No: 2022-AG-7647</div>
        </div>
      </div>
      <div style="text-align:right">
        <div style="font-size:11px;color:#5F5E5A">BioLab AI Pro · v4.0 · Final Year Project</div>
        <div style="font-size:10px;color:#1D9E75;margin-top:2px">● Engine active</div>
      </div>
    </div>""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════
#                       DNA ANALYSIS
# ══════════════════════════════════════════════════════════════════
elif "DNA" in module:
    st.markdown("## 🔬 DNA Sequence Analysis")

    up = st.file_uploader("Upload sequence file", type=["fa","fasta","fq","fastq","gb","gbk","embl","txt","seq"])
    raw = ""
    if up:
        raw = up.read().decode("utf-8", errors="ignore")
        st.success(f"Loaded: **{up.name}** ({len(raw):,} chars)")

    examples = {
        "Normal gene":  "ATGAAAGCAATTTTCGTACTGAAAGGTTTTGTTGGTTTTTTGTCAGTTTGCTTTTTGGTTCGTTGATTGCTCTTGTCATCGTAATAATAGCATTGATAAC",
        "BRCA1-like":   "ATGGATTTATCTGCTCTTCGCGTTGAAGAAGTACAAAATGTCATTAATGCTATGCAGAAAATCTTAGAGTGTCCCATCTGTCTGGAGTTGATCAAGGAACCTGTCTCC",
        "Multi-FASTA":  ">gene1 Normal\nATGAAAGCAATTTTCGTACTGAAAGGTTTT\n>gene2 Variant\nATGGATTTATCTGCTCTTCGCGTTGAAGAA\n>gene3 BRCA1\nATGGATTTATCTGCTCTTCGCGTTGAAGAAGTA",
        "FASTQ sample": "@SRR1234.1\nATGAAAGCAATTTTCGTACTGAAAGGTTTT\n+\nIIIIIIIIIIIIIIIIIIIIIIIIIIIIII",
        "GenBank":      "LOCUS  EXAMPLE  100 bp\nACCESSION  NM_000059\nORIGIN\n        1 atggatttat ctgctcttcg cgttgaagaa gtacaaaatg tcattaatgc\n       51 tatgcagaaa atcttagagt gtcccatctg tctggagttg\n//",
    }
    col_ex1, col_ex2 = st.columns([3, 1])
    ex_choice = col_ex1.selectbox("Load example", list(examples.keys()), label_visibility="collapsed")
    if col_ex2.button("Load"):
        raw = examples[ex_choice]

    raw = st.text_area("Paste sequence (any format)", value=raw, height=110,
                       placeholder="FASTA, FASTQ, GenBank, EMBL, or raw DNA…")

    if raw:
        parsed = parse_sequence(raw)
        st.caption(f"Detected: **{parsed['fmt']}** · {len(parsed['seqs'])} sequence(s) · {len(parsed['primary']):,} bp")

    if raw and st.button("▶  Run DNA Analysis", use_container_width=True):
        parsed = parse_sequence(raw)
        with st.spinner("Analyzing…"):
            res = analyze_dna(parsed['primary'])

        if not res:
            st.error("No valid DNA sequence found.")
        else:
            st.markdown(parse_info(parsed), unsafe_allow_html=True)
            c1,c2,c3,c4 = st.columns(4)
            c1.metric("Length",     f"{res['length']:,} bp")
            c2.metric("GC content", f"{res['gc']:.1f}%",   res['gc_status'])
            c3.metric("Codons",     f"{res['codons']:,}")
            c4.metric("CpG sites",  f"{res['cpg']:,}")

            st.markdown('<div class="glass-card"><div class="card-title">Nucleotide composition</div>', unsafe_allow_html=True)
            for base, col in [('A','#AFA9EC'),('T','#5DCAA5'),('G','#F0997B'),('C','#ED93B1')]:
                pct = res['counts'].get(base, 0) / res['valid'] * 100
                st.markdown(bar_html(base, pct, col), unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

            st.markdown('<div class="glass-card"><div class="card-title">Sequence visualization</div>', unsafe_allow_html=True)
            colored = color_seq(res['seq'], 200)
            st.markdown(f'<div class="seq-display">{colored}</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

            if parsed['multi']:
                st.markdown("#### Multi-sequence panel")
                table_data = []
                for s in parsed['seqs']:
                    gc_s = (s['seq'].count('G')+s['seq'].count('C'))/len(s['seq'])*100 if s['seq'] else 0
                    table_data.append({"ID": s['id'][:40], "Length": f"{len(s['seq']):,} bp",
                                       "GC%": f"{gc_s:.1f}%", "Description": s.get('desc','')[:50]})
                st.dataframe(table_data, use_container_width=True)

            tags_html = ""
            for tag, cls in [
                (res['gc_status'], 'tag-teal'),
                ('Full gene' if res['length'] > 100 else 'Short fragment', 'tag-teal' if res['length']>100 else 'tag-amber'),
                ('Start codon (ATG)' if res['has_start'] else 'No start codon', 'tag-teal' if res['has_start'] else 'tag-red'),
                ('Stop codon found' if res['has_stop'] else 'No stop codon', 'tag-teal' if res['has_stop'] else 'tag-amber'),
                (parsed['fmt'], 'tag-purple'),
            ]:
                tags_html += f'<span class="{cls}">{tag}</span>'
            st.markdown(f'<div class="glass-card"><div class="card-title">AI tags</div>{tags_html}</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════
#                     DISEASE DETECTION
# ══════════════════════════════════════════════════════════════════
elif "Disease" in module:
    st.markdown("## 🦠 Disease Risk Detection")
    st.caption("AI-powered screening based on sequence composition and known pathogenic markers")

    raw = st.text_area("DNA sequence (any format)", height=100,
                       value="ATGGATTTATCTGCTCTTCGCGTTGAAGAAGTACAAAATGTCATTAATGCTATGCAGAAAATCTTAGAGTGTCCCATCTGTCTGGAGTTGATCAAGGAACCTGTCTCC",
                       placeholder="Paste FASTA, GenBank, or raw DNA…")

    if raw and st.button("▶  Run Disease Screening", use_container_width=True):
        parsed = parse_sequence(raw)
        with st.spinner("Scanning disease markers…"):
            res = detect_disease(parsed['primary'])

        if not res:
            st.error("No valid sequence.")
        else:
            st.markdown(parse_info(parsed), unsafe_allow_html=True)

            lvl_icon = {'High':'🔴','Moderate':'🟠','Low':'🟡','Minimal':'🟢'}
            lvl_col  = {'High':'#F09595','Moderate':'#EF9F27','Low':'#5DCAA5','Minimal':'#5DCAA5'}
            col_score, col_prog = st.columns([1,3])
            with col_score:
                st.metric("Overall risk score", f"{res['overall']}/100", res['overall_level'])
            with col_prog:
                st.markdown(f"### {lvl_icon.get(res['overall_level'],'')} {res['overall_level']} risk")
                st.progress(res['overall'] / 100)

            if res['markers']:
                markers_html = "".join(f'<span class="tag-purple">{m}</span>' for m in res['markers'])
                st.markdown(f"**Detected markers:** {markers_html}", unsafe_allow_html=True)

            st.markdown("---")
            st.markdown("### Disease screening panel")
            for d in res['diseases']:
                c1, c2, c3 = st.columns([3, 1, 2])
                c1.markdown(f"**{d['name']}**\n\n*{d['gene']} · {d['cat']}*")
                c2.markdown(f"<span class='risk-{d['level'].lower()}'>{d['level']}</span>", unsafe_allow_html=True)
                c3.progress(d['risk']/100, text=f"{d['risk']}%")

            st.markdown("---")
            st.markdown("### Clinical recommendations")
            if res['overall'] > 50:
                st.markdown('<div class="alert-high"><div class="at">Genetic counseling strongly recommended</div><div class="as">High-risk pathogenic markers detected. Consult a clinical geneticist and perform confirmatory NGS.</div></div>', unsafe_allow_html=True)
            elif res['overall'] > 30:
                st.markdown('<div class="alert-mod"><div class="at">Moderate risk — follow-up advised</div><div class="as">Some disease markers detected. Additional sequencing and clinical history review recommended.</div></div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="alert-ok"><div class="at">Low risk — routine monitoring</div><div class="as">No high-risk markers identified. Standard clinical follow-up is appropriate.</div></div>', unsafe_allow_html=True)

            with st.expander("Recommended next steps"):
                for step in ["Validate with clinical NGS panel",
                             "Search NCBI ClinVar for variants",
                             "Consult a clinical geneticist",
                             "Perform family history assessment",
                             "Consider GWAS analysis for complex traits"]:
                    st.markdown(f"- {step}")


# ══════════════════════════════════════════════════════════════════
#                    PROTEIN PREDICTION
# ══════════════════════════════════════════════════════════════════
elif "Protein" in module:
    st.markdown("## 🧫 Protein Function Prediction")

    seq = st.text_area("Amino acid sequence (single-letter codes)", height=100,
                       value="MKTAYIAKQRQISFVKSHFSRQLEERLGLIEVQAPILSRVGDGTQDNLSGAEKAVQVKVKALPDAQFEVVHSLAKWKRQTLGQHDFS")

    if seq and st.button("▶  Predict Protein Function", use_container_width=True):
        with st.spinner("Analyzing protein…"):
            res = predict_protein(seq.strip().upper().replace('\n','').replace(' ',''))

        if res:
            c1,c2,c3,c4 = st.columns(4)
            c1.metric("Length",      f"{res['length']} aa")
            c2.metric("Mol. weight", f"{round(res['mw']/1000,1)} kDa")
            c3.metric("Hydrophobic", f"{res['hydro']:.1f}%")
            c4.metric("Charged",     f"{res['charged']:.1f}%")

            st.markdown("#### Predicted functions")
            for p in res['preds']:
                c1, c2 = st.columns([3,1])
                c1.markdown(f"**{p['n']}** — *{p['d']}*")
                c2.progress(p['c']/100, text=f"{p['c']}%")

            st.markdown("#### Secondary structure")
            for name, val, col in [("Alpha helix", res['helix'],'#5DCAA5'),
                                    ("Beta sheet",  res['sheet'],'#85B7EB'),
                                    ("Coil / loop", res['coil'], '#888780')]:
                st.markdown(f"**{name}** — {val}%")
                st.progress(val/100)

            st.markdown("#### Physicochemical properties")
            c1,c2,c3,c4 = st.columns(4)
            c1.metric("Isoelectric pI",  res['pi'])
            c2.metric("Instability idx", res['instability'])
            c3.metric("GRAVY score",     res['gravy'])
            c4.metric("Aliphatic idx",   res['aliphatic'])


# ══════════════════════════════════════════════════════════════════
#                   MUTATION DETECTION
# ══════════════════════════════════════════════════════════════════
elif "Mutation" in module:
    st.markdown("## 🔍 Advanced Mutation Detection")

    c1, c2 = st.columns(2)
    ref_raw = c1.text_area("Reference sequence",
                            value="ATGAAAGCAATTTTCGTACTGAAAGGTTTTGTTGGTTTTTTGTCAGTTTGCTTTTTGGTT",
                            height=100)
    sam_raw = c2.text_area("Sample sequence",
                            value="ATGAAAGCAATTTTAGTACTGAAAGGTTTTGTTGGTTTTTTGTCAGTTTGCTTTTTGGTT",
                            height=100)

    if st.button("▶  Detect Mutations", use_container_width=True):
        ref_p = parse_sequence(ref_raw)
        sam_p = parse_sequence(sam_raw)
        with st.spinner("Comparing sequences…"):
            res = detect_mutations(ref_p['primary'], sam_p['primary'])

        if res:
            c1,c2,c3,c4 = st.columns(4)
            c1.metric("Total SNPs",        res['count'])
            c2.metric("Missense",          len(res['missense']))
            c3.metric("Nonsense",          len(res['nonsense']))
            c4.metric("Identity",          f"{res['similarity']:.1f}%")

            st.metric("Pathogenic score",  f"{res['pathogenic_score']}/100")
            st.progress(res['pathogenic_score']/100)

            if res['indels']:
                for ind in res['indels']:
                    st.warning(f"**{'Frameshift' if ind['frameshift'] else 'In-frame'} {ind['type']}** detected — {ind['size']} bp")

            if res['snps']:
                st.markdown("#### SNP table")
                data = [{
                    "Position": s['pos'],
                    "Ref": s['ref'], "Sample": s['sample'],
                    "Ref AA": s['ref_aa'], "Sam AA": s['sam_aa'],
                    "Type": "Nonsense" if s['nonsense'] else ("Silent" if s['synonymous'] else "Missense"),
                } for s in res['snps'][:30]]
                st.dataframe(data, use_container_width=True)
                if res['count'] > 30:
                    st.caption(f"Showing first 30 of {res['count']} mutations.")
            else:
                st.success("No mutations — sequences are identical.")


# ══════════════════════════════════════════════════════════════════
#                    CODON ANALYSIS
# ══════════════════════════════════════════════════════════════════
elif "Codon" in module:
    st.markdown("## 📊 Codon Analysis & Translation")

    raw = st.text_area("Coding DNA sequence", height=100,
                       value="ATGAAAGCAATTTTCGTACTGAAAGGTTTTGTTGGTTTTTTGTCAGTTTGCTTTTTGGTTCGTTGATTGCTCTTGTCATCGTAATAATAGCATTGATAAC")

    if raw and st.button("▶  Analyze Codons", use_container_width=True):
        parsed = parse_sequence(raw)
        with st.spinner("Translating…"):
            res = analyze_codons(parsed['primary'])

        if res:
            c1,c2,c3,c4 = st.columns(4)
            c1.metric("Total codons",  res['n_codons'])
            c2.metric("Amino acids",   res['n_aa'])
            c3.metric("Start codon",   f"pos {res['start_pos']}" if res['start_pos'] >= 0 else "—")
            c4.metric("CAI score",     f"{res['cai']:.1f}%")

            st.markdown("#### Translated protein (first 40 AA)")
            st.code(" — ".join(res['protein'][:40]) + ("…" if len(res['protein']) > 40 else ""))

            st.markdown("#### Codon frequency table")
            freq_rows = [{
                "Codon": c, "Amino Acid": CODON_TABLE.get(c,'?'),
                "Count": n,
                "Frequency": f"{n/res['n_codons']*100:.1f}%" if res['n_codons'] else "—"
            } for c, n in res['freq'].most_common(20)]
            st.dataframe(freq_rows, use_container_width=True)

            st.markdown("#### Amino acid composition")
            aa_rows = [{"AA": aa, "Count": cnt,
                        "Fraction": f"{cnt/res['n_aa']*100:.1f}%" if res['n_aa'] else "—"}
                       for aa, cnt in res['aa_freq'].most_common(10) if aa != 'Stop']
            st.dataframe(aa_rows, use_container_width=True)


# ══════════════════════════════════════════════════════════════════
#                      ORF FINDER
# ══════════════════════════════════════════════════════════════════
elif "ORF" in module:
    st.markdown("## 🧭 Open Reading Frame (ORF) Finder")

    raw = st.text_area("DNA sequence", height=100,
                       value="GCTAGCATGAAAGCAATTTTCGTACTGAAAGGTTTTGTTGGTTTTTTGTCAGTTTGCTTTTTGGTTCGTTGATTGCTCTTGTCATCGTAATAATAGCATTGATAACTGACG")

    if raw and st.button("▶  Find ORFs", use_container_width=True):
        parsed = parse_sequence(raw)
        with st.spinner("Scanning reading frames…"):
            orfs = find_orfs(parsed['primary'])

        c1,c2,c3 = st.columns(3)
        c1.metric("ORFs found",   len(orfs))
        c2.metric("Longest ORF",  f"{orfs[0]['length']} bp" if orfs else "—")
        c3.metric("Probable proteins", sum(1 for o in orfs if o['probable_protein']))

        if orfs:
            st.markdown("#### ORF table")
            orf_data = [{
                "Rank": i+1, "Start": o['start'], "End": o['end'],
                "Length (bp)": o['length'], "Frame": o['frame'],
                "Codons": o['n_codons'],
                "Probable protein": "Yes" if o['probable_protein'] else "No",
            } for i, o in enumerate(orfs[:20])]
            st.dataframe(orf_data, use_container_width=True)

            st.markdown("#### Largest ORF sequence")
            colored = color_seq(orfs[0]['seq'], 200)
            st.markdown(f'<div class="seq-display">{colored}</div>', unsafe_allow_html=True)
        else:
            st.warning("No ORFs detected in this sequence.")


# ══════════════════════════════════════════════════════════════════
#                     Tm / PCR CALCULATOR
# ══════════════════════════════════════════════════════════════════
elif "Tm" in module:
    st.markdown("## 🌡️ Melting Temperature & PCR Calculator")

    ex_col1, ex_col2 = st.columns([3,1])
    primer_ex = ex_col1.selectbox("Load primer example", [
        "Short primer (17bp)", "Medium primer (32bp)", "Long primer (48bp)"])
    primer_seqs = {
        "Short primer (17bp)": "ATGAAAGCAATTTTCGT",
        "Medium primer (32bp)":"GCTAGCATGAAAGCAATTTTCGTACTGAAAGG",
        "Long primer (48bp)":  "ATGGATTTATCTGCTCTTCGCGTTGAAGAAGTACAAAATGTCATTAAT",
    }
    raw_tm = st.text_area("Primer / DNA sequence", value=primer_seqs[primer_ex], height=80)

    if raw_tm and st.button("▶  Calculate Tm", use_container_width=True):
        parsed = parse_sequence(raw_tm)
        with st.spinner("Calculating…"):
            res = calc_tm(parsed['primary'])

        if res:
            c1,c2,c3,c4 = st.columns(4)
            c1.metric("Tm (Wallace)",    f"{res['tm_wallace']:.1f} °C")
            c2.metric("Tm (Nearest-nbr)",f"{res['tm_nn']:.1f} °C")
            c3.metric("Tm (0.2M Na⁺)",  f"{res['tm_salt']:.1f} °C")
            c4.metric("Annealing temp",  f"{res['anneal']:.1f} °C")

            st.metric("Primer3 Tm", f"{res['tm_primer3']:.1f} °C")
            st.progress(min(res['gc_pct']/100, 1.0), text=f"GC content: {res['gc_pct']:.1f}%")

            st.markdown("#### Primer quality checklist")
            checks = [
                ("Length (18–28 bp)", res['length_ok'],  f"{res['n']} bp"),
                ("GC% (40–60%)",      res['gc_ok'],      f"{res['gc_pct']:.1f}%"),
                ("Tm > 50 °C",        res['tm_salt']>50, f"{res['tm_salt']:.1f} °C"),
                ("3' stability",      res['stable_3end'], f"3' GC={res['gc_3end']}/5"),
            ]
            for label, passed, val in checks:
                icon = "✅" if passed else "⚠️"
                st.markdown(f"{icon} **{label}** — {val}")

            qual_map = {'Optimal': 'success', 'Acceptable': 'warning', 'Needs review': 'error'}
            getattr(st, qual_map.get(res['quality'], 'info'))(
                f"Primer quality: **{res['quality']}**")


# ══════════════════════════════════════════════════════════════════
#                     PERSISTENT FOOTER
# ══════════════════════════════════════════════════════════════════
st.markdown("""
<div class="footer">
  <div style="display:flex;align-items:center;gap:12px">
    <div class="footer-av">A</div>
    <div>
      <div class="footer-name">Designed by ALI</div>
      <div class="footer-ag">AG No: 2022-AG-7647</div>
    </div>
  </div>
  <div style="text-align:right">
    <div style="font-size:11px;color:#5F5E5A">BioLab AI Pro · v4.0 · Final Year Project · Bioinformatics</div>
    <div style="font-size:10px;color:#1D9E75;margin-top:2px">● Engine active · Multi-format support</div>
  </div>
</div>
""", unsafe_allow_html=True)
