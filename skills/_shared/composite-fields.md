---
name: apiFieldsComposite
description: Composite list of valid API field paths for COMPOSITE_ASSET, COMPOSITE_EXPOSURE, COMPOSITE_EXPOSURE_VULNERABILITY, and COMPOSITE_EXPOSURE_WEAKNESS entities. Load before constructing FQL filters / sort / groupBy or `Securin__createDeepLink` view payloads when the account is in Composite Mode (default for accounts with `COMPOSITE_ASSET_LIST_VIEW=true`).
compatibility: Reference-only skill. No workflow steps; no MCP tool invocations beyond the listed `Securin__getApiFields` fallback.
allowed-tools:
  - Securin__getApiFields
model_grade: MEDIUM
metadata:
  personas: Security Analyst, RemOps Engineer, SOC Lead
  workflow_category: reference
---
# API Fields — Composite Mode

These are the ONLY valid field paths for **Composite Mode** queries on
this account, refreshed in parallel from the Securin Platform Gateway
at the start of every request. Use them when:

- The account is in Composite Mode (`COMPOSITE_ASSET_LIST_VIEW=true` —
  see "Step 0 — Account Mode" in the system prompt), AND
- The user did NOT explicitly ask for raw / unmerged / source data.

These paths apply to:

- `filters`, `sort`, and field selections in `Securin__assetQuery` /
  `Securin__exposureQuery` calls.
- `view.view.columns[].id` and field paths inside `view.view.filters`
  for `Securin__createDeepLink` when targeting composite entities.

## Hard rules

- If a field path is not listed below, do **not** use it. Do not invent
  or guess paths — pick the closest listed one or omit the field.
- Field paths are entity-scoped to the composite entityTypes
  (`COMPOSITE_ASSET`, `COMPOSITE_EXPOSURE`,
  `COMPOSITE_EXPOSURE_VULNERABILITY`, `COMPOSITE_EXPOSURE_WEAKNESS`).
- Do NOT use source-mode paths (`asset.*` / `exposure.*` without the
  composite prefix) here — those belong in the `apiFieldsSource` skill.

## Fallback

If an entity you need is not listed below — and only then — call
`Securin__getApiFields` once with the right composite `entityType` and
the matching `fetchGroups`
(`COMPOSITE_BUILT_IN,COMPOSITE_MAPPED_ATTRIBUTES_SOURCES,COMPOSITE_USER_MANAGED_ATTRIBUTES_SOURCES`)
to fetch its schema before constructing the query.

---

### COMPOSITE_ASSET
#### Built-in Attributes
  - `compositeAsset.accountId` (STRING)
  - `compositeAsset.compositeAssetDefinition.id` (LONG)
  - `compositeAsset.compositeAssetDefinition.name` (STRING)
  - `compositeAsset.criticality` (INTEGER) — "Asset Criticality"
  - `compositeAsset.discoveryTarget.dueDate` (DATE) — "Discovery Due Date"
  - `compositeAsset.discoveryTarget.dueDateCalculatedUsingField` (STRING)
  - `compositeAsset.discoveryTarget.dueDateCalculatedUsingValue` (DATE)
  - `compositeAsset.discoveryTarget.dueDateCreatedOn` (DATE)
  - `compositeAsset.discoveryTarget.dueDateUpdatedBy` (STRING)
  - `compositeAsset.discoveryTarget.dueDateUpdatedOn` (DATE)
  - `compositeAsset.discoveryTarget.generatedDueDate` (DATE)
  - `compositeAsset.discoveryTarget.isDefaultPolicyUsed` (BOOLEAN)
  - `compositeAsset.discoveryTarget.priority` (STRING) — "Discovery Target Priority"
  - `compositeAsset.discoveryTarget.status` (STRING) — "Discovery Target Status"
  - `compositeAsset.discoveryTarget.targetDays` (INTEGER) — "Discovery Target Days"
  - `compositeAsset.discoveryTarget.userOverriddenDueDate` (DATE)
  - `compositeAsset.firstDiscoveredOn` (DATE) — "Asset First Discovered On"
  - `compositeAsset.firstIngestedOn` (DATE) — "Asset First Ingested On"
  - `compositeAsset.id` (STRING) — "Asset ID"
  - `compositeAsset.identity.id` (STRING)
  - `compositeAsset.identity.name` (STRING)
  - `compositeAsset.identity.value` (STRING)
  - `compositeAsset.identitySourcedFrom` (STRING)
  - `compositeAsset.isOrphaned` (BOOLEAN)
  - `compositeAsset.isUserOverriddenCompositeAsset` (BOOLEAN)
  - `compositeAsset.lastDiscoveredOn` (DATE) — "Asset Last Discovered On"
  - `compositeAsset.lastIngestedOn` (DATE) — "Asset Last Ingested On"
  - `compositeAsset.lastSeenSourceAssetId` (STRING)
  - `compositeAsset.lifeCycleState` (STRING) — "Asset Lifecycle State"
  - `compositeAsset.name` (STRING) — "Asset Name"
  - `compositeAsset.reachability` (ENUM) — "Asset Reachability"
  - `compositeAsset.scores.overallScore` (DOUBLE) — "Asset Score"
  - `compositeAsset.scores.remediationScore` (DOUBLE) — "Asset Remediation Score"
  - `compositeAsset.scores.routingScore` (DOUBLE) — "Asset Routing Score"
  - `compositeAsset.scores.scanScore` (DOUBLE) — "Asset Discover Score"
  - `compositeAsset.scores.scanScoreReferenceDate` (DATE)
  - `compositeAsset.sourceAssetIDs` (STRING) — "Platform Asset ID"
  - `compositeAsset.sourceAssetTags.colorType` (ENUM)
  - `compositeAsset.sourceAssetTags.id` (LONG)
  - `compositeAsset.sourceAssetTags.isLocked` (BOOLEAN)
  - `compositeAsset.sourceAssetTags.name` (STRING) — "Asset Tags"
  - `compositeAsset.sources.connector.definitionID` (STRING) — "Asset Sources"
  - `compositeAsset.sources.connector.instanceID` (LONG) — "Connector ID"
  - `compositeAsset.sources.connector.name` (STRING) — "Connector Name"
  - `compositeAsset.sources.connector.productName` (STRING) — "Connector Product"
  - `compositeAsset.sources.connector.vendorName` (STRING) — "Connector Vendor"
  - `compositeAsset.sources.decommission.decommissionMode` (STRING) — "Decommission Mode"
  - `compositeAsset.sources.decommission.decommissionedBy` (STRING) — "Decommissioned By"
  - `compositeAsset.sources.decommission.decommissionedOn` (DATE) — "Decommissioned On"
  - `compositeAsset.sources.decommission.decommissionedReason` (STRING) — "Decommissioned Reason"
  - `compositeAsset.sources.decommission.preDecommissionLifeCycleState` (STRING)
  - `compositeAsset.sources.decommission.preDecommissionStatus` (STRING)
  - `compositeAsset.sources.isIdentitySourcedFrom` (BOOLEAN)
  - `compositeAsset.sources.lastSeenImportId` (STRING) — "Last Seen Import ID"
  - `compositeAsset.sources.lifeCycle.lastUpdatedOn` (DATE)
  - `compositeAsset.sources.lifeCycle.state` (STRING) — "Source Asset Lifecycle States"
  - `compositeAsset.sources.overriddenCriticality` (INTEGER)
  - `compositeAsset.sources.overriddenReachability` (ENUM)
  - `compositeAsset.sources.sourceAssetId` (STRING)
  - `compositeAsset.status` (STRING) — "Asset Status"
  - `compositeAsset.statusLastUpdatedOn` (STRING)
  - `compositeAsset.timeToScan` (INTEGER) — "Last Scan Interval"
  - `compositeAsset.workspaces.id` (LONG)
  - `compositeAsset.workspaces.name` (STRING) — "Workspaces"
  - `compositeAsset.workspaces.scores.score` (DOUBLE)

#### Built-in Mapped Attributes(Sources)
  - `compositeAsset.sources.mappedAttributes.applicationUrl` (STRING) — "Asset Application URL"
  - `compositeAsset.sources.mappedAttributes.assetType` (STRING) — "Asset Type"
  - `compositeAsset.sources.mappedAttributes.category` (STRING) — "Asset Category"
  - `compositeAsset.sources.mappedAttributes.cloudProperties.accountId` (STRING) — "Asset Cloud Account ID"
  - `compositeAsset.sources.mappedAttributes.cloudProperties.accountName` (STRING) — "Asset Cloud Account Name"
  - `compositeAsset.sources.mappedAttributes.cloudProperties.provider` (STRING) — "Asset Cloud Provider"
  - `compositeAsset.sources.mappedAttributes.cloudProperties.region` (STRING) — "Asset Cloud Region"
  - `compositeAsset.sources.mappedAttributes.cloudProperties.resourceCategory` (STRING) — "Asset Cloud Resource Category"
  - `compositeAsset.sources.mappedAttributes.cloudProperties.resourceId` (STRING) — "Asset Resource ID"
  - `compositeAsset.sources.mappedAttributes.cloudProperties.resourceName` (STRING) — "Asset Resource Name"
  - `compositeAsset.sources.mappedAttributes.cloudProperties.resourceType` (STRING) — "Asset Resource Type"
  - `compositeAsset.sources.mappedAttributes.containerProperties.url` (STRING) — "Asset Container URL"
  - `compositeAsset.sources.mappedAttributes.isCredentialed` (BOOLEAN) — "Is Credentialed Scan"
  - `compositeAsset.sources.mappedAttributes.name` (STRING) — "Source Asset Names"
  - `compositeAsset.sources.mappedAttributes.networkInterfaces.FQDN` (STRING) — "Asset FQDNs"
  - `compositeAsset.sources.mappedAttributes.networkInterfaces.ipv4s` (IP) — "Asset IPv4 Addresses"
  - `compositeAsset.sources.mappedAttributes.networkInterfaces.macAddresses` (STRING) — "Asset MAC Addresses"
  - `compositeAsset.sources.mappedAttributes.networkInterfaces.netbios` (STRING) — "Asset Netbios"
  - `compositeAsset.sources.mappedAttributes.repoProperties.url` (STRING) — "Code Repo URL"
  - `compositeAsset.sources.mappedAttributes.vendorFirstDiscoveredOn` (DATE) — "Asset Vendor First Discovered On"
  - `compositeAsset.sources.mappedAttributes.vendorIdentifier` (STRING)
  - `compositeAsset.sources.mappedAttributes.vendorLastDiscoveredOn` (DATE) — "Asset Vendor Last Discovered On"
  - `compositeAsset.sources.mappedAttributes.vendorStatus` (STRING) — "Asset Vendor Status"

#### User-Managed Attributes(Sources)
  - `compositeAsset.sources.userManagedAttributes.deviceType` (STRING) — "User-Managed Asset Device Types"
  - `compositeAsset.sources.userManagedAttributes.environment` (STRING) — "User-Managed Asset Environments"
  - `compositeAsset.sources.userManagedAttributes.label` (STRING) — "User-Managed Asset Labels"
  - `compositeAsset.sources.userManagedAttributes.location` (STRING) — "User-Managed Asset Locations"
  - `compositeAsset.sources.userManagedAttributes.operatingSystem` (STRING) — "User-Managed Asset OS"
  - `compositeAsset.sources.userManagedAttributes.supportedApplication` (STRING) — "User-Managed Asset Supported Applications"

### COMPOSITE_EXPOSURE
#### Built-in Attributes
  - `compositeExposure.accountId` (STRING) — "Account"
  - `compositeExposure.age` (INTEGER) — "Age in Days"
  - `compositeExposure.articles.articleId` (LONG) — "Article ID"
  - `compositeExposure.assignments.assignedOn` (DATE)
  - `compositeExposure.assignments.assignedTo.assignedOn` (DATE)
  - `compositeExposure.assignments.assignedTo.id` (STRING)
  - `compositeExposure.assignments.assignedTo.name` (STRING)
  - `compositeExposure.assignments.assignedTo.userType` (ENUM)
  - `compositeExposure.assignments.firstAssignedMode` (STRING)
  - `compositeExposure.assignments.isAssigned` (BOOLEAN)
  - `compositeExposure.assignments.ticketingSystemName` (STRING)
  - `compositeExposure.assignments.timeToAssign` (INTEGER)
  - `compositeExposure.compositeAssetId` (STRING)
  - `compositeExposure.description` (STRING) — "Exposure Description"
  - `compositeExposure.firstDiscoveredOn` (DATE) — "First Discovered On"
  - `compositeExposure.firstIngestedOn` (DATE) — "First Ingested On"
  - `compositeExposure.id` (STRING) — "Exposure ID"
  - `compositeExposure.identity.id` (STRING)
  - `compositeExposure.identity.name` (STRING)
  - `compositeExposure.identity.value` (STRING)
  - `compositeExposure.identitySourcedFrom` (STRING)
  - `compositeExposure.isOrphaned` (BOOLEAN)
  - `compositeExposure.lastDiscoveredOn` (DATE) — "Last Discovered On"
  - `compositeExposure.lastIngestedOn` (DATE) — "Last Ingested On"
  - `compositeExposure.lastResolvedOn` (DATE) — "Last Resolved On"
  - `compositeExposure.lastResurfacedOn` (DATE) — "Last Reopened On"
  - `compositeExposure.lastSeenSourceExposureId` (STRING)
  - `compositeExposure.lifeCycleState` (STRING) — "Lifecycle State"
  - `compositeExposure.remediationTarget.dueDate` (DATE) — "Remediation Due Date"
  - `compositeExposure.remediationTarget.dueDateCalculatedUsingField` (STRING)
  - `compositeExposure.remediationTarget.dueDateCalculatedUsingValue` (DATE)
  - `compositeExposure.remediationTarget.dueDateCreatedOn` (DATE)
  - `compositeExposure.remediationTarget.dueDateUpdatedBy` (STRING)
  - `compositeExposure.remediationTarget.dueDateUpdatedOn` (DATE)
  - `compositeExposure.remediationTarget.generatedDueDate` (DATE)
  - `compositeExposure.remediationTarget.isDefaultPolicyUsed` (BOOLEAN)
  - `compositeExposure.remediationTarget.priority` (STRING) — "Remediation Target Priority"
  - `compositeExposure.remediationTarget.status` (STRING) — "Remediation Target Status"
  - `compositeExposure.remediationTarget.targetDays` (INTEGER) — "Remediation Target Days"
  - `compositeExposure.remediationTarget.userOverriddenDueDate` (DATE)
  - `compositeExposure.routingTarget.dueDate` (DATE) — "Routing Due Date"
  - `compositeExposure.routingTarget.dueDateCalculatedUsingField` (STRING)
  - `compositeExposure.routingTarget.dueDateCalculatedUsingValue` (DATE)
  - `compositeExposure.routingTarget.dueDateCreatedOn` (DATE)
  - `compositeExposure.routingTarget.dueDateUpdatedBy` (STRING)
  - `compositeExposure.routingTarget.dueDateUpdatedOn` (DATE)
  - `compositeExposure.routingTarget.generatedDueDate` (DATE)
  - `compositeExposure.routingTarget.isDefaultPolicyUsed` (BOOLEAN)
  - `compositeExposure.routingTarget.priority` (STRING) — "Routing Target Priority"
  - `compositeExposure.routingTarget.status` (STRING) — "Routing Target Status"
  - `compositeExposure.routingTarget.targetDays` (INTEGER) — "Routing Target Days"
  - `compositeExposure.routingTarget.userOverriddenDueDate` (DATE)
  - `compositeExposure.scanSla` (INTEGER)
  - `compositeExposure.scores.cvssV2Score` (DOUBLE) — "CVSS v2"
  - `compositeExposure.scores.cvssV3Score` (DOUBLE) — "CVSS v3"
  - `compositeExposure.scores.cvssV4Score` (DOUBLE) — "CVSS v4"
  - `compositeExposure.scores.remediationScore` (DOUBLE) — "Remediation Score"
  - `compositeExposure.scores.riskIndex` (DOUBLE) — "Risk Index"
  - `compositeExposure.scores.routingScore` (DOUBLE) — "Routing Score"
  - `compositeExposure.scores.score` (DOUBLE) — "Score"
  - `compositeExposure.scores.scoreLevel` (ENUM) — "Score Level"
  - `compositeExposure.sourceExposureIds` (STRING) — "Source Exposure IDs"
  - `compositeExposure.sourceExposureTags.colorType` (ENUM)
  - `compositeExposure.sourceExposureTags.id` (LONG)
  - `compositeExposure.sourceExposureTags.isLocked` (BOOLEAN)
  - `compositeExposure.sourceExposureTags.name` (STRING) — "Tags"
  - `compositeExposure.sources.assignments.assignedOn` (DATE)
  - `compositeExposure.sources.assignments.assignedTo.assignedOn` (DATE) — "Assigned On"
  - `compositeExposure.sources.assignments.assignedTo.id` (STRING)
  - `compositeExposure.sources.assignments.assignedTo.name` (STRING) — "Assigned To"
  - `compositeExposure.sources.assignments.assignedTo.userType` (ENUM)
  - `compositeExposure.sources.assignments.firstAssignedMode` (STRING)
  - `compositeExposure.sources.assignments.isAssigned` (BOOLEAN) — "Is Routed"
  - `compositeExposure.sources.assignments.ticketingSystemName` (STRING)
  - `compositeExposure.sources.assignments.timeToAssign` (INTEGER) — "Time to Route"
  - `compositeExposure.sources.identifiedBy` (STRING)
  - `compositeExposure.sources.identifier` (STRING)
  - `compositeExposure.sources.integration.definitionID` (STRING) — "Exposure Sources"
  - `compositeExposure.sources.integration.instanceID` (LONG)
  - `compositeExposure.sources.integration.name` (STRING) — "Integration Name"
  - `compositeExposure.sources.integration.productName` (STRING)
  - `compositeExposure.sources.integration.vendorName` (STRING)
  - `compositeExposure.sources.isIdentitySourcedFrom` (BOOLEAN)
  - `compositeExposure.sources.lastSeenImportId` (STRING)
  - `compositeExposure.sources.lifeCycle.lastUpdatedOn` (DATE)
  - `compositeExposure.sources.lifeCycle.state` (STRING)
  - `compositeExposure.sources.scores.overrideScoreReason` (STRING)
  - `compositeExposure.sources.scores.score` (DOUBLE)
  - `compositeExposure.sources.scores.scoreLevel` (ENUM)
  - `compositeExposure.sources.scores.userOverriddenScore` (DOUBLE)
  - `compositeExposure.sources.sourceAssetId` (STRING)
  - `compositeExposure.sources.sourceExposureId` (STRING)
  - `compositeExposure.sources.standardizedVendorSeverityScore` (DOUBLE) — "Standardized Vendor Severity Score"
  - `compositeExposure.sources.status` (STRING)
  - `compositeExposure.status` (STRING) — "Status"
  - `compositeExposure.suppressedBy` (STRING)
  - `compositeExposure.suppressedByUserId` (STRING)
  - `compositeExposure.suppressedOn` (DATE)
  - `compositeExposure.suppressedReason` (STRING)
  - `compositeExposure.suppressedUntil` (DATE)
  - `compositeExposure.timeToAssign` (INTEGER)
  - `compositeExposure.timeToRemediate` (INTEGER) — "Time to Remediate"
  - `compositeExposure.timeToRemediateInDays` (INTEGER)
  - `compositeExposure.title` (STRING) — "Title"
  - `compositeExposure.userSuppressedState` (ENUM)
  - `ticketInfo.externalReferenceName` (STRING)
  - `ticketInfo.groupByKey` (STRING)
  - `ticketInfo.groupByValue` (STRING)
  - `ticketInfo.syncErrorInformation.errorCode` (STRING)
  - `ticketInfo.syncErrorInformation.errorMessage` (STRING)
  - `ticketInfo.syncErrorInformation.httpErrorCode` (STRING)
  - `ticketInfo.syncErrorInformation.timeStamp` (STRING)
  - `ticketInfo.ticketAssignedTo` (STRING)
  - `ticketInfo.ticketAssociatedOn` (DATE)
  - `ticketInfo.ticketCreatedDate` (DATE)
  - `ticketInfo.ticketId` (STRING)
  - `ticketInfo.ticketIntegrationId` (STRING)
  - `ticketInfo.ticketLink` (STRING)
  - `ticketInfo.ticketStatus` (STRING)
  - `ticketInfo.ticketSyncConfigId` (INTEGER)
  - `ticketInfo.ticketingSystemAttributes.fieldName` (STRING)
  - `ticketInfo.ticketingSystemAttributes.fieldValue` (STRING)
  - `vulnerabilities.affectedSoftwares.cpe23Uri` (STRING)
  - `vulnerabilities.affectedSoftwares.product` (STRING)
  - `vulnerabilities.affectedSoftwares.productCategories.category` (STRING)
  - `vulnerabilities.affectedSoftwares.vendor` (STRING)
  - `vulnerabilities.baseScore` (DOUBLE) — "Vuln CVSS Base Score"
  - `vulnerabilities.baseSeverity` (STRING) — "Vuln CVSS Base Severity"
  - `vulnerabilities.cvssv2.score` (DOUBLE) — "Vuln CVSSv2 Score"
  - `vulnerabilities.cvssv2.severity` (STRING) — "Vuln CVSSv2 Severity"
  - `vulnerabilities.cvssv2.vector` (STRING) — "Vuln CVSSv2 Vector"
  - `vulnerabilities.cvssv3.score` (DOUBLE) — "Vuln CVSSv3 Score"
  - `vulnerabilities.cvssv3.severity` (STRING) — "Vuln CVSSv3 Severity"
  - `vulnerabilities.cvssv3.vector` (STRING) — "Vuln CVSSv3 Vector"
  - `vulnerabilities.cvssv4.score` (DOUBLE) — "Vuln CVSSv4 Score"
  - `vulnerabilities.cvssv4.severity` (STRING) — "Vuln CVSSv4 Severity"
  - `vulnerabilities.cvssv4.vector` (STRING) — "Vuln CVSSv4 Vector"
  - `vulnerabilities.description` (STRING) — "Vuln Description"
  - `vulnerabilities.epss.lastModifiedDate` (DATE) — "Vuln EPSS Modified Date"
  - `vulnerabilities.epss.percentile` (STRING) — "Vuln EPSS Percentile"
  - `vulnerabilities.epss.probability` (DOUBLE) — "Vuln EPSS Probability"
  - `vulnerabilities.epss.source` (STRING) — "Vuln EPSS Source"
  - `vulnerabilities.exploitCount` (INTEGER)
  - `vulnerabilities.exploits.aliases` (STRING)
  - `vulnerabilities.exploits.attackClassifications` (STRING)
  - `vulnerabilities.exploits.description` (STRING)
  - `vulnerabilities.exploits.family` (STRING)
  - `vulnerabilities.exploits.lastTrendingDate` (DATE)
  - `vulnerabilities.exploits.subType` (STRING)
  - `vulnerabilities.exploits.tags` (STRING)
  - `vulnerabilities.exploits.title` (STRING) — "Exploit Title"
  - `vulnerabilities.exploits.type` (STRING)
  - `vulnerabilities.exploits.viThreatId` (STRING)
  - `vulnerabilities.hasExploit` (BOOLEAN) — "Has Exploit"
  - `vulnerabilities.hasFix` (BOOLEAN)
  - `vulnerabilities.hasMalware` (BOOLEAN) — "Has Malware"
  - `vulnerabilities.hasRansomware` (BOOLEAN) — "Has Ransomware"
  - `vulnerabilities.hasThreat` (BOOLEAN) — "Has Threat"
  - `vulnerabilities.hasThreatActor` (BOOLEAN) — "Has Threat Actor"
  - `vulnerabilities.id` (STRING) — "Vulnerability ID"
  - `vulnerabilities.isCisaKEV` (BOOLEAN) — "Is CISA KEV"
  - `vulnerabilities.isExploitedInTheWild` (BOOLEAN) — "Is Securin KEV"
  - `vulnerabilities.isTrending` (BOOLEAN) — "Is Trending"
  - `vulnerabilities.isWeaponized` (BOOLEAN) — "Is Weaponized"
  - `vulnerabilities.lastModifiedDate` (DATE)
  - `vulnerabilities.lastTrendingDate` (DATE)
  - `vulnerabilities.malwareCount` (INTEGER)
  - `vulnerabilities.malwares.aliases` (STRING)
  - `vulnerabilities.malwares.attackClassifications` (STRING)
  - `vulnerabilities.malwares.description` (STRING)
  - `vulnerabilities.malwares.family` (STRING) — "Ransomware Family"
  - `vulnerabilities.malwares.lastTrendingDate` (DATE)
  - `vulnerabilities.malwares.subType` (STRING)
  - `vulnerabilities.malwares.tags` (STRING)
  - `vulnerabilities.malwares.title` (STRING) — "Malware Title"
  - `vulnerabilities.malwares.type` (STRING)
  - `vulnerabilities.malwares.viThreatId` (STRING)
  - `vulnerabilities.mitreMappings.techniques.domains` (STRING)
  - `vulnerabilities.mitreMappings.techniques.id` (STRING) — "Mitre Technique ID"
  - `vulnerabilities.mitreMappings.techniques.name` (STRING) — "Mitre Technique Name"
  - `vulnerabilities.mitreMappings.techniques.relatedTechniques.id` (STRING) — "Mitre Related Technique ID"
  - `vulnerabilities.mitreMappings.techniques.relatedTechniques.name` (STRING) — "Mitre Related Technique Name"
  - `vulnerabilities.mitreMappings.techniques.relatedTechniques.nature` (STRING) — "Mitre Related Technique Nature"
  - `vulnerabilities.mitreMappings.techniques.relatedTechniques.status` (STRING)
  - `vulnerabilities.mitreMappings.techniques.status` (STRING)
  - `vulnerabilities.mitreMappings.techniques.tactics.domains` (STRING)
  - `vulnerabilities.mitreMappings.techniques.tactics.id` (STRING) — "Mitre Tactic ID"
  - `vulnerabilities.mitreMappings.techniques.tactics.name` (STRING) — "Mitre Tactic Name"
  - `vulnerabilities.mitreMappings.techniques.tactics.status` (STRING)
  - `vulnerabilities.newsArticles.articles.publishedDate` (DATE) — "News Article Published Date"
  - `vulnerabilities.newsArticles.articles.source.name` (STRING) — "News Article Source"
  - `vulnerabilities.newsArticles.articles.source.url` (STRING)
  - `vulnerabilities.newsArticles.articles.title` (STRING) — "News Article Title"
  - `vulnerabilities.prioritizedBy` (STRING)
  - `vulnerabilities.publishedDate` (DATE) — "Vuln Published Date"
  - `vulnerabilities.ransomwareCount` (INTEGER)
  - `vulnerabilities.riskIndex.index` (DOUBLE) — "Vuln Risk Index"
  - `vulnerabilities.riskIndex.severity` (STRING) — "Vuln Risk Index Severity"
  - `vulnerabilities.securinWarnedDate` (DATE)
  - `vulnerabilities.sources.name` (STRING)
  - `vulnerabilities.sources.url` (STRING)
  - `vulnerabilities.tags` (STRING) — "Vuln Tags"
  - `vulnerabilities.threatActors.associatedGroups` (STRING) — "Associated Threat Actors"
  - `vulnerabilities.threatActors.name` (STRING) — "Threat Actor"
  - `vulnerabilities.threats.aliases` (STRING) — "Threat Aliases"
  - `vulnerabilities.threats.attackClassifications` (STRING) — "Attack Classifications"
  - `vulnerabilities.threats.description` (STRING)
  - `vulnerabilities.threats.family` (STRING) — "Threat Family"
  - `vulnerabilities.threats.isVerified` (BOOLEAN)
  - `vulnerabilities.threats.lastModifiedDate` (DATE)
  - `vulnerabilities.threats.lastModifiedMonth` (STRING)
  - `vulnerabilities.threats.lastModifiedYear` (STRING)
  - `vulnerabilities.threats.lastTrendingDate` (DATE)
  - `vulnerabilities.threats.publishedDate` (DATE) — "Threat Published Date"
  - `vulnerabilities.threats.publishedMonth` (STRING) — "Threat Published Month"
  - `vulnerabilities.threats.publishedYear` (STRING) — "Threat Published Year"
  - `vulnerabilities.threats.sources.id` (STRING)
  - `vulnerabilities.threats.sources.lastModifiedDate` (DATE)
  - `vulnerabilities.threats.sources.lastModifiedMonth` (STRING)
  - `vulnerabilities.threats.sources.lastModifiedYear` (STRING)
  - `vulnerabilities.threats.sources.name` (STRING) — "Threat Source Name"
  - `vulnerabilities.threats.sources.publishedDate` (DATE)
  - `vulnerabilities.threats.sources.publishedMonth` (STRING)
  - `vulnerabilities.threats.sources.publishedYear` (STRING)
  - `vulnerabilities.threats.sources.url` (STRING) — "Threat Source Url"
  - `vulnerabilities.threats.subType` (STRING) — "Threat Sub Type"
  - `vulnerabilities.threats.tags` (STRING) — "Threat Tags"
  - `vulnerabilities.threats.title` (STRING) — "Threat Title"
  - `vulnerabilities.threats.type` (STRING) — "Threat Type"
  - `vulnerabilities.threats.verifiedBy` (STRING)
  - `vulnerabilities.threats.viThreatId` (STRING)
  - `vulnerabilities.title` (STRING) — "Vuln Title"
  - `vulnerabilities.weaknesses.id` (STRING)
  - `weaknesses.alternateTerms.description` (STRING)
  - `weaknesses.alternateTerms.term` (STRING)
  - `weaknesses.description` (STRING)
  - `weaknesses.id` (STRING) — "Weakness ID"
  - `weaknesses.likelihoodOfExploit` (STRING)
  - `weaknesses.mitreTop25` (STRING)
  - `weaknesses.modesOfIntroduction.note` (STRING)
  - `weaknesses.modesOfIntroduction.phase` (STRING)
  - `weaknesses.owaspTop10` (STRING)
  - `weaknesses.relatedAttackPatterns.id` (STRING)
  - `weaknesses.relatedWeaknesses.abstraction` (STRING)
  - `weaknesses.relatedWeaknesses.chainId` (STRING)
  - `weaknesses.relatedWeaknesses.id` (STRING)
  - `weaknesses.relatedWeaknesses.nature` (STRING)
  - `weaknesses.relatedWeaknesses.ordinal` (STRING)
  - `weaknesses.relatedWeaknesses.title` (STRING)
  - `weaknesses.relatedWeaknesses.type` (STRING)
  - `weaknesses.relatedWeaknesses.viewId` (STRING)
  - `weaknesses.title` (STRING)
  - `weaknesses.vrs.score` (DOUBLE)
  - `weaknesses.vrs.severity` (STRING)

#### Built-in Mapped Attributes(Sources)
  - `compositeExposure.sources.mappedAttributes.appHttpProperties.httpMethod` (STRING) — "HTTP Method"
  - `compositeExposure.sources.mappedAttributes.appHttpProperties.path` (STRING) — "Path"
  - `compositeExposure.sources.mappedAttributes.appHttpProperties.requestPayload` (STRING) — "Request Payload"
  - `compositeExposure.sources.mappedAttributes.appHttpProperties.responsePayload` (STRING) — "Response Payload"
  - `compositeExposure.sources.mappedAttributes.containerProperties.image` (STRING) — "Container Image"
  - `compositeExposure.sources.mappedAttributes.containerProperties.imageName` (STRING) — "Container Image Name"
  - `compositeExposure.sources.mappedAttributes.containerProperties.imageTag` (STRING) — "Container Image Tag"
  - `compositeExposure.sources.mappedAttributes.dependencyProperties.dependency` (STRING) — "Dependency"
  - `compositeExposure.sources.mappedAttributes.dependencyProperties.licenseName` (STRING) — "License Name"
  - `compositeExposure.sources.mappedAttributes.dependencyProperties.purl.name` (STRING) — "Dependency Package Name"
  - `compositeExposure.sources.mappedAttributes.dependencyProperties.purl.namespace` (STRING)
  - `compositeExposure.sources.mappedAttributes.dependencyProperties.purl.qualifiers` (STRING)
  - `compositeExposure.sources.mappedAttributes.dependencyProperties.purl.scheme` (STRING)
  - `compositeExposure.sources.mappedAttributes.dependencyProperties.purl.subpath` (STRING)
  - `compositeExposure.sources.mappedAttributes.dependencyProperties.purl.type` (STRING) — "Dependency Package Type"
  - `compositeExposure.sources.mappedAttributes.dependencyProperties.purl.version` (STRING) — "Dependency Package Version"
  - `compositeExposure.sources.mappedAttributes.description` (STRING) — "Description"
  - `compositeExposure.sources.mappedAttributes.diskPaths` (STRING) — "Diskpaths"
  - `compositeExposure.sources.mappedAttributes.exposureUrl` (STRING) — "Exposure URL"
  - `compositeExposure.sources.mappedAttributes.installedSoftware.endOfSupport` (STRING)
  - `compositeExposure.sources.mappedAttributes.installedSoftware.endOfSupportDate` (STRING) — "End of Support Date"
  - `compositeExposure.sources.mappedAttributes.installedSoftware.endOfSupportStatus` (STRING) — "End of Support Status"
  - `compositeExposure.sources.mappedAttributes.installedSoftware.name` (STRING) — "Installed Software Name"
  - `compositeExposure.sources.mappedAttributes.installedSoftware.vendor` (STRING) — "Installed Software Vendor"
  - `compositeExposure.sources.mappedAttributes.installedSoftware.version` (STRING) — "Installed Software Version"
  - `compositeExposure.sources.mappedAttributes.port` (INTEGER) — "Port"
  - `compositeExposure.sources.mappedAttributes.protocol` (STRING) — "Protocol"
  - `compositeExposure.sources.mappedAttributes.registryPaths` (STRING) — "Registry Paths"
  - `compositeExposure.sources.mappedAttributes.service` (STRING) — "Service"
  - `compositeExposure.sources.mappedAttributes.sourceCode.codeSnippet` (STRING) — "Code Snippet"
  - `compositeExposure.sources.mappedAttributes.sourceCode.columnNumber` (DOUBLE) — "Column Number"
  - `compositeExposure.sources.mappedAttributes.sourceCode.endLineNumber` (STRING) — "End Line Number"
  - `compositeExposure.sources.mappedAttributes.sourceCode.fileName` (STRING) — "Filename"
  - `compositeExposure.sources.mappedAttributes.sourceCode.filePath` (STRING) — "Exposure File Path"
  - `compositeExposure.sources.mappedAttributes.sourceCode.programmingLanguage` (STRING) — "Programming Language"
  - `compositeExposure.sources.mappedAttributes.sourceCode.startLineNumber` (STRING) — "Start Line Number"
  - `compositeExposure.sources.mappedAttributes.sourceRepo.branchName` (STRING) — "Branch Name"
  - `compositeExposure.sources.mappedAttributes.title` (STRING)
  - `compositeExposure.sources.mappedAttributes.type` (STRING) — "Exposure Type"
  - `compositeExposure.sources.mappedAttributes.vendorFirstDiscoveredOn` (DATE) — "Vendor First Discovered On"
  - `compositeExposure.sources.mappedAttributes.vendorIdentifier` (STRING) — "Exposure Vendor Identifier"
  - `compositeExposure.sources.mappedAttributes.vendorLastDiscoveredOn` (DATE) — "Vendor Last Discovered On"
  - `compositeExposure.sources.mappedAttributes.vendorRemediation` (STRING) — "Vendor Remediation"
  - `compositeExposure.sources.mappedAttributes.vendorResolvedOn` (DATE) — "Vendor Resolved On"
  - `compositeExposure.sources.mappedAttributes.vendorSeverity` (STRING) — "Vendor Severity"
  - `compositeExposure.sources.mappedAttributes.vendorSeverityList` (STRING)
  - `compositeExposure.sources.mappedAttributes.vendorStatus` (STRING) — "Vendor Status"
  - `compositeExposure.sources.mappedAttributes.vendorSuppressedState` (STRING) — "Vendor Suppressed State"
  - `compositeExposure.sources.mappedAttributes.vulnerabilityIds` (STRING) — "Vendor Vulnerability ID"
  - `compositeExposure.sources.mappedAttributes.weaknessIds` (STRING) — "Vendor Weakness ID"

#### User-Managed Attributes(Sources)
  - `compositeExposure.sources.userManagedAttributes.operatingSystem` (STRING) — "User-Managed Exposure OS"
  - `compositeExposure.sources.userManagedAttributes.patchGroup` (STRING) — "User-Managed Exposure Patch Group"
  - `compositeExposure.sources.userManagedAttributes.shortDescription` (STRING) — "User-Managed Exposure Short Description"

### COMPOSITE_EXPOSURE_VULNERABILITY
### COMPOSITE_EXPOSURE_WEAKNESS

---

_Field paths above were rendered from the on-disk cache at
`dynein/data/apiFields/*_apiFields.json`, which is refreshed in the
background after every request._
