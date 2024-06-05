import plyplus

# Define la gramática de Kaleidoscope
kaleidoscopeGrammar = """
start: program;

program: (function | expr)*;

function: 'def' VARIABLE '(' params ')' expr;

params: VARIABLE (',' VARIABLE)*;

expr: VARIABLE '=' expr
    | 'return' expr
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
    | 'for' VARIABLE '=' expr ',' expr ',' expr 'in' expr
    | 'while' expr 'do' expr
    | VARIABLE '(' args ')'
    | '(' expr ')'
    | NUMBER
    | VARIABLE
    ;

args: expr (',' expr)*;

NUMBER: '[0-9]+';
VARIABLE: '[a-zA-Z_][a-zA-Z0-9_]*';
WS: '[ \t\r\n]+' (%ignore);
"""

class KaleidoscopeToCppTransformer(plyplus.STransformer):
    def expr(self, expr):
        if len(expr.tail) == 1:  # Es un número o una variable
            return expr.tail[0]
        elif len(expr.tail) == 2:  # Es una operación unaria o retorno
            if expr.tail[0] == 'return':
                return f"return {self(expr.tail[1])};"
            return expr.tail[0] + self(expr.tail[1])
        elif expr.tail[0] == 'if':  # Es una declaración if
            return f"if ({self(expr.tail[1])}) {{ {self(expr.tail[2])} }} else {{ {self(expr.tail[3])} }}"
        elif expr.tail[0] == 'for':  # Es un bucle for
            return f"for (int {expr.tail[1]} = {self(expr.tail[2])}; {expr.tail[1]} < {self(expr.tail[4])}; {expr.tail[1]} += {self(expr.tail[5])}) {{ {self(expr.tail[7])} }}"
        elif expr.tail[0] == 'while':  # Es un bucle while
            return f"while ({self(expr.tail[1])}) {{ {self(expr.tail[3])} }}"
        elif len(expr.tail) == 3 and expr.tail[1] == '=':  # Es una asignación
            return f"{expr.tail[0]} = {self(expr.tail[2])};"
        elif len(expr.tail) == 3 and expr.tail[1] in ['+', '-', '*', '/', '<', '>', '<=', '>=', '==', '!=']:  # Es una operación binaria
            return f"({self(expr.tail[0])} {expr.tail[1]} {self(expr.tail[2])})"
        elif len(expr.tail) == 2 and expr.tail[1].head == 'args':  # Es una llamada a función
            args = ', '.join(map(self, expr.tail[1].tail))
            return f"{expr.tail[0]}({args})"
        else:  # Es una operación binaria
            return f"({self(expr.tail[0])} {expr.tail[1]} {self(expr.tail[2])})"
    
    def function(self, expr):
        params = ', '.join(expr.tail[2].tail) if len(expr.tail) > 3 else ''
        return f"auto {expr.tail[1]}({params}) {{ {self(expr.tail[-1])} }}"
    
    def program(self, expr):
        return '\n'.join(map(self, expr.tail))

def translateKaleidoscopeToCpp(filename):
    with open(filename) as f:
        kaleidoscope_code = f.read()
    
    # Analiza el código Kaleidoscope
    parser = plyplus.Grammar(kaleidoscopeGrammar)
    try:
        parse_tree = parser.parse(kaleidoscope_code)
    except plyplus.parser.ParseError as e:
        print(f"Error de sintaxis: {e}")
        return ""
    
    # Traduce el código a C++
    transformer = KaleidoscopeToCppTransformer()
    cpp_code = transformer.transform(parse_tree)
    
    return cpp_code

# Ejemplo de uso
if __name__ == "__main__":
    kaleidoscopeFile = "input.kd"
    cppCode = translateKaleidoscopeToCpp(kaleidoscopeFile)
    print("C++ code:")
    print(cppCode)
