import Parser as Parser
import sys as sys




#
# Open, parse and execute a File
#  and print the Result
#
def executeFile(filename, args):
   try:
      code = open(filename, "r").read()
   except BaseException as err:
      print(err)
      return None
   return executeCode(code, args)
      


#
# Parse and Execute
# and print the Result
#
def executeCode(code, args):
   parser = Parser.WhileParser()
   if parser.parse(code):
      try:
         print("Syntax correct!" )
         arglist = "(" + args.__str__().strip("[]") +")"
         code = code + "\nresult_ = " + parser.lastDeclaredFunction[0].__str__() + arglist
         exec_env = {}
         exec_env["__builtins__"] = { "range" : range }
         exec_env["result_"] = None
         exec(code, exec_env)
         result_ = exec_env["result_"]
         print ("Result : " + result_.__str__())
         return result_
      except TypeError as err:
         print(err.__str__())   
      except NameError as err:
         errMessage =  err.__str__()
         #
         # One of the possible erros is:
         # "global Name 'xy' is not defined" 
         # we do not print 'global', because there are no global variables in While
         #
         if errMessage[0:11] == "global name": 
            errMessage = errMessage[7: __builtins__.len(errMessage)]
         print(errMessage)



# __name__ == __main__ => This module is being run by itself and not 
#                         being imported from another module
if __name__ == '__main__':
   
   #
   # Different implementations
   # for Python 2 and Python 3 compatibility.
   #
   if sys.version_info[0] < 3:
      my_input = raw_input
   else:
      my_input = input
      
   
   
   #
   # Ask user for file and arguments
   # if not included in sys.argv
   #
   if len(sys.argv) <= 1:
      sys.argv.append(my_input("SourceFile : "))
      arg = my_input("Parameter : ")
      argList = arg.split(",")
      if len(argList) == 1:
         if argList[0].strip()!= "":
            sys.argv.append(argList[0])
      else:
         for str in argList:
            sys.argv.append(str)       
       
   
   #
   # Read arguments
   #
   try:
      args = [] 
      for i in range(2,len(sys.argv)):
         args += [int(sys.argv[i])]
   except ValueError:
      print('"'+ sys.argv[i].__str__() + '" is not a vaild Argument')
      exit()     
            
   result_ = executeFile(sys.argv[1], args)
   
         

      




