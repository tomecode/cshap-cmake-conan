cmake_minimum_required(VERSION 3.23)

set_target_properties(${this_target} PROPERTIES
  DOTNET_SDK "Microsoft.NET.Sdk"
  DOTNET_TARGET_FRAMEWORK "net6.0-windows")

set(CMAKE_DOTNET_SDK "Microsoft.NET.Sdk")
set(CMAKE_DOTNET_TARGET_FRAMEWORK "net6.0-windows")

project(Demo.App LANGUAGES CSharp)

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)

include(CSharpUtilities)

add_executable(${PROJECT_NAME}
  "AppWindow.xaml"
  "AppWindow.xaml.cs"
  "AppEntry.cs"
)

csharp_set_xaml_cs_properties(
  "AppWindow.xaml"
  "AppWindow.xaml.cs"
)

set_target_properties(${PROJECT_NAME} PROPERTIES RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin/$<0:>)
set_source_files_properties("Properties/Resources.resx" PROPERTIES VS_TOOL_OVERRIDE "PublicResXFileCodeGenerator")

set_property(SOURCE "AppEntry.cs" PROPERTY VS_XAML_TYPE "ApplicationDefinition")

set_property(TARGET ${PROJECT_NAME} PROPERTY VS_DOTNET_TARGET_FRAMEWORK_VERSION "v4.7.2")
set_property(TARGET ${PROJECT_NAME} PROPERTY WIN32_EXECUTABLE TRUE)

set(CMAKE_CSharp_FLAGS "/langversion:latest")
set(CMAKE_CSharp_FLAGS "/platform:x64")

set_target_properties(${PROJECT_NAME} PROPERTIES FOLDER "Application")

