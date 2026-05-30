# Personal Assistant MVP — Requirements v2

## 1. Product Goal

Build a Telegram-based personal assistant platform that can support many future capabilities through a skill-based architecture.

The MVP focuses on one capability: investment research.

The assistant should help a user make better investment decisions by combining:

- Explicit user profile context
- Confirmed portfolio context
- High-quality external research
- Skill-guided reasoning
- Telegram-based interaction
- Saved research artifacts

The MVP should prove that a personal assistant can produce more contextual, evidence-backed investment research than a generic chatbot.

## 2. Core Principles

### 2.1 Separation of Concerns

The application owns:

- User identity
- Telegram integration
- Profile storage and retrieval
- Portfolio storage and retrieval
- Session lifecycle
- Tool access
- Research artifact persistence

The agent owns:

- Planning
- Reasoning
- Research synthesis
- Recommendation generation
- Response generation

Skills own:

- Task-specific instructions
- Research process
- Quality standards
- Output expectations
- Safety boundaries

The core application must not hardcode investment logic.

### 2.2 Skill-Based Extensibility

The system should be extensible by adding new skills.

Future skills may include:

- Deep research
- Shopping recommendations
- Reminders
- Portfolio review
- Proactive monitoring

The MVP implements only one skill:

- Investment Research Skill

The MVP should use one broad Investment Research Skill. The application routes investment-related requests to this skill, and the skill internally handles task types such as single-stock analysis, comparisons, portfolio-aware recommendations, and capital deployment guidance.

The skill may later be split into smaller specialized skills if usage shows a clear quality or maintainability need.

### 2.3 Explicit Profile Only

The MVP must not infer or store user preferences from conversations.

The only durable user preference/context should be explicit profile fields updated or confirmed by the user.

Temporary instructions may be used within a session or request, but must not become long-term memory unless the user explicitly updates their profile.

Examples of what should not be stored:

- User dislikes PSU stocks
- User prefers dividend stocks
- User avoids small caps
- User is aggressive because they asked about risky stocks

### 2.4 Quality Over Speed

Investment research should prioritize quality, traceability, and decision usefulness over response speed.

The system should behave more like a junior investment analyst producing a concise investment brief than a chatbot producing a quick generic summary.

## 3. MVP Scope

The MVP is a Telegram-based personal investment research assistant.

It should support:

- One profile per user
- One portfolio per user
- Explicit profile memory
- Portfolio memory
- Saved research artifacts
- User-controlled temporary session context
- Investment Research Skill
- India and US equities
- High-quality investment research
- Suggested action and confidence
- Evidence-backed compact investment briefs

The MVP should not support user-facing retrieval of prior research artifacts in the first release. Artifacts should still be saved with enough metadata to support future retrieval, refreshes, comparison, and follow-up capability.

## 4. Profile Requirements

The system must store one profile per user.

The profile should contain only explicit, user-confirmed fields.

Required profile fields:

- Base currency
- Primary markets
- Default investment horizon
- Risk style

The system should automatically use the saved explicit profile when producing investment research. Because profile fields are explicit durable context, the bot does not need to ask for confirmation every time before using them.

The system must not infer or fill missing profile fields from conversation.

If profile fields are missing and the user asks for personalized action-oriented research, the assistant should either:

- Ask for the missing profile fields, or
- Offer to proceed with general, non-personalized research

The system may provide general, non-personalized investment research without a completed user profile.

Users may update profile fields through `/profile` or natural language commands such as:

```text
Update my risk style to moderate.
```

Every profile update must be explicit. The bot should confirm the change after updating the profile.

Temporary user instructions may override profile usage for a single request, but must not update durable profile memory.

Example:

```text
Ignore my profile and analyze this generally.
```

## 5. Portfolio Requirements

The system must store one portfolio per user.

The portfolio must be usable as context for investment research.

For MVP, portfolio data may be updated manually in the database. Broker ingestion, CSV upload, and Telegram-based portfolio editing are out of scope.

Before using saved portfolio context in investment research, the bot must show the user the portfolio context it intends to use and ask for confirmation.

For MVP, this confirmation is required every time portfolio context will be used. The system must not silently reuse prior confirmation across requests or sessions.

The confirmation should include relevant holdings or a concise summary when the portfolio is large.

The user must be able to:

- Continue with portfolio context
- Continue without portfolio context
- Cancel the task

Example:

```text
I will use your saved portfolio context:
- TCS: 12 shares
- Infosys: 20 shares
- Apple: 5 shares

This will help assess whether adding TCS increases concentration or improves fit.

Reply "confirm" to continue, "without portfolio" to run without it, or "cancel".
```

## 6. Session Context Requirements

The system must support user-controlled temporary session context.

Sessions are used for:

- Active task state
- Confirmation state
- Temporary task instructions
- Preventing context pollution

Sessions are not used for:

- Durable memory
- Inferred preferences
- Conversational follow-up Q&A
- Carrying old research into new answers automatically

Session behavior:

- User starts a session explicitly.
- User ends a session explicitly.
- Session expires after 45 minutes of inactivity.
- Starting a new session clears or replaces the previous session.
- Session context must not become durable memory.
- Outside an active session, the system should not assume conversational context.

## 7. Telegram Interface Requirements

Telegram is the only user interface for MVP.

The system should support natural language investment requests such as:

```text
Analyze TCS
Should I buy Apple?
Compare Infosys and TCS
I have ₹2 lakh to deploy next week
```

Prior-research retrieval requests such as the following are out of scope for the first MVP release:

```text
What did you say about TCS last time?
```

Minimal commands:

```text
/start
/profile
/portfolio
/start_session
/end_session
```

Natural language should remain the primary interface.

The `/portfolio` command may show saved portfolio context, but portfolio editing through Telegram is out of scope.

## 8. Investment Research Skill Requirements

The MVP must include one broad Investment Research Skill.

This skill should handle investment-related requests, including:

- Single-stock analysis
- Multi-stock comparison
- Portfolio-aware recommendation
- Capital deployment questions

The skill may internally classify the task type, but the application should not hardcode separate investment workflows.

The skill should guide the agent to:

- Understand the user request
- Identify required context
- Ask for missing critical information
- Use explicit profile context when available
- Use portfolio context only after confirmation
- Research current sources
- Separate facts from interpretation
- Produce a suggested action
- Provide confidence
- Cite sources
- Return output suitable for artifact storage

The skill should support India and US equities in MVP.

## 9. Capital Deployment Scope

Capital deployment questions are in scope, but only as research-guided equity deployment guidance.

The Investment Research Skill may help the user evaluate how to deploy a stated amount of capital across India or US equities, using the user’s explicit profile and confirmed portfolio context when available.

The assistant may:

- Compare a small set of candidate equities
- Ask the user to provide or narrow candidate options
- Identify risks
- Suggest whether to buy, hold, avoid, watch, or stage deployment

The assistant must not:

- Perform full portfolio optimization
- Provide tax-aware planning
- Execute trades
- Give precise allocation modeling unsupported by evidence
- Claim to predict short-term price movement

If the request is too broad, the assistant should narrow the task by asking for a market, candidate list, sector, amount, or time horizon.

## 10. Supported Investment Universe

In scope:

- Listed India equities
- Listed US equities
- ADRs, if clearly identified as equity exposure

Out of scope:

- Options
- Futures
- Crypto
- Bonds
- Mutual funds
- Complex ETFs
- Private companies
- Tax-aware recommendations
- Trade execution

If the user asks about an out-of-scope instrument, the assistant should politely narrow the request to listed India or US equity research.

## 11. Evidence-Backed Investment Brief

Completed investment research should return a compact, evidence-backed investment brief to the user.

The brief should be readable in approximately 30-45 seconds while still showing the main data points behind the recommendation.

It should include:

- Investment target
- Suggested action
- Confidence
- Relevant horizon
- Verdict summary
- Signal summary with supporting data points
- Explanation of why the signals lead to the suggested action
- Key risks
- Conditions that would change the view
- Portfolio relevance, when portfolio context is used
- Concise source summary

The assistant must avoid black-box recommendations. Each major positive or negative claim should be tied to a concrete metric, source-backed observation, or clearly stated assumption.

The assistant should avoid long textbook explanations of financial ratios unless the user explicitly asks for educational detail.

Example format:

```text
APL Apollo — Investment Brief

Suggested action: Watch
Confidence: Medium
Horizon: 12+ months

Verdict:
Strong business momentum, but valuation looks demanding. I would not call it an easy buy at current levels unless growth and margins continue improving.

Signal summary:
- Growth: Positive — revenue +13.7% YoY, net profit +20.9% YoY
- Profitability: Mixed — ROE 19.4%, but EBIT margin 4.9%
- Valuation: Expensive — P/E 42.8x vs sector 22.4x; P/B 10.1x vs industry 2.4x
- Balance sheet: Comfortable — interest coverage 9.7x
- Ownership: Positive — institutional holding +1.4% over last 2 quarters

Why this leads to Watch:
The company shows good growth, strong ROE, and manageable debt risk. But valuation is materially above sector averages, and EBIT margin is low. That creates a risk that even a good company may deliver poor returns if bought at too high a price.

Key risks:
- Premium valuation leaves little room for disappointment.
- Low EBIT margin could pressure profits if costs rise.
- Growth needs to remain strong to justify current multiples.

What would change the view:
- Move toward Buy if growth remains strong, margins improve, or valuation cools.
- Move toward Avoid if growth slows, margins weaken further, or valuation remains high without earnings support.

Sources: latest quarterly results, market valuation data, shareholding data
```

The Telegram response should be the investment brief. The saved artifact should contain the full structured research memo behind it.

## 12. Suggested Actions and Confidence

Allowed suggested actions:

- Buy
- Hold
- Avoid
- Watch

Action semantics:

- Buy: Evidence supports accumulation for the stated horizon, with risks acceptable for the user profile.
- Hold: Existing holders may continue holding, but new buying is not strongly supported.
- Avoid: Risk/reward appears unattractive or evidence quality is poor enough to stay away.
- Watch: Interesting but not enough conviction; wait for better price, stronger data, or clearer conditions.

Allowed confidence values:

- Low
- Medium
- High

Confidence semantics:

- High: Multiple reliable current sources support the view; key uncertainties are limited.
- Medium: Evidence is reasonable, but there are meaningful risks, valuation concerns, or incomplete data.
- Low: Evidence is mixed, data is incomplete, or the answer depends heavily on uncertain assumptions.

The assistant should provide Buy, Hold, or Avoid only when the available evidence, user profile, and confirmed portfolio context are sufficient to support that action.

When evidence is mixed, context is incomplete, source freshness is weak, or conviction is low, the assistant should use Watch with Low confidence and clearly explain the uncertainty.

If the request is ambiguous, out of scope, or missing critical information needed even to begin research, the assistant should ask a clarifying question or narrow the request instead of forcing a recommendation.

## 13. Source Quality and Freshness

The assistant should prefer high-quality sources.

Recommended source hierarchy:

- Company filings, annual reports, investor presentations, and earnings releases
- Exchange or regulatory sources such as NSE, BSE, and SEC
- Earnings transcripts or management commentary
- Reputable financial data providers
- Reputable business and market news
- Analyst or media commentary only as supporting evidence

Freshness requirements:

- Market price, valuation, recent performance, earnings, guidance, and news-sensitive claims need fresh or current sources.
- Business model, long-term strategy, and historical context can use older sources if still valid.
- Market-sensitive and financial metrics should include the relevant period, date, or "latest available" qualifier when practical.

The assistant should use available data points and explicitly mark missing or unavailable data. It must not fabricate metrics to fit the brief format.

If fresh data cannot be retrieved, the assistant may provide a limited view, but should not provide a high-confidence action. It should use Watch with Low confidence when useful, or decline to give an action while explaining what data was missing.

## 14. Research Artifact Requirements

The system must save completed investment research outputs as artifacts.

Artifacts are saved so research is not thrown away and can support future:

- Historical lookup
- Refreshes
- Follow-up capability
- Comparison against new research

For the first MVP release, artifacts are not user-retrievable through Telegram.

The system must not use saved artifacts as hidden conversational context.

Each artifact should store:

- User question
- Final answer
- Compact investment brief shown to the user
- Structured analysis sections
- Tickers/entities covered
- Suggested action
- Confidence
- Sources
- Created timestamp

### 14.1 Artifact Save Threshold

The system should save only completed investment research outputs as artifacts.

A response qualifies as a completed research artifact when it includes:

- A clear user question
- Identifiable investment target or entities
- Structured analysis
- Sources
- Suggested action
- Confidence
- Final answer

The system should not save:

- Clarifying questions
- Confirmation prompts
- Profile or portfolio management messages
- Prior-artifact retrieval responses
- Incomplete research drafts
- Casual investment explanations

### 14.2 Artifact Source Metadata

Research artifacts must store structured source metadata rather than only URLs.

Each source should include:

- URL
- Title
- Publisher
- Published date, when available
- Retrieved timestamp
- Short claim summary describing what the source supported

The MVP does not need to store:

- Full source snapshots
- Raw scraped pages
- Full document text
- Document embeddings
- Source version history

## 15. Comparison Output Requirements

For multi-stock comparisons, the assistant should provide a compact side-by-side signal summary and a final preference only if evidence supports it.

The comparison should include relevant dimensions such as:

- Growth
- Profitability
- Valuation
- Balance sheet
- Recent performance
- Key risks
- Portfolio fit, if portfolio context is used

Example:

```text
TCS vs Infosys — Investment Brief

Suggested action: Prefer TCS / Watch both
Confidence: Medium

Signal summary:
- Growth: TCS stronger on recent revenue stability.
- Margins: TCS has better operating resilience.
- Valuation: Infosys looks cheaper on relative multiples.
- Risk: Both remain exposed to US and Europe tech spending.

View:
TCS looks higher quality, but Infosys may offer better valuation support. I would prefer TCS only if valuation is acceptable for the user's horizon; otherwise Watch both.
```

## 16. Portfolio Relevance in Output

If portfolio context is used, the brief must include portfolio relevance.

Example:

```text
Portfolio fit:
You already have 18% IT exposure, so adding TCS would increase sector concentration.
```

If portfolio context is not used, the assistant may say:

```text
Portfolio fit: Not assessed; portfolio context was not used.
```

## 17. Safety and Compliance Boundaries

The assistant may provide educational investment research and suggested actions, but must not:

- Guarantee returns
- Claim certainty
- Tell the user to execute a trade immediately
- Present itself as a licensed financial advisor
- Hide uncertainty
- Recommend out-of-scope instruments
- Perform trade execution

The assistant should avoid "Buy now" style language.

Use:

```text
Suggested action: Buy
```

Avoid:

```text
Buy now
```

The assistant may discuss near-term risks and staged deployment, but should not claim to predict short-term price movement.

## 18. Out of Scope for MVP

The following are out of scope:

- Trade execution
- Broker integration
- Automatic buying or selling
- Broker CSV ingestion
- Portfolio editing through Telegram
- Full web application
- WhatsApp support
- Shopping recommendations
- Reminders
- Proactive monitoring
- Automatic research updates
- User-facing prior research retrieval
- Artifact listing or comparison
- Conversational follow-up on saved research
- Session-based follow-up Q&A
- Complex portfolio optimization
- Tax-aware recommendations
- Options, futures, crypto, bonds, and mutual funds
- Inferred preference memory
- Episodic memory
- Multi-user organization support
- Advanced dashboarding
- Complex artifact versioning
- Fully autonomous agent actions without user confirmation

## 19. High-Level Approach

The MVP should be built as a thin Telegram application that loads user context and delegates reasoning to a skill-driven agent.

High-level flow:

```text
User message
→ Telegram app
→ Identify user
→ Load profile, portfolio, session, and relevant stored data
→ Select Investment Research Skill
→ Confirm portfolio context if portfolio will be used
→ Agent executes skill
→ Agent produces compact brief + structured artifact data
→ App returns brief to user
→ App saves artifact when response meets completed-research threshold
```

Future capabilities should be added by introducing new skills, not by rewriting the core application.

## 20. Deferred Decisions for Implementation Spec

The following should be defined in the implementation spec:

- Data models
- Session state machine
- Telegram handler design
- Skill input/output contract
- Artifact schema
- Source schema
- Portfolio confirmation state
- Tool access policy
- Error and fallback handling
- Test scenarios
