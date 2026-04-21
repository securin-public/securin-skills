# Correlation Patterns

Reference templates for common threat-correlation questions. Each pattern assumes Step 0 preflight has already resolved the account-id and composite-vs-source model.

## Pattern 1 — "Am I affected by CVE-X?"

```text
1. searchVulnerabilityData
   filter: vulnerabilityId = 'CVE-X'
   → fetch KEV status, severity, exploits

2. hybridExposureData
   filter: exposure.mappedAttributes.vulnerabilityIds = 'CVE-X'
           AND exposure.status = 'Open'
   groupByField: "exposure.scores.scoreLevel"
   → count + severity breakdown

3. searchExposureData
   filter: same as above
   → itemize each exposure (capped, e.g., top 25 by severity)

4. searchAssetData (or searchCompositeAssetData)
   filter: asset.assetId = <id from step 3>  # or 'in' for a list
   → asset context

5. createDeepLink per affected asset + top-level filter link
```

## Pattern 2 — "Am I affected by [ransomware family]?"

```text
1. **Web search** for the ransomware family (e.g., "LockBit CVE list", "Clop ransomware CVE")
   → collect CVE IDs from published threat-intel reports (Unit42, Mandiant, CISA advisories)
   → confirm the CVE list with the user before correlating
   

2. hybridExposureData
   filter: exposure.mappedAttributes.vulnerabilityIds in [<cve-list>]
           AND exposure.status = 'Open'
   groupByField: "exposure.scores.scoreLevel"

3-5. As Pattern 1 steps 3-5
```

## Pattern 3 — "Am I affected by [threat actor]?"

```text
1. searchThreatActorData
   filter: name like '<actor>'          # bare path — no `threatActor.` prefix
   fields: ['threatActor']
   → gather actor record + cveIds array
   → ALSO gather TTPs if present

2-5. As Pattern 2 steps 2-5

6. Web search for ATT&CK mapping — Use web search for MITRE ATT&CK data.
```

## Pattern 4 — "Show me exposures to CISA KEV in my prod env"

```text
hybridExposureData
filter: exposure.status = 'Open'
        AND vulnerabilities.exploitation.isCisaKev = true
        AND exposure.workspaceId in [<prod-ws-ids>]
groupByField: "exposure.scores.scoreLevel"
aggs: [{type: "count"}]
```

## Pattern 5 — "What hunts my environment" (outbound)

```text
1. aggregateExposureData
   groupByField: "exposure.mappedAttributes.vulnerabilityIds"
   filter: exposure.status = 'Open' AND "<scope>"
   → list of CVEs with exposure counts in your env

2. For top N CVEs by exposure count, in parallel:
   - searchVulnerabilityData (CVE record)
   - searchThreatActorData (actors exploiting it), fields: ["threatActor"]
   - **Web search** (ransomware/malware → CVE list)

3. Aggregate by threat actor / ransomware family:
   Which actors/families map to the most CVEs in your env?
   Rank by # affected assets (join back via exposures → assets).
```

## Pattern 6 — "Am I vulnerable to the latest news-worthy CVE?"

User says "the Fortinet thing from last week" — no CVE ID.

```text
1. Web search to resolve the event to a CVE list.
   Ask user to confirm before proceeding.

2. For each confirmed CVE, run Pattern 1.

3. Consolidated report covering all CVEs from the event.
```

## Pattern 7 — "Net open exposures to exploited vulns, over time"

Time-series correlation for trending:

```text
hybridVulnerabilityTimelineData
filter: vulnerabilities.exploitation.exploitedInWild = true
        AND exposure.status = 'Open'
groupByField: "exposure.firstSeenAt"   # or exposure.state for new/closed
aggs: [{type: "count", interval: "week"}]
```

## Anti-patterns to avoid

- **Starting a correlation without a resolved account-id** — CC-1 preflight first, always.
- **Forgetting `fields: ["threatActor"]` / `fields: ["threat"]`** — returns empty rows silently.
- **Hand-constructing URLs** instead of `createDeepLink`.
- **Mixing `asset.*` and `compositeAsset.*`** in one query — pick one per account.
- **Blindly iterating all CVEs for a prolific threat actor** — batch, or prioritize by KEV / exploitedInWild first.
