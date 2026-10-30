param prefix string
param location string
param tags object
param workspaceId string
param appInsightsId string
param actionGroupId string
param iotHubId string
param jobNames array
param monthlyBudget int
param budgetName string
@description('Candidate alerts remain disabled until separately approved signal/owner/threshold verification. Does not approve or activate AI tasks.')
param enableCandidateAlerts bool = false
@description('Non-secret reference to named-human approval of owners, thresholds, windows, recipients and signal verification. No approval is inferred from a nonempty string.')
param approvalReference string = ''

var candidateAlertsEnabled = enableCandidateAlerts && !empty(trim(approvalReference))
var runbookBase = 'https://github.com/jmservera/ama/blob/main/infra/monitoring-runbooks.md'
var iotFailures = [
  { suffix: 'iot-ingress-throttle', metric: 'd2c.telemetry.ingress.sendThrottle' }
  { suffix: 'iot-routing-dropped', metric: 'd2c.telemetry.egress.dropped' }
  { suffix: 'iot-routing-invalid', metric: 'd2c.telemetry.egress.invalid' }
  { suffix: 'iot-routing-orphaned', metric: 'd2c.telemetry.egress.orphaned' }
]

resource jobFailures 'Microsoft.Insights/metricAlerts@2018-03-01' = [for jobName in jobNames: {
  name: 'alert-${jobName}-failed'
  location: 'global'
  tags: tags
  properties: {
    description: 'Candidate failed-execution presence check; proposed owner: Digital service owner, actual appointment pending. Runbook: ${runbookBase}#${endsWith(jobName, '-orch') || endsWith(jobName, '-orchestrator') ? 'job-orchestrator' : endsWith(jobName, '-audit') || endsWith(jobName, '-ledger-verify') ? 'job-ledger' : endsWith(jobName, '-load') || endsWith(jobName, '-import') ? 'job-import' : 'job-auth'}. Verify state dimension before activation.'
    severity: 2
    enabled: candidateAlertsEnabled
    scopes: [resourceId('Microsoft.App/jobs', jobName)]
    evaluationFrequency: 'PT5M'
    windowSize: 'PT15M'
    criteria: {
      'odata.type': 'Microsoft.Azure.Monitor.SingleResourceMultipleMetricCriteria'
      allOf: [
        {
          name: 'failed-execution'
          metricNamespace: 'Microsoft.App/jobs'
          metricName: 'Executions'
          dimensions: [{ name: 'state', operator: 'Include', values: ['Failed'] }]
          operator: 'GreaterThan'
          threshold: 0
          timeAggregation: 'Maximum'
          criterionType: 'StaticThresholdCriterion'
        }
      ]
    }
    actions: [{ actionGroupId: actionGroupId }]
  }
}]

resource iotFailureAlerts 'Microsoft.Insights/metricAlerts@2018-03-01' = [for failure in iotFailures: {
  name: 'alert-${prefix}-${failure.suffix}'
  location: 'global'
  tags: tags
  properties: {
    description: 'Candidate IoT transport failure; proposed owner: Digital service owner, actual appointment pending. Runbook: ${runbookBase}#${failure.suffix}. Missing traffic is not healthy ingestion.'
    severity: 2
    enabled: candidateAlertsEnabled
    scopes: [iotHubId]
    evaluationFrequency: 'PT5M'
    windowSize: 'PT15M'
    criteria: {
      'odata.type': 'Microsoft.Azure.Monitor.SingleResourceMultipleMetricCriteria'
      allOf: [
        {
          name: failure.suffix
          metricNamespace: 'Microsoft.Devices/IotHubs'
          metricName: failure.metric
          operator: 'GreaterThan'
          threshold: 0
          timeAggregation: 'Total'
          criterionType: 'StaticThresholdCriterion'
        }
      ]
    }
    actions: [{ actionGroupId: actionGroupId }]
  }
}]

var workbookContent = replace(
  replace(
    replace(
      replace(loadTextContent('../monitoring-workbook.json'), '__WORKSPACE_ID__', workspaceId),
      '__APP_INSIGHTS_ID__', appInsightsId),
    '__MONTHLY_BUDGET__', string(monthlyBudget)),
  '__BUDGET_NAME__', budgetName)

resource workbook 'Microsoft.Insights/workbooks@2023-06-01' = {
  name: guid(workspaceId, 'monitoring-146-operations')
  location: location
  tags: tags
  kind: 'shared'
  properties: {
    displayName: 'Zava Forward operations - source-only candidate'
    category: 'workbook'
    sourceId: workspaceId
    version: '1.0'
    serializedData: workbookContent
  }
}

output workbookId string = workbook.id
