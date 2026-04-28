def calcular_imposto_anual(renda_anual):
    if renda_anual <= 22847.76:
        return 0
    elif renda_anual <= 33919.80:
        return (renda_anual * 0.075) - 1713.58
    elif renda_anual <= 45012.60:
        return (renda_anual * 0.15) - 4257.57
    elif renda_anual <= 55976.16:
        return (renda_anual * 0.225) - 7633.51
    else:
        return (renda_anual * 0.275) - 10432.32