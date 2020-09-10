#include <string>
#include <iostream>

namespace {
void g() {
}
}

std::string f(const std::string& s) {
  try {
    return s + s;
  } catch (const std::exception ex) {
    throw std::runtime_error(ex.what());
  }
}

int main(int argc,
         char ** argv)
{
  std::cout << f(argv[0]) << std::endl;
  return 0;
}

