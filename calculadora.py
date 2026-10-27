def calcular_imposto_anual(renda: float, dependentes: int = 0) -> float:
    """Calcula o imposto de renda simplificado considerando dedução por dependente."""
    # Dedução anual aproximada por dependente (conforme regra do projeto)
    renda_tributavel = max(0.0, renda - (2275.08 * dependentes))

    if renda_tributavel <= 22847.76:
        return 0.0
    elif renda_tributavel <= 33919.80:
        return (renda_tributavel * 0.075) - 1713.58
    elif renda_tributavel <= 45012.60:
        return (renda_tributavel * 0.15) - 4257.57
    elif renda_tributavel <= 55976.16:
        return (renda_tributavel * 0.225) - 7633.51
    else:
        return (renda_tributavel * 0.275) - 10432.32