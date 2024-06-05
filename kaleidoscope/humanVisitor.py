from plyplus import STransformer


start: program;

## Generar archivo binario
## Generar archivo hexadecimal
## Soportar directrices " .asciz  "Hola""
program:
  label;

## Debe soportar solamente labels que estén definidos.
label: LABELNAME ':';

inst:
    instr  regname ',' regname ',' regname // R instruction
  | insti  regname ',' regname ',' imm     // I instruction
  | instil regname ',' offset;

offset: imm '\(' regname '\)';

instname: instr | insti;

instr: 'add' | 'sub' | 'xor';
insti: 'addi' | 'xori';
instil: 'lw' | 'lh' | 'lb';

imm : VAL;

VAL: '[0]|(\-|\+)?[1-9][0-9]*';


regname:
   'x0' | ZERO
  | 'x1' | 'ra'
  | 'x2' | 'x3' | 'x4' | 'x5' | 'x6'| 'x7' | 'x8' | 'x9' | 'x10'
  | 'x11' | 'x12' | 'x13' | 'x14' | 'x15' | 'x16'| 'x17' | 'x18' | 'x19' | 'x20'
  | 'x21' | 'x22' | 'x23' | 'x24' | 'x25' | 'x26'| 'x27' | 'x28' | 'x29' | 'x30'
  | 'x31' | 's0' | 'fp'
;

## No está bien!, ejemplos no soportados: ".LBB0_1: "
LABELNAME: '[a-z]+'
  (%unless
    ZERO: 'zero';
    ADD: 'add';
  );

// incluir el numeral como simbolo de comentario
COMMENT: ';' '.*?' (%ignore);
WS: '[ \t\r\n]+' (%ignore);