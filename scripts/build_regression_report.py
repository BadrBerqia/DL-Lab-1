"""Generate the final PDF report for Part 1 of the Deep Learning lab."""

from pathlib import Path

import pandas as pd
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    Image,
    KeepTogether,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


ROOT = Path(__file__).resolve().parents[1]
FIGURES = ROOT / "outputs" / "figures"
METRICS = ROOT / "outputs" / "metrics"
OUTPUT = ROOT / "report" / "final" / "rapport_regression_nyse.pdf"
OUTPUT.parent.mkdir(parents=True, exist_ok=True)

BLUE = colors.HexColor("#1F4E79")
LIGHT_BLUE = colors.HexColor("#DCE6F1")
ORANGE = colors.HexColor("#D97706")
GREEN = colors.HexColor("#4F7D5C")
LIGHT_GRAY = colors.HexColor("#F3F5F7")
DARK = colors.HexColor("#20262E")


def register_fonts():
    regular = Path(r"C:\Windows\Fonts\arial.ttf")
    bold = Path(r"C:\Windows\Fonts\arialbd.ttf")
    if regular.exists() and bold.exists():
        pdfmetrics.registerFont(TTFont("LabSans", str(regular)))
        pdfmetrics.registerFont(TTFont("LabSans-Bold", str(bold)))
        return "LabSans", "LabSans-Bold"
    return "Helvetica", "Helvetica-Bold"


FONT, FONT_BOLD = register_fonts()

styles = getSampleStyleSheet()
styles.add(
    ParagraphStyle(
        name="LabTitle",
        fontName=FONT_BOLD,
        fontSize=25,
        leading=30,
        textColor=BLUE,
        alignment=TA_CENTER,
        spaceAfter=14,
    )
)
styles.add(
    ParagraphStyle(
        name="LabSubtitle",
        fontName=FONT,
        fontSize=13,
        leading=18,
        textColor=DARK,
        alignment=TA_CENTER,
        spaceAfter=10,
    )
)
styles.add(
    ParagraphStyle(
        name="LabH1",
        fontName=FONT_BOLD,
        fontSize=17,
        leading=21,
        textColor=BLUE,
        spaceBefore=8,
        spaceAfter=10,
    )
)
styles.add(
    ParagraphStyle(
        name="LabH2",
        fontName=FONT_BOLD,
        fontSize=12,
        leading=15,
        textColor=GREEN,
        spaceBefore=6,
        spaceAfter=6,
    )
)
styles.add(
    ParagraphStyle(
        name="LabBody",
        fontName=FONT,
        fontSize=9.5,
        leading=14,
        textColor=DARK,
        alignment=TA_JUSTIFY,
        spaceAfter=7,
    )
)
styles.add(
    ParagraphStyle(
        name="LabBullet",
        fontName=FONT,
        fontSize=9.2,
        leading=13,
        leftIndent=12,
        firstLineIndent=-7,
        textColor=DARK,
        spaceAfter=4,
    )
)
styles.add(
    ParagraphStyle(
        name="LabCaption",
        fontName=FONT,
        fontSize=8,
        leading=10,
        textColor=colors.HexColor("#555555"),
        alignment=TA_CENTER,
        spaceBefore=4,
        spaceAfter=8,
    )
)
styles.add(
    ParagraphStyle(
        name="LabCallout",
        fontName=FONT_BOLD,
        fontSize=10,
        leading=14,
        textColor=BLUE,
        alignment=TA_LEFT,
        borderColor=LIGHT_BLUE,
        borderWidth=1,
        borderPadding=8,
        backColor=LIGHT_GRAY,
        spaceBefore=8,
        spaceAfter=10,
    )
)
styles.add(
    ParagraphStyle(
        name="Small",
        fontName=FONT,
        fontSize=7.5,
        leading=9,
        textColor=DARK,
    )
)


def p(text, style="LabBody"):
    return Paragraph(text, styles[style])


def bullet(text):
    return p(f"- {text}", "LabBullet")


def section(title):
    return p(title, "LabH1")


def subsection(title):
    return p(title, "LabH2")


def figure(filename, caption, width=16.5 * cm, height=None):
    path = FIGURES / filename
    image = Image(str(path), width=width, height=height)
    image.hAlign = "CENTER"
    return KeepTogether([image, p(caption, "LabCaption")])


def styled_table(data, widths, font_size=8):
    table = Table(data, colWidths=widths, repeatRows=1, hAlign="CENTER")
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), BLUE),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("FONTNAME", (0, 0), (-1, 0), FONT_BOLD),
                ("FONTNAME", (0, 1), (-1, -1), FONT),
                ("FONTSIZE", (0, 0), (-1, -1), font_size),
                ("LEADING", (0, 0), (-1, -1), font_size + 2),
                ("ALIGN", (1, 1), (-1, -1), "CENTER"),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, LIGHT_GRAY]),
                ("GRID", (0, 0), (-1, -1), 0.35, colors.HexColor("#9AA5B1")),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ]
        )
    )
    return table


def draw_page(canvas, document):
    canvas.saveState()
    page = canvas.getPageNumber()
    if page > 1:
        canvas.setStrokeColor(LIGHT_BLUE)
        canvas.line(2 * cm, A4[1] - 1.35 * cm, A4[0] - 2 * cm, A4[1] - 1.35 * cm)
        canvas.setFont(FONT, 7.5)
        canvas.setFillColor(colors.HexColor("#667085"))
        canvas.drawString(2 * cm, A4[1] - 1.05 * cm, "Atelier 1 - Régression NYSE")
        canvas.drawRightString(A4[0] - 2 * cm, 1.05 * cm, f"Page {page}")
    canvas.restoreState()


comparison = pd.read_csv(METRICS / "regression_model_comparison.csv", index_col=0)
epoch_metrics = pd.read_csv(METRICS / "regression_epoch_metrics.csv")
grid = pd.read_csv(METRICS / "grid_search_results.csv")
best_grid = grid.loc[grid["validation_mse"].idxmin()]

doc = SimpleDocTemplate(
    str(OUTPUT),
    pagesize=A4,
    rightMargin=1.8 * cm,
    leftMargin=1.8 * cm,
    topMargin=1.8 * cm,
    bottomMargin=1.6 * cm,
    title="Atelier 1 - Régression NYSE avec PyTorch",
    author="Badr BERQIA",
)

story = []

# Cover
story.extend(
    [
        Spacer(1, 2.1 * cm),
        p("Atelier 1 de Deep Learning", "LabTitle"),
        p("Régression des prix de clôture NYSE avec un MLP PyTorch", "LabSubtitle"),
        Spacer(1, 0.8 * cm),
        Table(
            [
                [p("<b>Étudiant</b>", "LabBody"), p("Badr BERQIA", "LabBody")],
                [p("<b>Partie rendue</b>", "LabBody"), p("Partie 1 - Régression", "LabBody")],
                [p("<b>Dataset</b>", "LabBody"), p("NYSE - prices-split-adjusted.csv", "LabBody")],
                [p("<b>Environnement</b>", "LabBody"), p("Windows local, Python 3.12, PyTorch, CUDA, RTX 3070", "LabBody")],
            ],
            colWidths=[4.2 * cm, 10.2 * cm],
            style=TableStyle(
                [
                    ("BACKGROUND", (0, 0), (0, -1), LIGHT_BLUE),
                    ("BOX", (0, 0), (-1, -1), 0.6, BLUE),
                    ("INNERGRID", (0, 0), (-1, -1), 0.3, colors.HexColor("#9AA5B1")),
                    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                    ("TOPPADDING", (0, 0), (-1, -1), 8),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
                ]
            ),
        ),
        Spacer(1, 0.8 * cm),
        p(
            "Dans ce rapport, je présente uniquement la partie régression. Je n'inclus pas la classification multiclasse de la partie 2 dans ce rendu.",
            "LabCallout",
        ),
        Spacer(1, 1.2 * cm),
        p(
            "<b>Note sur mon environnement.</b> L'énoncé mentionne Google Colab ou Kaggle comme environnements possibles. "
            "J'ai effectué tous mes entraînements et toutes mes évaluations localement sous Windows avec mon GPU personnel. "
            "J'utilise CUDA pour accélérer les calculs, tout en gardant mon notebook exécutable sur CPU.",
            "LabBody",
        ),
        PageBreak(),
    ]
)

# Problem and data
story.extend(
    [
        section("1. Objectif et formulation du problème"),
        p(
            "Mon objectif est de prédire, pour une action donnée et un jour de cotation t, le prix de clôture ajusté au prochain jour de cotation t+1. "
            "Je considère donc chaque couple action-date comme une observation. Ma table contient 851 264 lignes, 501 symboles et sept colonnes sur la période du 4 janvier 2010 au 30 décembre 2016.",
        ),
        subsection("Variables utilisées"),
        bullet("<b>Entrées que j'utilise :</b> open, high, low, close et volume observés au jour t."),
        bullet("<b>Cible que je prédis :</b> target_next_close, soit la clôture du prochain jour de cotation pour le même symbole."),
        bullet("<b>Construction que j'applique :</b> tri par symbole et date, puis groupby(&quot;symbol&quot;)[&quot;close&quot;].shift(-1)."),
        bullet("<b>Taille finale obtenue :</b> 850 763 exemples après retrait des 501 dernières lignes sans cible."),
        subsection("Contrôles de qualité"),
        p(
            "Je ne détecte aucune valeur manquante dans la table d'origine ni aucun doublon date-action. "
            "J'ai aussi vérifié que les contraintes OHLC sont respectées. Je conserve les vingt et une lignes dont le volume est nul, car elles sont rares et leurs prix restent cohérents.",
        ),
        figure(
            "01_aapl_close_over_time.png",
            "Figure 1 - Évolution temporelle du prix de clôture ajusté de l'action AAPL.",
            width=16.3 * cm,
            height=7.4 * cm,
        ),
        PageBreak(),
    ]
)

# EDA
story.extend(
    [
        section("2. Analyse exploratoire"),
        p(
            "Je visualise une seule action, AAPL, afin d'éviter de superposer 501 séries temporelles. "
            "J'observe une tendance globale haussière, mais aussi plusieurs baisses locales : je ne peux donc jamais connaître le prochain cours avec certitude.",
        ),
        figure(
            "01_aapl_current_vs_next_close.png",
            "Figure 2 - La clôture du lendemain est généralement proche de la clôture courante.",
            width=12.3 * cm,
            height=10.8 * cm,
        ),
        p(
            "J'observe que le nuage se concentre autour de la diagonale y = x. Cela justifie mon choix d'une baseline de persistance : prédire demain avec le prix d'aujourd'hui. "
            "Sur AAPL, j'obtiens une MAE de 0,9278 et une RMSE de 1,3393 avec cette règle.",
        ),
        PageBreak(),
    ]
)

# Split and model
split_data = [
    ["Ensemble", "Période", "Observations"],
    ["Entraînement", "2010-01-04 au 2014-12-30", "599 692"],
    ["Validation", "2015-01-02 au 2015-12-30", "124 458"],
    ["Test", "2016-01-04 au 2016-12-29", "125 624"],
]
story.extend(
    [
        section("3. Préparation des données"),
        p(
            "J'effectue un découpage chronologique. Je recalcule la cible séparément dans chaque période afin d'empêcher la première observation d'une période future de devenir la cible de la période précédente.",
        ),
        styled_table(split_data, [4.0 * cm, 7.7 * cm, 3.5 * cm], 8.5),
        Spacer(1, 0.35 * cm),
        p(
            "J'ajuste les StandardScaler des entrées et de la cible uniquement sur l'entraînement. "
            "Je transforme ensuite la validation et le test avec ces mêmes paramètres. Je convertis les arrays en float32 et je les regroupe en mini-batches PyTorch.",
        ),
        section("4. Modèle MLP initial"),
        bullet("J'ai choisi l'architecture 5 -> 64 -> ReLU -> 32 -> ReLU -> 1."),
        bullet("Mon modèle contient 2 497 paramètres entraînables."),
        bullet("J'utilise l'erreur quadratique moyenne sur la cible standardisée comme fonction de coût."),
        bullet("J'utilise Adam avec un learning rate de 0,001."),
        bullet("J'entraîne pendant 10 époques et je choisis le meilleur état sur la validation."),
        p(
            "Mon réseau reçoit cinq valeurs par exemple. Ses couches cachées apprennent des représentations intermédiaires ; sa dernière couche produit une seule valeur car ma cible est un prix continu unique.",
        ),
        figure(
            "01_baseline_loss_curves.png",
            "Figure 3 - Loss d'entraînement et de validation du MLP initial.",
            width=15.5 * cm,
            height=8.6 * cm,
        ),
        PageBreak(),
    ]
)

# Search and regularization
story.extend(
    [
        section("5. GridSearch et régularisation"),
        subsection("Recherche d'hyperparamètres"),
        p(
            "Avec GridSearchCV, je compare 16 combinaisons : architectures (32,16) ou (64,32), learning rates 0,0005 ou 0,001, optimiseurs Adam ou RMSprop, et 5 ou 10 époques. "
            "Pour maîtriser le temps de calcul, j'utilise un sous-échantillon déterministe de 80 000 exemples d'entraînement et 20 000 exemples de validation.",
        ),
        p(
            f"La meilleure configuration que j'obtiens sur ce sous-échantillon est <b>{best_grid['param_module__hidden_dims']}</b>, "
            f"learning rate <b>{best_grid['param_lr']:.4f}</b>, optimiseur <b>{best_grid['optimizer_name']}</b> et "
            f"<b>{int(best_grid['param_max_epochs'])} époques</b>, avec une MSE de validation standardisée de "
            f"<b>{best_grid['validation_mse']:.6f}</b>.",
        ),
        p(
            "Après mon réentraînement complet, cette configuration ne dépasse pas mon MLP initial. "
            "J'en conclus qu'un classement sur sous-échantillon n'est pas garanti de se conserver exactement sur toutes les données.",
        ),
        subsection("Techniques de régularisation"),
        bullet("<b>L2 :</b> weight_decay = 10^-4 ; pénalise les poids de grande amplitude."),
        bullet("<b>Dropout :</b> taux 0,2 après chaque couche cachée ; désactive aléatoirement des activations pendant l'entraînement."),
        bullet("<b>Dropout + L2 + early stopping :</b> combinaison des deux pénalités et arrêt après trois époques sans amélioration."),
        p(
            "Dans mes expériences, la régularisation n'améliore pas les performances. Le dropout dégrade fortement mon accuracy à ±5 %, ce qui indique plutôt du sous-apprentissage que la correction d'un overfitting.",
        ),
        figure(
            "01_numeric_correlations.png",
            "Figure 4 - Corrélations entre les variables numériques. Les prix OHLC sont très redondants.",
            width=12.3 * cm,
            height=9.6 * cm,
        ),
        PageBreak(),
    ]
)

# Results
result_data = [["Méthode", "MAE", "RMSE", "R²", "Acc. ±5 %"]]
for name, row in comparison.iterrows():
    result_data.append(
        [
            p(str(name), "Small"),
            f"{row['MAE']:.4f}",
            f"{row['RMSE']:.4f}",
            f"{row['R2']:.4f}",
            f"{row['Accuracy ±5% (%)']:.2f} %",
        ]
    )

story.extend(
    [
        section("6. Résultats sur l'ensemble de test"),
        p(
            "J'exprime la MAE et la RMSE dans l'unité du prix. Je définis l'accuracy de régression comme le pourcentage de mes prédictions dont l'erreur absolue est inférieure ou égale à 5 % de la vraie cible.",
        ),
        styled_table(result_data, [6.1 * cm, 2.1 * cm, 2.1 * cm, 2.0 * cm, 2.8 * cm], 7.5),
        Spacer(1, 0.35 * cm),
        p(
            "<b>Mon résultat principal :</b> j'obtiens la meilleure MAE (0,9484), la meilleure RMSE (2,1429) et la meilleure accuracy à ±5 % (97,81 %) avec la persistance. "
            "Mon MLP initial est proche, mais il n'apporte aucun gain qui justifierait sa complexité.",
            "LabCallout",
        ),
        figure(
            "01_model_comparison.png",
            "Figure 5 - Comparaison des erreurs et de l'accuracy à ±5 %.",
            width=16.6 * cm,
            height=6.6 * cm,
        ),
        PageBreak(),
    ]
)

# Curves and interpretation
story.extend(
    [
        section("7. Évolution au fil des époques"),
        figure(
            "01_loss_train_test.png",
            "Figure 6 - Loss standardisée de l'entraînement et du test.",
            width=15.2 * cm,
            height=8.1 * cm,
        ),
        figure(
            "01_accuracy_train_test.png",
            "Figure 7 - Pourcentage de prédictions à ±5 % sur l'entraînement et le test.",
            width=15.2 * cm,
            height=8.1 * cm,
        ),
        p(
            "J'observe que ma loss d'entraînement diminue globalement et que ma loss de test reste supérieure mais proche, sans divergence progressive. "
            "Mon accuracy se stabilise autour de 96 à 97 % après quelques époques. J'explique une partie de ses fluctuations par le seuil discret de ±5 % : une petite variation peut faire passer plusieurs exemples juste au-dessus ou juste au-dessous du seuil.",
        ),
        p(
            "Je ne détecte pas de signe fort d'overfitting sur dix époques. J'observe néanmoins que la progression devient faible après environ six époques, ce qui limite l'intérêt d'un entraînement beaucoup plus long.",
        ),
        PageBreak(),
    ]
)

# Conclusion and learning
story.extend(
    [
        section("8. Conclusion, limites et apprentissages"),
        subsection("Conclusion"),
        p(
            "Mon MLP apprend correctement la relation entre les prix du jour courant et la clôture suivante, mais il ne bat pas ma baseline de persistance. "
            "J'en retiens qu'un modèle complexe n'est utile que s'il améliore une référence simple et pertinente.",
        ),
        subsection("Limites"),
        bullet(
            "J'interprète le R² proche de 1 avec prudence : il mesure surtout la forte similarité entre deux niveaux de prix consécutifs et ne prouve pas que mon modèle prédit correctement les rendements ou la direction du marché."
        ),
        bullet(
            "J'observe que mes variables OHLC sont très corrélées et que le volume seul apporte peu d'information supplémentaire dans cette formulation."
        ),
        bullet(
            "J'ai volontairement limité ma GridSearch à un sous-échantillon et à 16 configurations pour rester compatible avec le temps disponible."
        ),
        bullet(
            "Pour prolonger mon travail, je pourrais prédire un rendement, ajouter une fenêtre temporelle de plusieurs jours ou utiliser un modèle séquentiel."
        ),
        subsection("Ce que ce travail m'a permis d'apprendre"),
        bullet("Inspecter un DataFrame, ses types, ses valeurs manquantes, ses doublons et ses statistiques."),
        bullet("Distinguer les variables d'entrée de la cible et construire une cible temporelle avec shift."),
        bullet("Respecter l'ordre chronologique et prévenir les fuites de données."),
        bullet("Standardiser avec des paramètres appris uniquement sur l'entraînement."),
        bullet("Comprendre les tensors, mini-batches, couches cachées, fonctions d'activation, loss, gradients et optimiseur."),
        bullet("Entraîner et évaluer un MLP PyTorch sur GPU local."),
        bullet("Comparer un réseau à une baseline, lire les courbes train/test et diagnostiquer l'overfitting."),
        bullet("Interpréter GridSearch, L2, dropout et early stopping sans supposer qu'ils améliorent toujours le modèle."),
        Spacer(1, 0.35 * cm),
        p(
            "<b>Mes livrables associés :</b> mon notebook entièrement exécuté, mes tableaux CSV de métriques, mes figures exportées et mon code d'installation reproductible dans le dossier DL-Lab-1.",
            "LabCallout",
        ),
    ]
)

doc.build(story, onFirstPage=draw_page, onLaterPages=draw_page)
print(f"Rapport créé : {OUTPUT}")
print(f"Taille : {OUTPUT.stat().st_size} octets")
