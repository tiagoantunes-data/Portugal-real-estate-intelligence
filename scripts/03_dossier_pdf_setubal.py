"""
LUXAR — Dossier de Mercado PDF v1 | Península de Setúbal
Gera PDF profissional pronto para portfólio, LinkedIn e GitHub.

Uso:
    python scripts/03_dossier_pdf_setubal.py
"""

from datetime import date
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm, mm
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    Image,
    NextPageTemplate,
    PageBreak,
    PageTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)

# ─── Configuração ─────────────────────────────────────────────────────────────

BASE_DIR = Path(__file__).parent.parent
GRAFICOS_DIR = BASE_DIR / "outputs/graficos_setubal"
OUTPUT_DIR = BASE_DIR / "outputs"
OUTPUT_DIR.mkdir(exist_ok=True)

OUTPUT_PDF = OUTPUT_DIR / "LUXAR_Dossier_Mercado_Setubal_v1.pdf"

W, H = A4  # 595 x 842 pt

# ─── Paleta ───────────────────────────────────────────────────────────────────

NAVY    = colors.HexColor("#1A3E5C")
BLUE    = colors.HexColor("#2E6DA4")
GOLD    = colors.HexColor("#F4A020")
LIGHT   = colors.HexColor("#F7F9FC")
WHITE   = colors.white
GREY    = colors.HexColor("#6B7280")
LGREY   = colors.HexColor("#E5E9EF")
BLACK   = colors.HexColor("#111827")

# ─── Estilos ──────────────────────────────────────────────────────────────────

def build_styles():
    styles = {}

    styles["cover_brand"] = ParagraphStyle(
        "cover_brand",
        fontName="Helvetica-Bold",
        fontSize=11,
        textColor=GOLD,
        alignment=TA_LEFT,
        spaceAfter=2,
    )
    styles["cover_title"] = ParagraphStyle(
        "cover_title",
        fontName="Helvetica-Bold",
        fontSize=28,
        textColor=WHITE,
        alignment=TA_LEFT,
        leading=34,
        spaceAfter=8,
    )
    styles["cover_subtitle"] = ParagraphStyle(
        "cover_subtitle",
        fontName="Helvetica",
        fontSize=14,
        textColor=colors.HexColor("#B0C4D8"),
        alignment=TA_LEFT,
        spaceAfter=4,
    )
    styles["cover_meta"] = ParagraphStyle(
        "cover_meta",
        fontName="Helvetica",
        fontSize=9,
        textColor=colors.HexColor("#8AA5BE"),
        alignment=TA_LEFT,
    )
    styles["cover_disclaimer"] = ParagraphStyle(
        "cover_disclaimer",
        fontName="Helvetica",
        fontSize=7.5,
        textColor=colors.HexColor("#5A7A96"),
        alignment=TA_LEFT,
    )

    styles["section_label"] = ParagraphStyle(
        "section_label",
        fontName="Helvetica-Bold",
        fontSize=7.5,
        textColor=GOLD,
        alignment=TA_LEFT,
        spaceBefore=0,
        spaceAfter=4,
        leading=10,
    )
    styles["section_title"] = ParagraphStyle(
        "section_title",
        fontName="Helvetica-Bold",
        fontSize=17,
        textColor=NAVY,
        alignment=TA_LEFT,
        spaceBefore=4,
        spaceAfter=6,
        leading=21,
    )
    styles["body"] = ParagraphStyle(
        "body",
        fontName="Helvetica",
        fontSize=9.5,
        textColor=BLACK,
        alignment=TA_LEFT,
        leading=15,
        spaceAfter=8,
    )
    styles["body_small"] = ParagraphStyle(
        "body_small",
        fontName="Helvetica",
        fontSize=8.5,
        textColor=GREY,
        alignment=TA_LEFT,
        leading=13,
        spaceAfter=6,
    )
    styles["insight_label"] = ParagraphStyle(
        "insight_label",
        fontName="Helvetica-Bold",
        fontSize=7,
        textColor=GOLD,
        alignment=TA_LEFT,
        spaceAfter=2,
    )
    styles["insight_text"] = ParagraphStyle(
        "insight_text",
        fontName="Helvetica",
        fontSize=8.5,
        textColor=NAVY,
        alignment=TA_LEFT,
        leading=13,
    )
    styles["footer_text"] = ParagraphStyle(
        "footer_text",
        fontName="Helvetica",
        fontSize=7,
        textColor=GREY,
        alignment=TA_LEFT,
    )
    styles["footer_right"] = ParagraphStyle(
        "footer_right",
        fontName="Helvetica",
        fontSize=7,
        textColor=GREY,
        alignment=TA_RIGHT,
    )
    styles["toc_number"] = ParagraphStyle(
        "toc_number",
        fontName="Helvetica-Bold",
        fontSize=9,
        textColor=GOLD,
        alignment=TA_LEFT,
    )
    styles["toc_title"] = ParagraphStyle(
        "toc_title",
        fontName="Helvetica",
        fontSize=9,
        textColor=NAVY,
        alignment=TA_LEFT,
    )
    styles["stat_value"] = ParagraphStyle(
        "stat_value",
        fontName="Helvetica-Bold",
        fontSize=22,
        textColor=NAVY,
        alignment=TA_CENTER,
        leading=26,
    )
    styles["stat_label"] = ParagraphStyle(
        "stat_label",
        fontName="Helvetica",
        fontSize=7.5,
        textColor=GREY,
        alignment=TA_CENTER,
        leading=11,
    )
    styles["stat_delta"] = ParagraphStyle(
        "stat_delta",
        fontName="Helvetica-Bold",
        fontSize=9,
        textColor=colors.HexColor("#27AE60"),
        alignment=TA_CENTER,
    )

    return styles

S = build_styles()

# ─── Page templates ───────────────────────────────────────────────────────────

class LuxarDoc(BaseDocTemplate):
    def __init__(self, filename, **kwargs):
        super().__init__(filename, **kwargs)
        self.page_num = 0

    def handle_pageBegin(self):
        self.page_num += 1
        super().handle_pageBegin()


def cover_background(canvas, doc):
    canvas.saveState()
    # Fundo principal Navy
    canvas.setFillColor(NAVY)
    canvas.rect(0, 0, W, H, fill=1, stroke=0)
    # Barra dourada lateral
    canvas.setFillColor(GOLD)
    canvas.rect(0, 0, 5, H, fill=1, stroke=0)
    # Bloco geométrico decorativo (canto superior direito)
    canvas.setFillColor(colors.HexColor("#163354"))
    canvas.rect(W * 0.55, H * 0.55, W * 0.45, H * 0.45, fill=1, stroke=0)
    # Linha dourada horizontal
    canvas.setStrokeColor(GOLD)
    canvas.setLineWidth(0.5)
    canvas.line(40, H * 0.28, W - 40, H * 0.28)
    canvas.restoreState()


def content_background(canvas, doc):
    canvas.saveState()
    # Barra lateral esquerda fina
    canvas.setFillColor(NAVY)
    canvas.rect(0, 0, 4, H, fill=1, stroke=0)
    # Header band
    canvas.setFillColor(LIGHT)
    canvas.rect(0, H - 28, W, 28, fill=1, stroke=0)
    # Nome da marca no header
    canvas.setFont("Helvetica-Bold", 7.5)
    canvas.setFillColor(NAVY)
    canvas.drawString(20, H - 18, "LUXAR")
    canvas.setFont("Helvetica", 7)
    canvas.setFillColor(GREY)
    canvas.drawString(56, H - 18, "Inteligência de Mercado Imobiliário")
    # Linha separadora header
    canvas.setStrokeColor(LGREY)
    canvas.setLineWidth(0.5)
    canvas.line(0, H - 28, W, H - 28)
    # Footer
    canvas.setFillColor(LIGHT)
    canvas.rect(0, 0, W, 22, fill=1, stroke=0)
    canvas.setStrokeColor(LGREY)
    canvas.line(0, 22, W, 22)
    canvas.setFont("Helvetica", 6.5)
    canvas.setFillColor(GREY)
    canvas.drawString(20, 8, "Dossier de Mercado — Península de Setúbal | v1 | Mai 2026")
    canvas.drawRightString(W - 20, 8, f"Página {doc.page}")
    canvas.restoreState()


def build_page_templates(doc):
    cover_frame = Frame(
        40, 60, W - 80, H - 120,
        leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0,
        id="cover",
    )
    content_frame = Frame(
        30, 32, W - 50, H - 70,
        leftPadding=0, rightPadding=0, topPadding=8, bottomPadding=0,
        id="content",
    )
    cover_tpl = PageTemplate(id="Cover", frames=[cover_frame], onPage=cover_background)
    content_tpl = PageTemplate(id="Content", frames=[content_frame], onPage=content_background)
    doc.addPageTemplates([cover_tpl, content_tpl])


# ─── Componentes ──────────────────────────────────────────────────────────────

def hrule(width=W - 80, color=LGREY, thickness=0.5):
    data = [[""]]
    t = Table(data, colWidths=[width])
    t.setStyle(TableStyle([
        ("LINEBELOW", (0, 0), (-1, -1), thickness, color),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
    ]))
    return t


def insight_box(text: str, width=W - 80):
    """Caixa de insight com borda esquerda dourada."""
    inner = Paragraph(text, S["insight_text"])
    label = Paragraph("▲ INSIGHT PRINCIPAL", S["insight_label"])
    data = [[label], [inner]]
    t = Table(data, colWidths=[width - 24])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#FFFBF0")),
        ("LEFTPADDING", (0, 0), (-1, -1), 12),
        ("RIGHTPADDING", (0, 0), (-1, -1), 12),
        ("TOPPADDING", (0, 0), (0, 0), 10),
        ("BOTTOMPADDING", (0, -1), (-1, -1), 10),
        ("TOPPADDING", (0, 1), (-1, -1), 4),
        ("LINEBEFORE", (0, 0), (0, -1), 3, GOLD),
        ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#F0E0C0")),
    ]))
    return t


def stat_card(value: str, label: str, delta: str = "", bg=LIGHT):
    """Cartão de KPI compacto."""
    content = [
        [Paragraph(value, S["stat_value"])],
        [Paragraph(label, S["stat_label"])],
    ]
    if delta:
        content.append([Paragraph(delta, S["stat_delta"])])
    t = Table(content, colWidths=[120])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), bg),
        ("BOX", (0, 0), (-1, -1), 0.5, LGREY),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 10),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]))
    return t


def kpi_row(cards: list, total_width=W - 80):
    """Linha de KPI cards."""
    n = len(cards)
    col_w = total_width / n
    data = [cards]
    t = Table(data, colWidths=[col_w] * n)
    t.setStyle(TableStyle([
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ]))
    return t


def chart_image(filename: str, max_width=W - 80, max_height=None):
    path = GRAFICOS_DIR / filename
    if not path.exists():
        return Paragraph(f"[Gráfico não encontrado: {filename}]", S["body_small"])
    img = Image(str(path))
    iw, ih = img.imageWidth, img.imageHeight
    scale = min(max_width / iw, (max_height or 999) / ih)
    img.drawWidth = iw * scale
    img.drawHeight = ih * scale
    return img


def section_header(number: str, title: str):
    return [
        Paragraph(f"SECÇÃO {number}", S["section_label"]),
        Paragraph(title, S["section_title"]),
        hrule(color=NAVY, thickness=1),
        Spacer(1, 8),
    ]


# ─── Conteúdo ─────────────────────────────────────────────────────────────────

def build_cover():
    story = []
    story.append(Spacer(1, H * 0.08))
    story.append(Paragraph("LUXAR", S["cover_brand"]))
    story.append(Spacer(1, 6))
    story.append(Paragraph(
        "Dossier de Mercado<br/>Imobiliário",
        S["cover_title"],
    ))
    story.append(Paragraph(
        "Península de Setúbal — 2019 a 2025",
        S["cover_subtitle"],
    ))
    story.append(Spacer(1, 20))
    story.append(Paragraph(
        "Análise trimestral de preços, volume de transações<br/>"
        "e dinâmicas de mercado por município",
        S["cover_meta"],
    ))
    story.append(Spacer(1, H * 0.18))
    story.append(hrule(color=colors.HexColor("#2A5A82"), thickness=0.5))
    story.append(Spacer(1, 12))

    meta_data = [
        ["Versão", "Edição", "Período de dados", "Produzido por"],
        ["v1.0", "Mai 2026", "Q1 2019 — Q4 2025", "LUXAR | luxar.pt"],
    ]
    meta_table = Table(meta_data, colWidths=[80, 80, 140, 130])
    meta_table.setStyle(TableStyle([
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica"),
        ("FONTSIZE", (0, 0), (-1, 0), 7),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.HexColor("#5A7A96")),
        ("FONTNAME", (0, 1), (-1, 1), "Helvetica-Bold"),
        ("FONTSIZE", (0, 1), (-1, 1), 8.5),
        ("TEXTCOLOR", (0, 1), (-1, 1), WHITE),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 10),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 20))
    story.append(Paragraph(
        "Fonte de dados: INE — Estatísticas de Preços da Habitação ao Nível Local (EPH)  |  "
        "Dados de acesso público. Análise e tratamento LUXAR.",
        S["cover_disclaimer"],
    ))
    return story


def build_intro():
    story = []
    story.append(NextPageTemplate("Content"))
    story.append(PageBreak())
    story += section_header("—", "Índice")

    toc_items = [
        ("01", "Contexto e Território"),
        ("02", "Preços: Evolução da Sub-Região"),
        ("03", "Preços por Município — Série Histórica"),
        ("04", "Ranking de Preços — Q4 2025"),
        ("05", "Volume de Transações"),
        ("06", "Variação Homóloga — Heatmap"),
        ("07", "Distribuição de Preços em 2025"),
        ("08", "Metodologia e Fontes"),
    ]
    for num, title in toc_items:
        row = Table(
            [[Paragraph(num, S["toc_number"]), Paragraph(title, S["toc_title"])]],
            colWidths=[30, W - 120],
        )
        row.setStyle(TableStyle([
            ("LEFTPADDING", (0, 0), (-1, -1), 0),
            ("RIGHTPADDING", (0, 0), (-1, -1), 0),
            ("TOPPADDING", (0, 0), (-1, -1), 7),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
            ("LINEBELOW", (0, 0), (-1, -1), 0.3, LGREY),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ]))
        story.append(row)

    story.append(Spacer(1, 20))
    story.append(hrule(color=LGREY))
    story.append(Spacer(1, 16))

    story.append(Paragraph("SOBRE ESTE DOSSIER", S["section_label"]))
    story.append(Spacer(1, 6))
    story.append(Paragraph(
        "Este relatório analisa a evolução do mercado residencial na Península de Setúbal "
        "entre o 1.º trimestre de 2019 e o 4.º trimestre de 2025. Cobre nove municípios "
        "da sub-região NUTS 1B: Alcochete, Almada, Barreiro, Moita, Montijo, Palmela, "
        "Seixal, Sesimbra e Setúbal.",
        S["body"],
    ))
    story.append(Paragraph(
        "A análise foca-se em três dimensões: evolução de preços medianos por m², "
        "volume de transações e variação homóloga — permitindo contextualizar cada "
        "município no conjunto da sub-região e identificar tendências estruturais.",
        S["body"],
    ))
    story.append(Spacer(1, 10))

    # KPIs de contexto
    cards = [
        stat_card("9", "Municípios\nanalisados"),
        stat_card("28", "Trimestres\nde dados"),
        stat_card("2.831 €", "Preço mediano/m²\nQ4 2025 (sub-região)", "▲ +27,4% YoY"),
        stat_card("~16.000", "Transações/ano\n(média 2024–2025)"),
    ]
    story.append(kpi_row(cards))

    return story


def build_section_01():
    """Contexto e território."""
    story = [PageBreak()]
    story += section_header("01", "Contexto e Território")

    story.append(Paragraph(
        "A Península de Setúbal (NUTS III — código 1B) localiza-se a sul da Área "
        "Metropolitana de Lisboa, separada da capital pelo estuário do Tejo. "
        "A sua proximidade a Lisboa, combinada com preços historicamente mais acessíveis "
        "e crescente oferta de transportes (Fertagus, Transtejo, Barreiro-Oriente), "
        "tem alimentado uma procura crescente de famílias em busca de habitação principal.",
        S["body"],
    ))
    story.append(Paragraph(
        "O mercado da Península de Setúbal tem registado uma aceleração consistente desde "
        "2022, com Almada, Seixal e Sesimbra a liderarem a valorização. Em 2025, o preço "
        "mediano da sub-região ultrapassou os 2.800 €/m² — reflectindo uma valorização "
        "superior a 70% face ao início de 2019.",
        S["body"],
    ))

    story.append(Spacer(1, 10))

    # Tabela de municípios
    story.append(Paragraph("MUNICÍPIOS INCLUÍDOS", S["section_label"]))
    story.append(Spacer(1, 6))

    mun_data = [
        ["Município", "Cód. INE", "Preço Med./m² Q4 2025", "Var. YoY"],
        ["Almada",    "1B01503", "3.311 €",  "+18,9%"],
        ["Sesimbra",  "1B01511", "3.010 €",  "+25,3%"],
        ["Seixal",    "1B01510", "2.901 €",  "+27,0%"],
        ["Barreiro",  "1B01504", "2.821 €",  "+35,0%"],
        ["Alcochete", "1B01502", "2.737 €",  "+24,4%"],
        ["Setúbal",   "1B01512", "2.699 €",  "+27,3%"],
        ["Montijo",   "1B01507", "2.652 €",  "+27,4%"],
        ["Moita",     "1B01506", "2.510 €",  "+37,2%"],
        ["Palmela",   "1B01508", "2.471 €",  "+17,2%"],
    ]
    col_ws = [130, 80, 130, 80]
    t = Table(mun_data, colWidths=col_ws)
    t.setStyle(TableStyle([
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 8.5),
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
        ("BACKGROUND", (0, 1), (-1, -1), WHITE),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [WHITE, LIGHT]),
        ("TEXTCOLOR", (0, 1), (-1, -1), BLACK),
        ("TEXTCOLOR", (3, 1), (3, -1), colors.HexColor("#27AE60")),
        ("FONTNAME", (3, 1), (3, -1), "Helvetica-Bold"),
        ("ALIGN", (2, 0), (-1, -1), "RIGHT"),
        ("LEFTPADDING", (0, 0), (-1, -1), 10),
        ("RIGHTPADDING", (0, 0), (-1, -1), 10),
        ("TOPPADDING", (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
        ("BOX", (0, 0), (-1, -1), 0.5, LGREY),
        ("LINEBELOW", (0, 0), (-1, -1), 0.3, LGREY),
    ]))
    story.append(t)
    story.append(Spacer(1, 6))
    story.append(Paragraph(
        "Fonte: INE, EPH Q4 2025. YoY = variação face ao mesmo trimestre do ano anterior.",
        S["body_small"],
    ))

    return story


def build_section_02():
    """Evolução preço sub-região."""
    story = [PageBreak()]
    story += section_header("02", "Evolução do Preço Mediano — Sub-Região")

    story.append(Paragraph(
        "O gráfico abaixo apresenta a série trimestral completa do preço mediano de "
        "habitação por m² na Península de Setúbal, desde Q1 2019 até Q4 2025.",
        S["body"],
    ))
    story.append(Spacer(1, 8))
    story.append(chart_image("01_evolucao_preco_subreigiao.png", max_width=W - 80, max_height=320))
    story.append(Spacer(1, 12))
    story.append(insight_box(
        "O preço mediano da Península de Setúbal cresceu de 1.280 €/m² em Q1 2019 para "
        "2.831 €/m² em Q4 2025 — uma valorização de <b>+121%</b> em 6 anos e meio. "
        "O ritmo de crescimento acelerou visivelmente desde 2024: o ano de 2025 registou "
        "a maior variação homóloga da série, com +27,4% no Q4."
    ))
    story.append(Spacer(1, 10))
    story.append(Paragraph(
        "A série reflecte um mercado com procura estrutural robusta, impulsionada pela "
        "atractividade relativa face a Lisboa e pela escassez de oferta nova. "
        "O abrandamento verificado em 2020–2021 (impacto COVID) foi rapidamente "
        "reabsorvido, sem que os preços tenham recuado em nenhum trimestre desde 2019.",
        S["body"],
    ))
    return story


def build_section_03():
    """Evolução por município."""
    story = [PageBreak()]
    story += section_header("03", "Preços por Município — Série Histórica")

    story.append(Paragraph(
        "Evolução trimestral do preço mediano por m² para cada um dos nove municípios "
        "da Península de Setúbal, com foco no período 2022–2025.",
        S["body"],
    ))
    story.append(Spacer(1, 8))
    story.append(chart_image("02_evolucao_preco_municipios.png", max_width=W - 80, max_height=330))
    story.append(Spacer(1, 12))
    story.append(insight_box(
        "Almada mantém-se consistentemente acima dos restantes municípios, atingindo "
        "3.311 €/m² em Q4 2025. O Barreiro e a Moita registaram as maiores acelerações "
        "relativas em 2025 — sinais de uma convergência de preços no mercado da margem sul. "
        "Palmela apresenta o crescimento mais moderado, permanecendo abaixo dos 2.500 €/m²."
    ))
    return story


def build_section_04():
    """Ranking Q4 2025."""
    story = [PageBreak()]
    story += section_header("04", "Ranking de Preços — Q4 2025")

    story.append(Paragraph(
        "Comparação do preço mediano por m² entre municípios no último trimestre "
        "disponível (Q4 2025), com indicação da variação face ao mesmo período de 2024.",
        S["body"],
    ))
    story.append(Spacer(1, 8))
    story.append(chart_image("03_ranking_preco_q4_2025.png", max_width=W - 80, max_height=330))
    story.append(Spacer(1, 12))
    story.append(insight_box(
        "Spread de preços de 840 €/m² entre Almada (3.311 €) e Palmela (2.471 €). "
        "Todos os municípios registaram variações homólogas positivas superiores a 17%, "
        "com destaque para Moita (+37,2%) e Barreiro (+35,0%) — municípios historicamente "
        "mais acessíveis que estão agora a convergir para a média da sub-região."
    ))
    return story


def build_section_05():
    """Volume de transações."""
    story = [PageBreak()]
    story += section_header("05", "Volume de Transações")

    story.append(Paragraph(
        "Evolução trimestral do número de transações de alojamentos familiares na "
        "Península de Setúbal, com média móvel de 4 trimestres.",
        S["body"],
    ))
    story.append(Spacer(1, 8))
    story.append(chart_image("04_volume_transacoes_trimestral.png", max_width=W - 80, max_height=300))
    story.append(Spacer(1, 12))
    story.append(insight_box(
        "O volume de transações atingiu o pico em 2021–2022, seguido de uma correcção "
        "em 2022–2023 (subida de taxas de juro). Em 2024–2025, o mercado retomou "
        "o crescimento: Q4 2025 registou 4.011 transações na sub-região, aproximando-se "
        "dos máximos históricos. A tendência sugere procura sólida apesar da subida de preços."
    ))
    return story


def build_section_06():
    """Heatmap YoY."""
    story = [PageBreak()]
    story += section_header("06", "Variação Homóloga — Heatmap")

    story.append(Paragraph(
        "Visualização da variação homóloga do preço mediano/m² para cada município "
        "e trimestre desde 2021. Verde intenso indica forte valorização; vermelho, "
        "desaceleração ou queda.",
        S["body"],
    ))
    story.append(Spacer(1, 8))
    story.append(chart_image("05_heatmap_yoy_municipios.png", max_width=W - 80, max_height=260))
    story.append(Spacer(1, 12))
    story.append(insight_box(
        "O heatmap revela três fases distintas: (1) crescimento forte em 2021–2022 "
        "(pós-pandemia); (2) moderação em 2023 com variações entre 8% e 14%; "
        "(3) reaceleração generalizada em 2024–2025, com todos os municípios a superar "
        "15% de valorização homóloga no Q4 2025. Nenhum município registou queda de preços."
    ))
    return story


def build_section_07():
    """Distribuição 2025."""
    story = [PageBreak()]
    story += section_header("07", "Distribuição de Preços em 2025")

    story.append(Paragraph(
        "Evolução intra-anual do preço mediano por m² durante os quatro trimestres "
        "de 2025, por município. Permite visualizar o ritmo e amplitude de subida "
        "ao longo do ano.",
        S["body"],
    ))
    story.append(Spacer(1, 8))
    story.append(chart_image("06_distribuicao_precos_2025.png", max_width=W - 80, max_height=330))
    story.append(Spacer(1, 12))
    story.append(insight_box(
        "Em 2025, todos os municípios registaram subidas consistentes trimestre a trimestre. "
        "Almada e Seixal apresentam a maior amplitude de variação intra-anual (>300 €/m²). "
        "A convergência progressiva entre municípios sugere que o mercado da Península de "
        "Setúbal está a tornar-se mais homogéneo, com menor diferencial de preços relativos."
    ))
    return story


def build_metodologia():
    """Metodologia e fontes."""
    story = [PageBreak()]
    story += section_header("08", "Metodologia e Fontes")

    story.append(Paragraph(
        "FONTES DE DADOS",
        S["insight_label"],
    ))
    story.append(Paragraph(
        "INE — Instituto Nacional de Estatística, Estatísticas de Preços da Habitação "
        "ao Nível Local (EPH), publicações trimestrais Q1 a Q4 2025. Dados de acesso "
        "público disponíveis em www.ine.pt.",
        S["body"],
    ))

    story.append(Paragraph("INDICADORES", S["insight_label"]))
    indicadores = [
        ["Indicador", "Definição"],
        ["Preço mediano/m²",
         "Valor mediano das vendas de alojamentos familiares por metro quadrado útil, "
         "em euros. Robusto face a outliers."],
        ["N.º de transações",
         "Número total de escrituras de compra e venda de alojamentos familiares "
         "registadas no trimestre."],
        ["Variação YoY",
         "Taxa de variação homóloga: comparação com o mesmo trimestre do ano anterior."],
        ["Variação QoQ",
         "Taxa de variação face ao trimestre imediatamente anterior."],
    ]
    t = Table(indicadores, colWidths=[130, W - 80 - 140])
    t.setStyle(TableStyle([
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 8),
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [WHITE, LIGHT]),
        ("LEFTPADDING", (0, 0), (-1, -1), 10),
        ("RIGHTPADDING", (0, 0), (-1, -1), 10),
        ("TOPPADDING", (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("BOX", (0, 0), (-1, -1), 0.5, LGREY),
        ("LINEBELOW", (0, 0), (-1, -1), 0.3, LGREY),
    ]))
    story.append(t)
    story.append(Spacer(1, 12))

    story.append(Paragraph("PROCESSAMENTO", S["insight_label"]))
    story.append(Paragraph(
        "Pipeline de dados desenvolvido em Python 3.13 com as bibliotecas pandas, "
        "openpyxl e DuckDB. Dados extraídos das sheets trimestrais dos ficheiros "
        "Excel EPH, transformados para formato long (tidy data) e exportados como "
        "Parquet e CSV. Visualizações geradas com matplotlib. Código open-source "
        "disponível no GitHub.",
        S["body"],
    ))

    story.append(Paragraph("LIMITAÇÕES", S["insight_label"]))
    story.append(Paragraph(
        "• Dados por tipologia (T0, T1, T2, T3+) não disponíveis a nível de município "
        "nas publicações EPH.<br/>"
        "• Alguns municípios com baixo volume de transações apresentam dados "
        "confidenciais (marcados como '//' pelo INE) em determinados trimestres.<br/>"
        "• O preço mediano/m² refere-se a alojamentos familiares no total, sem "
        "distinção entre novos e existentes a nível municipal.<br/>"
        "• O Distrito de Setúbal em termos administrativos inclui também municípios "
        "classificados no NUTS Alentejo Litoral (ex: Grândola, Alcácer do Sal) — "
        "esses dados não estão incluídos neste dossier.",
        S["body"],
    ))

    story.append(Spacer(1, 16))
    story.append(hrule(color=LGREY))
    story.append(Spacer(1, 10))

    story.append(Paragraph(
        "Produzido por LUXAR | tiago@luxar.pt | luxar.pt<br/>"
        "Dados: INE, licença de utilização pública. Análise e visualizações: © LUXAR 2026.",
        S["body_small"],
    ))

    return story


# ─── Build ────────────────────────────────────────────────────────────────────

def build_pdf():
    doc = LuxarDoc(
        str(OUTPUT_PDF),
        pagesize=A4,
        leftMargin=0,
        rightMargin=0,
        topMargin=0,
        bottomMargin=0,
    )
    build_page_templates(doc)

    story = []
    story += build_cover()
    story += build_intro()
    story += build_section_01()
    story += build_section_02()
    story += build_section_03()
    story += build_section_04()
    story += build_section_05()
    story += build_section_06()
    story += build_section_07()
    story += build_metodologia()

    doc.build(story)
    print(f"\n✅ PDF gerado: {OUTPUT_PDF}")
    print(f"   Tamanho: {OUTPUT_PDF.stat().st_size / 1024:.0f} KB")


if __name__ == "__main__":
    build_pdf()
