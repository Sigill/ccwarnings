#include <string>
#include <iostream>

namespace {
void g() {
}
}

std::string f(const std::string s, int i) {
  try {
    return s + std::to_string(i);
  } catch (const std::exception ex) {
    throw std::runtime_error(ex.what());
  }
}

int main(int argc,
         char ** argv)
{
  std::cout << f(argv[0], 3.14) << std::endl;
  return 0;
}

