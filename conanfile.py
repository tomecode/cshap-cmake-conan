from conans import ConanFile, CMake, tools
from conans.tools import load
import os
import xml.etree.ElementTree as ET


class GseLibConan(ConanFile):
    name = "demo"
    author = "Demo from Tome"
    description = "C# demo with CMAKE and Conan"
    settings = "os", "compiler", "build_type", "arch"
    generators = "cmake"
    exports_sources = ["src/*"]


    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def append_elemnet_to_xml(sefl, root, element_name, element_value):
        existing_elements = root.findall(element_name)
        if not existing_elements:
            use_wpf_element = ET.Element(element_name)
            use_wpf_element.text = element_value
            root.append(use_wpf_element)
            root[-1].tail = "  \n"
        else:
            existing_elements[0].text = element_value

    def customize_csproj(self, csproj_file_path):
        # In *csproj enable all required .net functions
        tree = ET.parse(csproj_file_path)
        root = tree.getroot()

        for project in root.findall(".//PropertyGroup[@Label='Globals']"):
            self.append_elemnet_to_xml(project, 'UseWPF', 'true')
            self.append_elemnet_to_xml(project, 'UseWindowsForms', 'true')
            self.append_elemnet_to_xml(project, 'GenerateAssemblyInfo', 'false')
            self.append_elemnet_to_xml(project, 'AppendTargetFrameworkToOutputPath', 'false')

        # Configure the entry(main) class
        if csproj_file_path.endswith("Demo.App.csproj"):
            # Fix: https://learn.microsoft.com/en-us/dotnet/core/compatibility/sdk/6.0/outputtype-not-set-automatically
            self.append_elemnet_to_xml(project, 'OutputType', 'WinExe')
            self.append_elemnet_to_xml(project, 'DisableWinExeOutputInference', 'true')

            if not root.findall(".//PropertyGroup/StartupObject"):
                root.append(
                    ET.fromstring('<PropertyGroup><StartupObject>Demo.AppEntry</StartupObject></PropertyGroup>'))

        tree.write(csproj_file_path, encoding='UTF-8', xml_declaration=True)

    def customize_csprojs(self):
        # Adds additional parameters required by c#/.net
        for root, _, files in os.walk(self.source_folder):
            for file in files:
                if file.endswith(".csproj"):
                    csproj_file_path = os.path.join(root, file)
                    self.customize_csproj(csproj_file_path)
                    print(f"Modified {csproj_file_path}")

    def transfer_dll_to_product_location(self, csproj_file_path, libraries):
        # Add command in the csproj file to copy the dll to the product location
        tree = ET.parse(csproj_file_path)
        root = tree.getroot()

        for dll_file_path in libraries:
            template = '<ItemGroup><Content Include="' + dll_file_path + '"><Pack>true</Pack><CopyToOutputDirectory>Always</CopyToOutputDirectory></Content></ItemGroup> '
            xml_element = ET.fromstring(template)
            root.append(xml_element)
            root[-1].tail = "  \n"

        tree.write(csproj_file_path, encoding='UTF-8', xml_declaration=True)

    def build(self):
        cmake = CMake(self)
        if os.environ.get("TEST_RESULTS_PATH"):
            cmake.definitions["TEST_RESULTS_PATH"] = os.path.normpath(os.environ["TEST_RESULTS_PATH"])

        self.customize_csprojs()

        cmake.configure(source_folder="src")

        self.customize_csprojs()

        cmake.build()

        cmake.definitions["BUILD_UNIT_TESTS"] = True
        cmake.test()


    def imports(self):
        # needed to copy transitive dll dependencies to bin for
        # (e.g. for unittest to be able to runs)
        self.copy("*-dotnet.dll", dst="")

    def package(self):
        self.copy("*.dll", dst="bin", keep_path=False, excludes="*test*")

        if self.settings.arch == "x86_64":
            arch_deps = "bin/x64"
        elif self.settings.arch == "x86":
            arch_deps = "bin/x86"
        else:
            arch_deps = None
        self.copy("*.dll", dst="bin", src=arch_deps, keep_path=False)
        self.copy("*.exe", dst="bin", keep_path=False, excludes="*test*")
        self.copy("*.exe.config", dst="bin", keep_path=False)

