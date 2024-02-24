# cshap-cmake-conan

Sample project demonstrating how to build a C# solution project with CMake and Conan. 
The project itself contains only a single application with one empty WPF window and project dedicated for unit tests.

## Requirements
1. cmake, version: 3.27.7 or higher
2. conan, version: 1.61.0, btw. version 2.0 is not supported in this demo project
3. visual studio, 17
4. .net 4.8

## Project structure

* [src/](src) - root directory for sources
  * [App/](src/App) - demo application with c# and single window
  * [Tests/](src/Tests) - Sample single project for unit tests
* [conanfile.py](conanfile.py) - Conan package file, where all the magic happens for compiling, etc

## How to build
Building this demo project can be done using the following commands:

```bash
cd $projectHome
conan install . --install-folder=build -pr win_profile_x64
conan build . --build-folder=build
```
- During the build phase, the project files are regenerated.
- The entire project is compiled.
- Unit tests are executed.
- To execute unit tests, it may be required to update the path to the current location of Visual Studio in the file: `src/Tests/App/CMakeLists.txt` line: 15

The output of the generated project (solution) will be in the following folder, where the following files will be generated:
```bash
$projectHome/build/
$projectHome/build/Demo.sln
$projectHome/build/....
```