import streamlit as st
import pandas as pd
import hashlib
from pathlib import Path

st.set_page_config(
    page_title="Consulta Fácil | Horários Escolares",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="collapsed"
)

DIAS = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado"]
horarios = Path(__file__).parent / "data" / "horarios.csv"

# Paleta consistente: a mesma disciplina recebe sempre a mesma cor.
PALETA = [
    "#DCEBFA", "#FCE2D5", "#E2F0D9", "#FFF2CC", "#E4DFEC",
    "#DDEBF7", "#F4CCCC", "#D9EAD3", "#FCE5CD", "#D9D2E9",
    "#CFE2F3", "#FADBD8", "#D5E8D4", "#F9E79F", "#E8DAEF"
]

def carregar_dados():
    if horarios.exists():
        df = pd.read_csv(horarios, dtype=str).fillna("")
        return df
    return pd.DataFrame(columns=[
        "Turma", "Dia", "Periodo", "Inicio", "Fim", "Disciplina", "Professor"
    ])

def cor_disciplina(nome):
    if not nome:
        return "#F3F4F6"
    indice = int(hashlib.md5(nome.strip().lower().encode("utf-8")).hexdigest(), 16) % len(PALETA)
    return PALETA[indice]

def formatar_hora(valor):
    valor = str(valor).strip()
    return valor.replace(":00", "h").replace(":30", "h30")

def validar_dados(df):
    obrigatorias = ["Turma", "Dia", "Periodo", "Inicio", "Fim", "Disciplina", "Professor"]
    faltantes = [c for c in obrigatorias if c not in df.columns]
    if faltantes:
        return False, "Colunas ausentes no arquivo: " + ", ".join(faltantes)
    return True, ""

def render_celula(disciplina, professor):
    if not disciplina:
        return '<div class="celula vazia"><span class="vazio">—</span></div>'
    cor = cor_disciplina(disciplina)
    disciplina_html = str(disciplina).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    professor_html = str(professor or "Professor não informado").replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    return f"""
    <div class="celula" style="background:{cor};">
      <div class="disciplina">{disciplina_html}</div>
      <div class="professor">{professor_html}</div>
    </div>
    """

st.markdown("""
<style>
    .block-container {padding-top: 1.5rem; padding-bottom: 2rem; max-width: 1500px;}
    .cabecalho {margin-bottom: 1rem;}
    .subtitulo {color: #64748b; margin-top: -12px;}
    .grade-wrap {overflow-x: auto; width: 100%; padding-bottom: 8px;}
    table.grade {border-collapse: separate; border-spacing: 4px; width: 100%; min-width: 920px; table-layout: fixed;}
    table.grade th {background: #1e293b; color: white; padding: 12px 6px; border-radius: 8px; text-align: center; font-size: 14px;}
    table.grade th.lateral {background: #334155; width: 68px;}
    table.grade td {padding: 0; vertical-align: middle; text-align: center;}
    .numero {background:#e2e8f0; color:#0f172a; font-weight:800; border-radius:8px; padding:12px 4px; min-height:65px; display:flex; align-items:center; justify-content:center;}
    .horario {background:#f1f5f9; color:#334155; border:1px solid #e2e8f0; border-radius:8px; padding:8px 3px; min-height:65px; display:flex; align-items:center; justify-content:center; font-size:12px; font-weight:700;}
    .celula {border-radius:8px; min-height:65px; height:100%; padding:9px 5px; display:flex; flex-direction:column; align-items:center; justify-content:center; gap:5px; border:1px solid rgba(15,23,42,.08); box-sizing:border-box;}
    .celula.vazia {background:#f8fafc; border:1px dashed #cbd5e1;}
    .disciplina {font-weight:800; color:#172033; font-size:13px; line-height:1.2; overflow-wrap:anywhere;}
    .professor {font-size:11px; color:#334155; line-height:1.2; overflow-wrap:anywhere;}
    .vazio {color:#94a3b8; font-size:18px;}
    .legenda {display:flex; flex-wrap:wrap; gap:8px; margin-top:16px;}
    .item-legenda {display:flex; align-items:center; gap:6px; background:#f8fafc; border:1px solid #e2e8f0; border-radius:20px; padding:5px 10px; font-size:12px; color:#334155;}
    .amostra {width:12px; height:12px; border-radius:4px; border:1px solid rgba(0,0,0,.08);}
    @media (max-width: 700px) {
      .block-container {padding-left: .6rem; padding-right: .6rem;}
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="cabecalho"><h1>📚 Consulta Fácil</h1><p class="subtitulo">Horários escolares por turma</p></div>', unsafe_allow_html=True)

df = carregar_dados()
valido, erro = validar_dados(df)

if not valido:
    st.error(erro)
    st.stop()

if df.empty:
    st.warning("Ainda não há horários cadastrados. Adicione os dados ao arquivo dados/horarios.csv.")
    st.info("O projeto já vem com um arquivo de exemplo. Se ele estiver vazio, confira se o arquivo CSV foi incluído na pasta dados.")
    st.stop()

df["Periodo"] = pd.to_numeric(df["Periodo"], errors="coerce")
df = df.dropna(subset=["Periodo"])
df["Periodo"] = df["Periodo"].astype(int)

turmas = sorted(df["Turma"].dropna().astype(str).unique().tolist())
if not turmas:
    st.warning("Nenhuma turma encontrada no arquivo de horários.")
    st.stop()

col_selecao, col_info = st.columns([1, 2])
with col_selecao:
    turma_selecionada = st.selectbox("Selecione sua turma", turmas)
with col_info:
    st.markdown("<div style='padding-top:30px;color:#64748b'>Escolha uma turma para visualizar os horários de segunda a sábado.</div>", unsafe_allow_html=True)

dados_turma = df[df["Turma"] == turma_selecionada].copy()

# Dez períodos fixos. Os intervalos podem ser ajustados depois no CSV.
periodos = list(range(1, 11))
horarios_por_periodo = {}
for p in periodos:
    linhas = dados_turma[dados_turma["Periodo"] == p]
    if not linhas.empty:
        horarios_por_periodo[p] = (linhas.iloc[0]["Inicio"], linhas.iloc[0]["Fim"])
    else:
        horarios_por_periodo[p] = ("", "")

cabecalho = """
<div class="grade-wrap">
<table class="grade">
<thead><tr>
<th class="lateral">Aula</th>
<th class="lateral">Horário</th>
""" + "".join(f"<th>{dia}</th>" for dia in DIAS) + """
</tr></thead><tbody>
"""

linhas_html = []
for periodo in periodos:
    inicio, fim = horarios_por_periodo[periodo]
    if inicio and fim:
        intervalo = f"{formatar_hora(inicio)} – {formatar_hora(fim)}"
    else:
        intervalo = "Definir"
    linha = f'<tr><td><div class="numero">{periodo}</div></td><td><div class="horario">{intervalo}</div></td>'
    for dia in DIAS:
        registro = dados_turma[
            (dados_turma["Periodo"] == periodo) &
            (dados_turma["Dia"].str.strip().str.lower() == dia.lower())
        ]
        if registro.empty:
            conteudo = render_celula("", "")
        else:
            item = registro.iloc[0]
            conteudo = render_celula(item["Disciplina"], item["Professor"])
        linha += f"<td>{conteudo}</td>"
    linha += "</tr>"
    linhas_html.append(linha)

st.markdown(cabecalho + "".join(linhas_html) + "</tbody></table></div>", unsafe_allow_html=True)

disciplinas = sorted([d for d in dados_turma["Disciplina"].dropna().astype(str).unique() if d.strip()])
if disciplinas:
    st.markdown("**Legenda das disciplinas**")
    legenda = '<div class="legenda">'
    for disciplina in disciplinas:
        cor = cor_disciplina(disciplina)
        nome = disciplina.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        legenda += f'<span class="item-legenda"><span class="amostra" style="background:{cor}"></span>{nome}</span>'
    legenda += "</div>"
    st.markdown(legenda, unsafe_allow_html=True)
    
with st.expander("Sobre os horários"):
    st.write("A grade apresenta dez períodos. Os intervalos estão no arquivo CSV e podem ser ajustados posteriormente, inclusive para considerar os intervalos da escola.")
    st.caption("As células sem disciplina cadastrada aparecem vazias. As cores são atribuídas automaticamente e permanecem iguais para a mesma disciplina.")
