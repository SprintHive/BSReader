#!/usr/bin/groovy
@Library('github.com/fabric8io/fabric8-pipeline-library@v2.2.311')
@Library('github.com/SprintHive/sprinthive-pipeline-library@debug')
def utils = new io.fabric8.Utils()
clientsNode{
  def newVersion = ''
  def componentName = 'bsreader'
  def resourcesDir = 'resources/kubernetes'

  checkout scm

  stage('Build and publish docker image') {
      if (!fileExists ('Dockerfile')) {
        throw new Exception('Missing Dockerfile')
      }

      newVersion = publishDockerImage{
        name = componentName
      }
  }

  stage('Rollout to testing') {
    def namespace = 'origination-demo-test'
    def deployStage = 'test'

    def apiObjects = kubeObjectListFromTemplates{
      templates = [
          readFile(resourcesDir + '/deployment.json'),
          readFile(resourcesDir + '/service.json'),
          readFile(resourcesDir + '/ingress-test.json')
      ]
      stage = deployStage
      version = newVersion
      name = componentName
    }

    // Launch Service
    kubernetesApply(file: apiObjects, environment: namespace)
  }
}
