class CalculatorError(Exception):
    """Alapértelmezett kivétel a számológéphez."""
    pass

class LexicalError(CalculatorError):
    """Érvénytelen karakter vagy felismerhetetlen token esetén."""
    pass

class ParseError(CalculatorError):
    """Szintaktikai hiba (pl. hiányzó zárójel, érvénytelen operátor-sorrend)."""
    pass

class EvaluateError(CalculatorError):
    """Matematikai kiértékelési hiba (pl. nullával való osztás, negativ gyökvonás)."""
    pass