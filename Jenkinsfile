@Library('ecdc-pipeline')
import ecdcpipeline.ContainerBuildNode
import ecdcpipeline.ConanPackageBuilder

project = "conan-date"

conan_user = "ess-dmsc"
conan_pkg_channel = "stable"

containerBuildNodes = [
  'centos': ContainerBuildNode.getDefaultContainerBuildNode('centos7'),
  'debian': ContainerBuildNode.getDefaultContainerBuildNode('debian9'),
  'ubuntu': ContainerBuildNode.getDefaultContainerBuildNode('ubuntu1804'),
  'alpine': ContainerBuildNode.getDefaultContainerBuildNode('alpine')
]

packageBuilder = new ConanPackageBuilder(this, containerBuildNodes, conan_pkg_channel)
packageBuilder.defineRemoteUploadNode('centos')

builders = packageBuilder.createPackageBuilders { container ->
  packageBuilder.addConfiguration(container)
}

node {
  checkout scm

  builders['macOS'] = get_macos_pipeline()
  // builders['windows10'] = get_win10_pipeline()
  parallel builders

  // Delete workspace when build is done.
  cleanWs()
}

def get_macos_pipeline() {
  return {
    node('macos') {
      cleanWs()
      dir("${project}") {
        stage("macOS: Checkout") {
          checkout scm
        }  // stage

        stage("macOS: Package") {
          sh "conan create . ${conan_user}/${conan_pkg_channel} \
            --settings date:build_type=Release \
            --options date:shared=False"

          sh "conan create . ${conan_user}/${conan_pkg_channel} \
            --settings date:build_type=Release \
            --options date:shared=True"

          sh "conan create . ${conan_user}/${conan_pkg_channel} \
            --settings date:build_type=Debug \
            --options date:shared=False"

          sh "conan create . ${conan_user}/${conan_pkg_channel} \
            --settings date:build_type=Debug \
            --options date:shared=True"
        }  // stage
      }  // dir
    }  // node
  }  // return
}  // def

def get_win10_pipeline() {
  return {
    node('windows10') {
      // Use custom location to avoid Win32 path length issues
      ws('c:\\jenkins\\') {
      cleanWs()
      dir("${project}") {
        stage("win10: Checkout") {
          checkout scm
        }  // stage

        stage("win10: Package") {
          bat """C:\\Users\\dmgroup\\AppData\\Local\\Programs\\Python\\Python36\\Scripts\\conan.exe \
            create . ${conan_user}/${conan_pkg_channel} \
            --settings date:build_type=Release \
            --options date:shared=True \
            --build=outdated"""
        }  // stage
      }  // dir
      }  // ws
    }  // node
  }  // return
}  // def
