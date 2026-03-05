import re
from fastapi import HTTPException

# Regex estrita: SCHEMA.TABELA ou apenas TABELA (somente A-Z, 0-9 e _)
_IDENTIFIER_RE = re.compile(r"^[A-Z][A-Z0-9_]*(\.[A-Z][A-Z0-9_]*)?$")
_BLOCK_TOKENS = ("--", "/*", "*/", "'", ";", " ", "\"")
_BLOCK_KEYS = ("SELECT", "INSERT", "UPDATE", "DELETE", "DROP", "ALTER", "CREATE", "EXECUTE")

def validate_view_name(view_name: str) -> str:
    view_name = view_name.strip().upper()
    for key in _BLOCK_KEYS:
        if key in view_name:
            raise HTTPException(400, f"Nome da view inválido. O token '{key}' não é permitido.")
    for token in _BLOCK_TOKENS:
        if token in view_name:
            raise HTTPException(400, f"Nome da view inválido. O token '{token}' não é permitido.")
    if not _IDENTIFIER_RE.fullmatch(view_name):
        raise HTTPException(400, "Nome da view inválido. Use apenas letras, números e underscores, e opcionalmente um schema (SCHEMA.TABELA).")
    return view_name


# Validação de filiais: deve ser uma string de números inteiros separados por vírgula, sem espaços
# Retorna um lista de strings para uso na query
def validate_filiais(filial: str) -> list[str]:
    filial = filial.strip()
    if not re.fullmatch(r"^\d+(,\d+)*$", filial):
        raise HTTPException(400, "Parâmetro 'filial' inválido. Deve conter apenas números inteiros separados por vírgula, sem espaços. Exemplo: 1,2,3")
    return [f"'{f.strip()}'" for f in filial.split(",")]