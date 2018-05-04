#include <cstdlib>
#include <iostream>
#include <date/date.h>
#include <date/tz.h>

using namespace date;
using namespace std::chrono;

int main()
{
    // Test we can use date.h
    auto today = year_month_weekday{floor<days>(system_clock::now())};
    std::cout << today << '\n';

    // Test we can use tz.h
    using namespace date;
    using namespace std::chrono;
    auto t = make_zoned(current_zone(), system_clock::now());
    std::cout << t << '\n';

    return EXIT_SUCCESS;
}

