import plyplus

# Define la gramática de Kaleidoscope
kaleidoscope_grammar = """
start: expr;

expr: VARIABLE '=' expr
    | expr '+' expr
    | expr '-' expr
    | expr '*' expr
    | expr '/' expr
    | '(' expr ')'
    | NUMBER
    | VARIABLE
    ;

NUMBER: '[0-9]+';
VARIABLE: '[a-zA-Z_][a-zA-Z0-9_]*';
WS: '[ \t\r\n]+' (%ignore);
"""

# Define el traductor de Kaleidoscope a C++
class KaleidoscopeToCppTransformer(plyplus.STransformer):
    def expr(self, expr):
        if len(expr.tail) == 1:  # Es un número o una variable
            return expr.tail[0]
        elif len(expr.tail) == 2:  # Es una operación unaria (por ejemplo, '-' expr)
            return expr.tail[0] + self(expr.tail[1])
        else:  # Es una operación binaria (por ejemplo, expr '+' expr)
            return f"({self(expr.tail[0])} {expr.tail[1]} {self(expr.tail[2])})"

# Función para traducir un archivo de tipo Kaleidoscope a C++
def translate_kaleidoscope_to_cpp(filename):
    with open(filename) as f:
        kaleidoscope_code = f.read()
    
    # Analiza el código Kaleidoscope
    parser = plyplus.Grammar(kaleidoscope_grammar)
    parse_tree = parser.parse(kaleidoscope_code)
    
    # Traduce el código a C++
    transformer = KaleidoscopeToCppTransformer()
    cpp_code = transformer(parse_tree)
    
    return cpp_code

# Ejemplo de uso
if __name__ == "__main__":
    kaleidoscope_file = "input.kd"
    cpp_code = translate_kaleidoscope_to_cpp(kaleidoscope_file)
    print("C++ code:")
    print(cpp_code)
