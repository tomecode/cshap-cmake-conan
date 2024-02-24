cmake_minimum_required(VERSION 3.23)
project(Demo LANGUAGES CSharp)

set_target_properties(${this_target} PROPERTIES
  DOTNET_SDK "Microsoft.NET.Sdk"
  DOTNET_TARGET_FRAMEWORK "net6.0-windows")

set(CMAKE_DOTNET_SDK "Microsoft.NET.Sdk")
set(CMAKE_DOTNET_TARGET_FRAMEWORK "net6.0-windows")

option(BUILD_UNIT_TESTS "Run unit tests" OFF)
set(TEST_RESULTS_PATH "${CMAKE_BINARY_DIR}/test_results" CACHE STRING "Tests results path")
file(TO_CMAKE_PATH "${TEST_RESULTS_PATH}" TEST_RESULTS_PATH)

add_subdirectory(App)

enable_testing()
add_subdirectory(Tests)
