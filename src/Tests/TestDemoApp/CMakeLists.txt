cmake_minimum_required(VERSION 3.23)

set_target_properties(${this_target} PROPERTIES
  DOTNET_SDK "Microsoft.NET.Sdk"
  DOTNET_TARGET_FRAMEWORK "net6.0-windows")

set(CMAKE_DOTNET_SDK "Microsoft.NET.Sdk")
set(CMAKE_DOTNET_TARGET_FRAMEWORK "net6.0-windows")

project(TestDemoApp LANGUAGES CSharp)

include(CSharpUtilities)

# TODO this path must be config
set(VSTest_EXECUTABLE "c:/Program Files/Microsoft Visual Studio/2022/Community/Common7/IDE/CommonExtensions/Microsoft/TestWindow/vstest.console.exe")

add_library(${PROJECT_NAME} SHARED)
target_sources(${PROJECT_NAME} PRIVATE
  "TestApp.cs"
)

set_target_properties(${PROJECT_NAME} PROPERTIES
  VS_GLOBAL_ROOTNAMESPACE ${PROJECT_NAME}
  VS_GLOBAL_TestProjectType "UnitTest"
  VS_GLOBAL_TreatWarningsAsErrors True
  VS_GLOBAL_PROJECT_TYPES "{429f5d7e-7e16-4f55-85a6-6836a9b1e4e9};{51b9ceb0-146a-4eb1-9dfc-f04d1a184df3}"
  VS_DOTNET_REFERENCES "${VS_DOTNET_REFERENCES}"
  FOLDER "UnitTest"
)

#target dotnet version
set_property(TARGET ${PROJECT_NAME} PROPERTY VS_DOTNET_TARGET_FRAMEWORK_VERSION "v4.7.2")
set_property(TARGET ${PROJECT_NAME} PROPERTY WIN32_EXECUTABLE TRUE)

set(CMAKE_CSharp_FLAGS "/langversion:latest")
set(CMAKE_CSharp_FLAGS "/platform:x64")

# list of used dependencies
set_property(TARGET ${PROJECT_NAME} PROPERTY VS_PACKAGE_REFERENCES "MSTest.TestFramework_3.1.1;xunit.extensibility.execution_2.5.2;MSTest.TestAdapter_3.1.1;Microsoft.NET.Test.Sdk_17.7.2")

add_dependencies(${PROJECT_NAME}
  "Demo.App"
)

add_test(
  NAME ${PROJECT_NAME}
  COMMAND "${VSTest_EXECUTABLE}" "/logger:console;verbosity=normal" "/ResultsDirectory:${TEST_RESULTS_PATH}" "/logger:trx;LogFileName=TestResults.xml" "$<TARGET_FILE:${PROJECT_NAME}>"
)
