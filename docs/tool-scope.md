# Tool scope

The six skills query Securin and explain the result. They are not a standing grant to change the platform.

## What the skills call

The skills name search, aggregate, field lookup, and deep link tools. Examples include `searchExposureData`, `searchVulnerabilityData`, `aggregateAssetData`, `getApiFields`, `createDeepLink`, and `getDeepLink`.

`createDeepLink` and `createDeepLinkForView` mint a platform URL for a filter the user already asked to see. They do not change exposure records, asset records, or tickets.

`securin-remediation-guidance` drafts ticket text for the user to copy. The skill tells the agent not to create the ticket.

## Confirmation rule

The remote server can expose tools beyond the six skills. `search_tools` is the discovery tool. This package does not add host permissions and does not preapprove tools.

Do not call a tool that creates, updates, or deletes a platform record unless the user confirms that exact action in the same turn. Deletion, bulk edits, and ticket creation stay in that class. A deep link is not in that class.

If a tool result would send data outside the accounts the signed in user can open, stop and say so.

## What this review could not list

A full tool inventory needs a signed in session. This change did not call the live server with a user token, so it does not claim that every remote tool is read only. The skill files are the boundary this package controls.

## Names

Threat data from Securin is Securin Signals. The score is Risk Index. The API field name remains `riskIndex`.
