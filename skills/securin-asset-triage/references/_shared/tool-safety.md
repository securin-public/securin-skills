<!-- Mirrored from skills/_shared/tool-safety.md. Do not edit here — edit the source and run scripts/sync-shared.sh. -->

# Tool safety

Read this before calling Securin MCP tools.

OAuth is the default. Each user signs in as that user. Do not invent, reuse, or print a bearer token, a client secret, or an App Access key.

Query tools and deep links are in scope for the skills. `createDeepLink` and `getDeepLink` only mint a URL.

Do not call a tool that creates, updates, or deletes a platform record unless the user confirms that exact action in the same turn. Ticket text is a draft. Do not create the ticket.

Threat records come from Securin Signals. The score is Risk Index. The API field name remains `riskIndex`.

If no skill fits, use `search_tools` to find a tool by description, then apply the confirmation rule above.
