/**
 * Define classes
 *
 */

#include <variant>

struct Shareable
{
  int data;
  int fromPid;
};

/**
 * A variant which can be either empty (monostate), Shareable or an error message (string)
 */
using ShareableVariant = std::variant<std::monostate, Shareable, std::string>;

/**
 * Print value of ShareableVariant (without Newline)
 */
void printVariant(const ShareableVariant &sv)
try
{
  using namespace std;
  if (std::holds_alternative<std::monostate>(sv))
  {
    // Empty
    cout << "(empty)";
  }
  else if (std::holds_alternative<Shareable>(sv))
  {
    // Shareable
    Shareable s = std::get<Shareable>(sv);
    cout << "Shareable data () from pID=" << s.fromPid; // taotodo
  }
  else if (std::holds_alternative<std::string>(sv))
  {
    // Error
    cout << "ERR data (" << std::get<std::string>(sv) << ")";
  }
}
catch (...)
{
  std::cout << RED << "Unable to parse shareable data" << std::endl;
}
