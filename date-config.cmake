# DATE_INCLUDE_DIRS   - where to find date/date.h, etc.
# DATE_LIBRARIES      - List of libraries when using date.
# DATE_FOUND          - True if date found.

find_path(DATE_INCLUDE_DIR NAMES date/date.h PATHS ${CONAN_INCLUDE_DIRS_DATE})
find_library(DATE_LIBRARY NAMES ${CONAN_LIBS_DATE} PATHS ${CONAN_LIB_DIRS_DATE})

find_package(CURL REQUIRED)
find_package(OpenSSL REQUIRED)
find_package(Threads)

set(DATE_FOUND TRUE)
set(DATE_INCLUDE_DIRS ${DATE_INCLUDE_DIR})
set(DATE_LIBRARIES ${DATE_LIBRARY} ${CURL_LIBRARIES} ${OPENSSL_LIBRARIES} ${CMAKE_DL_LIBS} Threads::Threads)

message("** FOUND DATE:  ${DATE_LIBRARIES} ${DATE_VERSION_STRING}")

mark_as_advanced(DATE_LIBRARIES DATE_LIBRARY DATE_INCLUDE_DIRS DATE_INCLUDE_DIR)
