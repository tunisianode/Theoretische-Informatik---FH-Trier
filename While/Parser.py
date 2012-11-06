import Lexer
import ply.yacc as yacc




#
# A Parser for the While-Language
#
class WhileParser(object):
   
   def __init__(self):
      #Generate the Lexer
      self.lexer = Lexer.WhileLexer(reportError=self.lexicalError)
      
      #
      # Terminial-Tokens from the While-Language
      # PLY need the Tokens  
      #
      self.tokens = self.lexer.grammerTokens
      
      #Generate Parser
      self.parser = yacc.yacc(method="SLR", picklefile = "parsetab.pyc", module = self)
      
    
   #
   # Parse a While-Program
   # return true, if it is a valid program
   #
   def parse(self, programm):
      self.init()
      
   
      #Parse Program
      self.parser.parse(programm, lexer=self.lexer)
   
      #check variables != functions
      intersecVarFunc =  self.variables.intersection(self.functionNamens)
      if intersecVarFunc:
         errStr = [var for var in  intersecVarFunc].__str__().strip("[]")
         self.reportSemantikError(errStr +  " appear(s) as Function and Variable")
      
      
      #check called Functions is subset_eq to declared Functions 
      for func in self.calledFunctions:
         if not func in self.functions:
            self.reportSemantikError( "Function '"+ func[0]+ "' (Argument count:  %i ) is not declared" %func[1])
   
      return not self.errorDetected
         
      
   #
   # Initialise/ Reset the parser
   #             
   def init(self):
       
      self.errorDetected = False
      self.reportContextSensitiveErrors = True
      self.checkLocalDeclaredFlag = False
      self.variables = set([])
      self.functions = set([])
      self.functionNamens = set([])
      self.localDeclaredVariables = set([])
      self.localUsedVariables = set([])
      self.calledFunctions = set([])
      self.params = set([])
      self.argCounter = 0
      self.zeroCounter = 0
      self.lastDeclaredFunction = None



   #
   #Functions for Error-Reporting
   #
   def reportError(self, str, line = None):  
      print("******************************")
      if line:
         print("Line "+ line.__str__() + ":")
      print("")
      try:
         print(str)
      except UnicodeEncodeError as err:
         print(err)
      print("")
      self.errorDetected = True
   
   
   
   def reportSyntaxError(self, str, line = None):
      self.reportError(str, line)
      # do not report semantik-Errors 
      # maybe it's just a problem of bad synchronisation
      self.reportContextSensitiveErrors = False
   
   def reportLexicalError(self, str, line = None):
      self.reportError(str, line)
      # do not report semantik-Errors
      # maybe it's just a problem of bad synchronisation
      self.reportContextSensitiveErrors = False
      
   def reportSemantikError(self, str, line = None):
      if self.reportContextSensitiveErrors:
         self.reportError(str, line)
   
   def lexicalError(self, t):
      errStr = t.lexer.getLinePos(t.lexpos)
      errStr += "Illegal character '%s'" % t.value[0]
      self.reportLexicalError(errStr, t.lineno)

   #########################################################################
   #########################################################################
   # All following Functions are handled by PLY
   # self.tokens is set in the Constructor
   #########################################################################
   #########################################################################
   
     
   def p_error(self, p):
      if p:
         lineno = p.lineno
         value = p.value
         if p.type == "NEWLINE" : 
            value = "NEWLINE"
         
         errStr = p.lexer.getLinePos(p.lexpos)
         if p.type == "DEDENT" and p.lexer.getColumn(p.lexpos) != 0:
            # DEDENT normaly appears behind newline 
            # Otherwise it must be one of the gerenrated  DEDENTs before EOF.
            errStr+="Unexpected token DEDENT or END_OF_FILE"
         else:
            errStr += "Unexpected token '%s'" % value
         self.reportSyntaxError(errStr, lineno)
      else:
         self.reportSyntaxError("Syntax error at EOF")
   
   
   def p_program(self, p):
      '''program : funcdef
                   | funcdef  program'''
      
   
   def p_funcdef(self, p):
      '''funcdef : DEF NAME '(' ')' ':'  funcbody 
                  | DEF NAME '(' paramlist ')' ':' funcbody'''
            
      funcName = p[2]
      
      if self.checkLocalDeclaredFlag:
         # each Variables that is used, must be declared
         notDeclared = (self.localUsedVariables - self.localDeclaredVariables) - self.params
         if notDeclared:
            errStr = [var for var in notDeclared].__str__().strip("[]")
            self.reportSemantikError(errStr+  " is/are used but not declared in function '"+ p[2] + "'", p.lineno(1) ) 
            
         # each Variables that is declared in initlist, must be used
         notUsed =  self.localDeclaredVariables - self.localUsedVariables
         if notUsed:
            errStr = [var for var in notUsed].__str__().strip("[]")
            self.reportSemantikError(errStr+  " is/are declared but not used in function '"+ p[2] + "'", p.lineno(1) )
      
      
      # Declare Function
      if funcName in self.functionNamens:
         self.reportSemantikError( "Multiple declared Function '"+p[2]+ "'", p.lineno(1))
      self.paramCount = len(self.params)
      self.functions.add((funcName, self.paramCount))
      self.lastDeclaredFunction = (funcName, self.paramCount)
      self.functionNamens.add(funcName)
      
      self.params = set([])
      self.localDeclaredVariables = set([])
      self.localUsedVariables = set([])
   
   
       
      
   
   def p_paramlist(self, p):
      '''paramlist : NAME ',' paramlist
                   | NAME'''
      # Variable must be declared only one time
      if p[1] in self.localDeclaredVariables or p[1] in self.params:
         self.reportSemantikError("Multiple declared Variable '" + p[1] + "'", p.lineno(1))
   
     
      # Variable is used in program
      self.variables.add(p[1])
      
      # Variable is declared in namespace
      self.params.add(p[1])
      
      
   def p_initlist(self, p):
      '''initlist : NAME ',' initlist
                   | NAME'''
      # Variable must be declared only one time
      if p[1] in self.localDeclaredVariables or p[1] in self.params:
         self.reportSemantikError("Multiple declared Variable '" + p[1] + "'", p.lineno(1))
      
      
      # Variable is used in program
      self.variables.add(p[1])
      
      # Variable is declared in namespace
      self.localDeclaredVariables.add(p[1])
       
   
   def p_funcbodyWithoutDecl(self, p):
      '''funcbody : NEWLINE INDENT funcstatementlist DEDENT'''
   
      #Do not check if all used variables in this Function are declared 
      self.checkLocalDeclaredFlag = False
   
   
   def p_funcbodyWithDecl(self, p):
      '''funcbody : NEWLINE INDENT '[' initlist ']' '=' '[' zerolist ']'  NEWLINE funcstatementlist DEDENT
                   | NEWLINE INDENT '[' ']' '=' '['  ']' NEWLINE funcstatementlist DEDENT'''
      self.checkLocalDeclaredFlag = True
      
      # length of zerolist must be equal to length of initlist
      if self.zeroCounter != len(self.localDeclaredVariables):
         self.reportSemantikError("Number of values does not match", p.lineno(1))
      
      self.zeroCounter  = 0
       
   
   def p_zerolist(self, p):
      '''zerolist : ZERO
                  | ZERO ',' zerolist'''
      self.zeroCounter += 1
   
   
   def p_returnStatement(self, p):
      '''returnstatement : RETURN expression NEWLINE'''
   
   
   def p_funcStatementList(self, p):
      '''funcstatementlist :  statementlist returnstatement
                           |  returnstatement'''
   
   def p_statement_list(self, p): 
      '''statementlist :  statement statementlist
                        | statement''' 
                        
   def p_statement(self, p):
      '''statement : simplestatement NEWLINE
                  | compoundstatement'''
   
   def p_statement_if(self, p):
      '''compoundstatement : IF condition ':' block
                   | IF condition ':' block  ELSE ':' block''' 
          
   
   def p_statement_while(self, p):
      '''compoundstatement : WHILE condition ':' block ''' 
   
   def p_statement_for(self, p):
      '''compoundstatement : FOR NAME  IN RANGE '(' expression ',' expression ')' ':' block '''
      self.variables.add(p[2]) 
      self.localUsedVariables.add(p[2])
   
   
   def p_statement_assign(self, p):
      '''simplestatement : NAME "=" expression'''
      self.variables.add(p[1])
      self.localUsedVariables.add(p[1])
   
   
   
   
      
   #def p_statement_print(p):
   #   '''simplestatement : print expression'''
   
   
   
   def p_block(self, p):
      '''block : NEWLINE INDENT statementlist DEDENT'''
   
   
   def p_expression_arith(self, p):
      '''expression :  '(' expression '+' expression ')'
                     | '(' expression '-' expression ')' '''
   
       
   
   def p_expression_number(self, p):
      '''expression : NUMBER
                   | ZERO
                   | '-' ZERO
                   | '-' NUMBER'''
      
   
   
                      
   def p_expression_funccall(self, p):
      ''' expression : NAME '(' arglist ')'
                      | NAME '('  ')' '''
      self.calledFunctions.add( (p[1], self.argCounter) )
      self.argCounter = 0
   
   
   def p_expression_name(self, p):
      "expression : NAME"
      self.variables.add(p[1])
      self.localUsedVariables.add(p[1])
   
   def p_arglist(self, p):
      ''' arglist : expression
                 | expression ',' arglist'''
      
      # count the Number of Arguments of Function-Call
      self.argCounter += 1
   
   
   def p_condition(self, p):
      '''condition : '(' condition AND condition ')'   
                     | '(' condition OR condition ')'
                     | '(' expression BOOLOP expression ')'
                     | '(' NOT condition ')' '''
                     
   
   

   
   
   
   
   
   
   








