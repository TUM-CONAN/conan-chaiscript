#include <iostream>
#include <chaiscript/chaiscript.hpp>

double function(int i, double j)
{
  return i * j;
}

int main()
{
  chaiscript::ChaiScript chai;
  chai.add(chaiscript::fun(&function), "function");

  double d = chai.eval<double>("function(3, 4.75);");
}

