def limpar_e_converter(valor):
    if "%" in valor:
        multiplicador = -1 if "-" in valor else 1
        return (
            multiplicador * float(valor.strip("%").replace(".", "").replace(",", "."))
        ) / 100
    elif "." in valor:
        return float(valor.replace(".", "").replace(",", "."))
    else:
        return float(valor.replace(",", "."))
