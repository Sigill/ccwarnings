#include <string>
#include <stdexcept>
#include <cstdlib>

namespace {
void useless_function() {}
}

std::string should_pass_by_cref(const std::string s, int i) {
  return s + std::to_string(i);
}

const char* has_notes(int i) {
  static char buf[8];
  snprintf(buf, sizeof(buf), "#%d", i);
  return buf;
}

std::string bad_conversion(int i) {
  const char* buf = has_notes(123456789);
  return should_pass_by_cref(buf, i);
}

std::string should_catch_by_ref() {
  try {
    return bad_conversion(123.456);
  } catch (const std::exception ex) {
    throw std::runtime_error(ex.what());
  }
}
