# utils.py
def rupiah(n: int):
    try:
        return f"Rp{int(n):,}".replace(",", ".")
    except:
        return str(n)