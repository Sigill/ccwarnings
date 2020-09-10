#include <string>
#include <iostream>

std::string f(const std::string s) {
  return s + s;
}

int main(int argc,
         char ** argv)
{
  std::cout << f(argv[0]) << std::endl;
  return 0;
}

