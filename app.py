import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import json
import os

# ================= CONFIG =================

ctk.set_appearance_mode("dark")

ROXO = "#8A05BE"
ROXO_HOVER = "#5A0280"
PRETO = "#121212"
CINZA = "#1E1E1E"
BRANCO = "#FFFFFF"

ARQUIVO = "historico.json"
renda_anual_global = None

# ================= HISTÓRICO =================

def salvar_historico(renda, imposto, dependentes):
    dados = carregar_historico()
    dados.append({
        "renda": renda,
        "imposto": imposto,
        "dependentes": dependentes
    })

    with open(ARQUIVO, "w") as f:
        json.dump(dados, f)


def carregar_historico():
    if not os.path.exists(ARQUIVO):
        return []
    with open(ARQUIVO, "r") as f:
        return json.load(f)

# ================= CÁLCULO =================

def calcular_imposto(renda, dependentes=0):
    renda -= 2275.08 * dependentes
    renda = max(0, renda)

    if renda <= 22847.76:
        return 0
    elif renda <= 33919.80:
        return (renda * 0.075) - 1713.58
    elif renda <= 45012.60:
        return (renda * 0.15) - 4257.57
    elif renda <= 55976.16:
        return (renda * 0.225) - 7633.51
    else:
        return (renda * 0.275) - 10432.32

# ================= TELAS =================

def mostrar_menu():
    limpar_tela()

    frame = ctk.CTkFrame(app, fg_color=PRETO)
    frame.pack(fill="both", expand=True)

    ctk.CTkLabel(
        frame,
        text="💳 Finance Dashboard",
        font=("Arial", 26, "bold"),
        text_color=ROXO
    ).pack(pady=40)

    ctk.CTkButton(
        frame,
        text="💰 Imposto de Renda",
        fg_color=ROXO,
        hover_color=ROXO_HOVER,
        height=40,
        command=abrir_ir
    ).pack(pady=15, padx=50, fill="x")

    ctk.CTkButton(
        frame,
        text="🧮 Calcular Renda",
        fg_color=ROXO,
        hover_color=ROXO_HOVER,
        height=40,
        command=abrir_calc
    ).pack(pady=15, padx=50, fill="x")


def abrir_ir():
    limpar_tela()

    ctk.CTkLabel(app, text="💰 Imposto de Renda", font=("Arial", 20)).pack(pady=10)

    global entry_renda, entry_dep, resultado, frame_grafico

    entry_renda = ctk.CTkEntry(app, placeholder_text="Renda anual")
    entry_renda.pack(pady=10)

    # AUTO PREENCHIMENTO
    if renda_anual_global is not None:
        entry_renda.insert(0, str(renda_anual_global))

    entry_dep = ctk.CTkEntry(app, placeholder_text="Dependentes")
    entry_dep.pack(pady=5)

    ctk.CTkButton(
        app,
        text="Calcular",
        fg_color=ROXO,
        hover_color=ROXO_HOVER,
        command=calcular_ir
    ).pack(pady=10)

    # CARD RESULTADO
    card = ctk.CTkFrame(app, fg_color=CINZA, corner_radius=15)
    card.pack(pady=10, padx=20, fill="x")

    resultado = ctk.CTkLabel(
        card,
        text="R$ 0,00",
        font=("Arial", 20, "bold"),
        text_color=BRANCO
    )
    resultado.pack(pady=15)

    frame_grafico = ctk.CTkFrame(app, fg_color=PRETO)
    frame_grafico.pack(fill="both", expand=True, padx=20, pady=10)

    ctk.CTkButton(app, text="⬅ Voltar", command=mostrar_menu).pack(pady=20)


def abrir_calc():
    limpar_tela()

    frame = ctk.CTkFrame(app)
    frame.pack(expand=True)

    ctk.CTkLabel(frame, text="🧮 Calculadora de Renda", font=("Arial", 20)).pack(pady=20)

    global entry_mensal, label_anual

    entry_mensal = ctk.CTkEntry(frame, placeholder_text="Renda mensal")
    entry_mensal.pack(pady=10)

    label_anual = ctk.CTkLabel(frame, text="")
    label_anual.pack(pady=10)

    ctk.CTkButton(
        frame,
        text="Calcular Anual",
        fg_color=ROXO,
        hover_color=ROXO_HOVER,
        command=calc_anual
    ).pack(pady=10)

    ctk.CTkButton(frame, text="⬅ Voltar", command=mostrar_menu).pack(pady=20)

# ================= AÇÕES =================

def calcular_ir():
    try:
        renda = float(entry_renda.get())
        dep = entry_dep.get().strip()
        dependentes = int(dep) if dep != "" else 0

        imposto = calcular_imposto(renda, dependentes)

        resultado.configure(
            text=f"R$ {imposto:,.2f}\nDependentes: {dependentes}"
        )

        salvar_historico(renda, imposto, dependentes)
        mostrar_dashboard(renda, imposto)

    except:
        resultado.configure(text="Erro")


def calc_anual():
    global renda_anual_global

    try:
        mensal = float(entry_mensal.get())
        anual = mensal * 12

        renda_anual_global = anual  # 🔥 salva para auto preencher

        label_anual.configure(text=f"R$ {anual:,.2f}")

    except:
        label_anual.configure(text="Erro")

# ================= DASHBOARD =================

def mostrar_dashboard(renda, imposto):
    for widget in frame_grafico.winfo_children():
        widget.destroy()

    fig, ax = plt.subplots(figsize=(6, 4))

    valores = [renda, imposto]
    labels = ["Renda", "Imposto"]

    cores = ["#8A05BE", "#BBBBBB"]

    bars = ax.bar(labels, valores, color=cores, width=0.5)

    # Fundo dark
    fig.patch.set_facecolor("#121212")
    ax.set_facecolor("#121212")

    # Remove linhas feias
    for spine in ax.spines.values():
        spine.set_visible(False)

    ax.tick_params(colors="white")

    # Título
    ax.set_title("Resumo Financeiro", color="white", fontsize=14)

    # Valores nas barras
    for bar in bars:
        altura = bar.get_height()
        ax.text(
            bar.get_x() + bar.get_width()/2,
            altura,
            f"R$ {altura:,.0f}",
            ha="center",
            color="white",
            fontsize=10
        )

    canvas = FigureCanvasTkAgg(fig, master=frame_grafico)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True)

# ================= UTIL =================

def limpar_tela():
    for w in app.winfo_children():
        w.destroy()

# ================= APP =================

app = ctk.CTk()
app.geometry("900x600")
app.title("Finance Dashboard")

mostrar_menu()

app.mainloop()