import plyplus

# Define la gramática de Kaleidoscope
kaleidoscope_grammar = """
start: expr;

expr: VARIABLE '=' expr
    | expr '+' expr
    | expr '-' expr
    | expr '*' expr
    | expr '/' expr
    | expr '<' expr
    | expr '>' expr
    | expr '<=' expr
    | expr '>=' expr
    | expr '==' expr
    | expr '!=' expr
    | 'if' expr 'then' expr 'else' expr
    | 'for' VARIABLE '=' expr ',' expr ',' expr 'in' expr 'do' expr
    | 'while' expr 'do' expr
    | 'def' VARIABLE '(' params ')' '->' expr
    | VARIABLE '(' args ')'
    | '(' expr ')'
    | NUMBER
    | VARIABLE
    ;

params: VARIABLE (',' VARIABLE)*;
args: expr (',' expr)*;

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
        elif expr.tail[0] == 'if':  # Es una declaración if
            return f"if ({self(expr.tail[1])}) {{ {self(expr.tail[2])} }} else {{ {self(expr.tail[3])} }}"
        elif expr.tail[0] == 'for':  # Es un bucle for
            return f"for ({self(expr.tail[1])}; {self(expr.tail[2])}; {self(expr.tail[3])}) {{ {self(expr.tail[6])} }}"
        elif expr.tail[0] == 'while':  # Es un bucle while
            return f"while ({self(expr.tail[1])}) {{ {self(expr.tail[3])} }}"
        elif expr.tail[0] == 'def':  # Es una declaración de función
            params = ', '.join(expr.tail[2].split(',')) if len(expr.tail) > 4 else ''
            return f"auto {expr.tail[1]}({params}) {{ return {self(expr.tail[-1])}; }}"
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
