start: operacion;

operacion:
  '\(' operacion '\)'
  | '\-' operacion
  |  suma
  | numero ;

suma:  operacion ('\+'| '\-' | '\*' | '/') operacion;

numero: '[0]|((\-|\+)?[1-9][0-9]*)';
WS: '[ ]+' (%ignore);