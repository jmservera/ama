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
param storageAccountId string
@description('Agent-task poison queue whose message arrivals raise the candidate alert; import-jobs-poison has no producer in source and stays a documented gap.')
param poisonQueueName string = 'agent-tasks-poison'
@description('Separate default-false gate for the poison-queue candidate, additional to the shared approval guard.')
param enablePoisonQueueAlerts bool = false
@description('Separate default-false gate for the AI limit-breach candidate, additional to the shared approval guard.')
param enableAiLimitAlerts bool = false
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

resource agentTasksPoison 'Microsoft.Insights/scheduledQueryRules@2023-03-15-preview' = {
  name: 'alert-${prefix}-agent-tasks-poison'
  location: location
  tags: tags
  properties: {
    displayName: 'Agent task moved to the poison queue'
    description: 'Candidate poison-queue arrival; proposed owner: Digital service owner with the competent task owner, actual appointment pending. Runbook: ${runbookBase}#agent-tasks-poison. Verify StorageQueueLogs ObjectKey and PutMessage before activation; no result is not proof of a healthy queue.'
    severity: 2
    enabled: candidateAlertsEnabled && enablePoisonQueueAlerts
    scopes: [workspaceId]
    evaluationFrequency: 'PT15M'
    windowSize: 'PT15M'
    criteria: {
      allOf: [
        {
          query: 'StorageQueueLogs | where tolower(_ResourceId) startswith tolower("${storageAccountId}") and OperationName == "PutMessage" and StatusText == "Success" and ObjectKey has "/${poisonQueueName}/"'
          timeAggregation: 'Count'
          operator: 'GreaterThan'
          threshold: 0
          failingPeriods: { numberOfEvaluationPeriods: 1, minFailingPeriodsToAlert: 1 }
        }
      ]
    }
    actions: { actionGroups: [actionGroupId] }
  }
}

resource aiLimitBreach 'Microsoft.Insights/scheduledQueryRules@2023-03-15-preview' = {
  name: 'alert-${prefix}-ai-limits'
  location: location
  tags: tags
  properties: {
    displayName: 'AI call, token, budget or expiry limit held'
    description: 'Candidate AI limit breach (calls, tokens, budget, authority expiry); proposed owner: competent task owner and Digital service owner, Finance for budget and price, actual appointment pending. Runbook: ${runbookBase}#ai-limits. Class anchors: ${runbookBase}#ai-limit-calls, ${runbookBase}#ai-limit-tokens, ${runbookBase}#ai-limit-budget, ${runbookBase}#ai-limit-expiry. Console marker is a non-authoritative signal; the assistant ledger is the record. Does not suspend a task or approve limits.'
    severity: 2
    enabled: candidateAlertsEnabled && enableAiLimitAlerts
    scopes: [workspaceId]
    evaluationFrequency: 'PT15M'
    windowSize: 'PT15M'
    criteria: {
      allOf: [
        {
          query: 'ContainerAppConsoleLogs | where Log has "AI_LIMIT_BREACH"'
          timeAggregation: 'Count'
          operator: 'GreaterThan'
          threshold: 0
          failingPeriods: { numberOfEvaluationPeriods: 1, minFailingPeriodsToAlert: 1 }
        }
      ]
    }
    actions: { actionGroups: [actionGroupId] }
  }
}

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
