import ply.lex as lex

#
# A Scanner for the While-Language
#
class WhileLexer(lex.Lexer):
    

   #
   # reportError must accept two params: a errorMessage and the lineNumber
   #
   def __init__(self, reportError = None, debug=0, optimize=0, lextab='lextab', reflags=0): 
      self.lexer = lex.lex(debug=debug, optimize=optimize, lextab=lextab, reflags=reflags, module=self)
      self.token_stream = None
      self.reportError = reportError
      
      self.currentLineIndent = 0; 
      self.indentLevel = [0];    
   
   
   def input(self, s):
      # add newline,
      # because the Filter-Method expects a newline at the end of a file 
      s = s + "\n"
      self.lexer.paren_count = 0
      self.lexer.input(s)
      self.token_stream = self._filter( )
      self.inputString = s
   
   # get the next Token   
   def token(self):
      try:
         t = next(self.token_stream)
         return t
      except StopIteration:
         return None
      
   # Calculate the column from a position in the input
   # difference between the last NEWLINE and pos
   def getColumn(self, pos):
      last_nl = self.inputString.rfind('\n', 0, pos)
 
      column = (pos - last_nl) -1
      return column
   
   # get the full line as an String from a position
   def getLine(self, pos):
      last_nl = self.inputString.rfind('\n', 0, pos)
      next_nl = self.inputString.find('\n', pos)
      return self.inputString[last_nl + 1 :next_nl]
   
   # get a string that highlight the position in the line
   # the result is something like: 
   #   "if (x * y):" 
   #   "      ^"
   # "^" highlights the position 
   def getLinePos(self, pos):
      str = self.getLine(pos) + "\n"
      for i in range(0, self.getColumn(pos)):
         str += " "
      str += "^\n"
      return str
      


   #
   #Convert BLANK into DEDENT and INDENT
   #Skip multiple NEWLINES
   #
   def _filter(self):
      tokens = iter(self.lexer.token, None)
      indentSwitch = True
      curIndent = 0
      indentStack = [0]
      newlinePos = 0
      
      for t in tokens:
         t.lexer = self
         if indentSwitch:
            if t.type == "BLANK":     
               curIndent += 1
            elif t.type == "NEWLINE":
               newlinePos = t.lexpos
               curIndent = 0
            else:
               while curIndent < indentStack[len(indentStack) - 1]:
                  indentStack.pop()
                  yield self._new_token("DEDENT", t.lineno, newlinePos + 1, self, "DEDENT")
               if curIndent > indentStack[len(indentStack) - 1]:
                  indentStack.append(curIndent)
                  yield self._new_token("INDENT", t.lineno, newlinePos + 1, self,  "INDENT")
               yield t
               indentSwitch = False     
         else:
            if t.type == "BLANK": pass
            elif t.type == "NEWLINE":
               curIndent = 0
               newlinePos = t.lexpos
               indentSwitch = True
               yield t
            else: yield t
      while 0 < indentStack[len(indentStack) - 1]:
         indentStack.pop()
         yield self._new_token("DEDENT", t.lineno, t.lexpos, self, "DEDENT")

   # Generate a Token
   def _new_token(self, type, lineno, lexpos, lexer, value=None):
      tok = lex.LexToken()
      tok.lexer = lexer
      tok.type = type
      tok.lineno = lineno
      tok.lexpos = lexpos
      if value == None:
         tok.value = type
      else:
         tok.value = value
      return tok

   #########################################################################
   #########################################################################
   # All following Variables and Functions are handled by PLY
   #########################################################################
   #########################################################################
   
   
           
   #
   # Keywords, which are not allowed in While
   # 
   reserved = ('class', 'False', 'finally', 'is', 'None', 
               'continue', 'lambda', 'try', 'True', 
               'from', 'nonlocal', 'del', 'global', 
               'with', 'as', 'elif', 'yield', 'assert', 
               'import', 'pass', 'break', 'except' , 'raise', 'print')
   
   #
   # While-Keywords 
   #
   keywords = {'and':'AND', 'or' :'OR', 'not': 'NOT', 'if':'IF', 'while':'WHILE', 'else':'ELSE',
               'for':'FOR', 'in':'IN', 'range':'RANGE', 'def':'DEF', 'return':'RETURN'
   } 
   
   #
   # Tokens, which appear in the BNF-Grammar
   #
   grammerTokens = tuple(keywords.values()) + ('NAME', 'NUMBER', 'ZERO', 'NEWLINE' , 'INDENT', 'DEDENT', 'BOOLOP')
   
   
   #
   # Tokens, which will be handled by the scanner
   #
   tokens = reserved + grammerTokens + ("BLANK",)
   
   #
   # While-Literals
   #
   literals = ('=', '+', '-', '(', ')', ':', ',', '[' , ']' )
   
   
   #
   # Descrpiton of Comments
   #
   def t_COMMENT(self, t):
      r'\# ([a-zA-Z0-9\ \.,\?!"\'_ \# \( \) / \+ \- \* < > | \{ \} \[ \] = \^ ~ $ % : ;])*'
   
   #
   # Description of Tokens
   #
   def t_NAME(self, t):
      r'[a-zA-Z][a-zA-Z0-9]*'
      if t.value in self.keywords :
         t.type = self.keywords[t.value]
      elif t.value in self.reserved:
         t.type = t.value
      return t
   
   def t_NEWLINE(self, t):
      r'\n'
      t.lexer.lineno += 1
      return t
   
   def t_BLANK(self, t):
      r'\ '
      return t
   
   t_NUMBER = r'([1-9][0-9]*)'
   
   t_ZERO = r'0'
   
   t_BOOLOP = r' >= | <= | < | > | == | !='
 
   
   
   #
   # Error reporting
   #
   def t_error(self, t):
      if self.reportError:
         t.lexer = self
         self.reportError(t)
      else:
         print ("Line " + t.lineno.__str__() + " : Illegal character " + t.value[0])
      self.lexer.skip(1)
   
   

   
  



