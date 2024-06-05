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
