from calculadora import calcular_imposto_anual
from utils import mostrar_dicas_declaracao

def main():
    print("=== Calculadora de Imposto de Renda ===")

    renda = float(input("Digite sua renda anual (R$): "))
    imposto = calcular_imposto_anual(renda)

    print(f"\n💰 Imposto devido: R$ {imposto:.2f}")

    if imposto > 0:
        print("⚠️ Você deve pagar imposto.")
    else:
        print("✅ Você está isento.")

    mostrar_dicas_declaracao()

if __name__ == "__main__":
    main()