# Software Requirements Specification

# Personal Assistant MVP: Investment Research Assistant

## 1. Overview

### 1.1 Purpose

This document describes the software requirements for the MVP version of a personal assistant platform.

The MVP focuses on one capability:

> Investment research through Telegram.

The assistant should help a user make better investment decisions by combining explicit user context, portfolio context, current research, and a skill-guided agent.

The MVP should prove that a personal assistant can produce more useful and contextual investment research than a generic chatbot.

### 1.2 Product Summary

The product is a Telegram-based assistant that can answer investment research questions such as:

- Analyze TCS
- Should I buy Apple?
- Compare Infosys and TCS
- I have ₹2 lakh to deploy next week

The assistant should return a short, evidence-backed investment brief that is readable in 30-45 seconds.

It should also save completed research outputs as structured artifacts for future use, even though user-facing retrieval of past research is not part of the first MVP.

### 1.3 Primary User

The primary user is an individual investor who wants fast but thoughtful investment research.

The user may invest in Indian and US equities and wants the assistant to consider:

- Their explicit investment profile
- Their saved portfolio
- Current market and company data
- Key risks and valuation context

## 2. Goals and Non-Goals

### 2.1 Goals

The MVP must:

- Provide investment research through Telegram.
- Support India and US listed equities.
- Store one explicit profile per user.
- Store one portfolio per user.
- Use profile context automatically when available.
- Use portfolio context only after user confirmation.
- Produce compact, evidence-backed investment briefs.
- Save completed research outputs as artifacts.
- Keep investment logic inside a skill-driven agent layer.
- Avoid inferred or hidden long-term memory.

### 2.2 Non-Goals

The MVP will not support:

- Trade execution
- Broker integration
- CSV portfolio import
- Portfolio editing through Telegram
- WhatsApp
- Web app or dashboard
- Reminders
- Proactive monitoring
- Automatic research refreshes
- Prior research retrieval through Telegram
- Conversational follow-up on saved research
- Tax-aware advice
- Options, futures, crypto, bonds, mutual funds, or complex ETFs
- Multi-user organizations
- Fully autonomous actions without user confirmation

## 3. Product Principles

### 3.1 Thin Application, Smart Agent

The application should manage product concerns:

- Telegram integration
- User identity
- Profile storage
- Portfolio storage
- Session state
- Confirmation state
- Tool access
- Artifact persistence

The agent should manage reasoning concerns:

- Understanding the investment request
- Planning the research
- Selecting useful sources
- Interpreting evidence
- Producing the recommendation
- Writing the investment brief

The Investment Research Skill should manage domain-specific behavior:

- Research process
- Output quality bar
- Safety rules
- Source expectations
- Recommendation standards

The core application must not hardcode investment logic.

### 3.2 Explicit Memory Only

The assistant must only store durable context that the user explicitly provides or confirms.

The assistant must not infer preferences from conversation.

Examples of preferences that must not be stored unless explicitly updated:

- User dislikes PSU stocks
- User prefers dividend stocks
- User avoids small caps
- User is aggressive because they asked about risky stocks

Temporary instructions may affect a single request or active session, but must not become permanent memory.

### 3.3 Quality Over Speed

Investment research should prioritize usefulness, evidence, and traceability over speed.

The assistant should feel like a junior investment analyst producing a concise research brief, not a chatbot giving a generic answer.

## 4. Users and Data

### 4.1 User

Each Telegram user maps to one application user.

The system must identify users through Telegram identity.

### 4.2 Profile

Each user has one profile.

Required profile fields:

- Base currency
- Primary markets
- Default investment horizon
- Risk style

The system should use saved profile context automatically when producing investment research.

The bot does not need to ask for confirmation every time before using profile fields, because these fields are explicit durable memory.

If the profile is missing or incomplete:

- General research may still proceed.
- Personalized action-oriented research should ask for missing fields or offer to continue as general research.

The system must not invent profile defaults.

### 4.3 Portfolio

Each user has one saved portfolio.

The portfolio may be updated manually in the database for MVP.

The system must not use portfolio context silently.

Before using portfolio context, the bot must show the relevant portfolio context and ask for confirmation.

This confirmation is required every time portfolio context is used.

The user must be able to:

- Continue with portfolio context
- Continue without portfolio context
- Cancel the task

## 5. User Experience Requirements

### 5.1 Telegram Interface

Telegram is the only user interface for MVP.

Natural language should be the primary mode of interaction.

Supported examples:

```text
Analyze TCS
Should I buy Apple?
Compare Infosys and TCS
I have ₹2 lakh to deploy next week
```

Minimal commands:

```text
/start
/profile
/portfolio
/start_session
/end_session
```

### 5.2 Session Behavior

Sessions are temporary task containers.

Sessions are used for:

- Active task state
- Confirmation state
- Temporary task instructions
- Preventing context pollution

Sessions are not used for:

- Long-term memory
- Inferred preferences
- Saved research retrieval
- Follow-up Q&A
- Hidden conversation memory

Session rules:

- User starts a session explicitly.
- User ends a session explicitly.
- Session expires after 45 minutes of inactivity.
- Starting a new session replaces the previous session.
- Session context must not become durable memory.

### 5.3 Portfolio Confirmation Flow

When the assistant wants to use portfolio context, it should send a confirmation message before research begins.

Example:

```text
I will use your saved portfolio context:
- TCS: 12 shares
- Infosys: 20 shares
- Apple: 5 shares

This will help assess whether adding TCS increases concentration or improves fit.

Reply "confirm" to continue, "without portfolio" to run without it, or "cancel".
```

For large portfolios, the bot may show a concise summary plus relevant holdings.

## 6. Investment Research Requirements

### 6.1 Investment Research Skill

The MVP must include one broad Investment Research Skill.

The application should route investment-related requests to this skill.

The skill should internally handle:

- Single-stock analysis
- Multi-stock comparison
- Portfolio-aware recommendation
- Capital deployment questions

The application should not hardcode separate investment workflows for these task types.

### 6.2 Supported Markets and Instruments

In scope:

- Listed Indian equities
- Listed US equities
- ADRs, if clearly identified

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

If the user asks about an out-of-scope instrument, the assistant should politely narrow the request to listed Indian or US equity research.

### 6.3 Capital Deployment Questions

Capital deployment questions are in scope, but narrowly.

The assistant may help the user think through how to deploy a stated amount into equities.

The assistant may:

- Ask for missing amount, market, horizon, or candidate list.
- Compare a small set of equity candidates.
- Suggest staged deployment.
- Recommend Buy, Hold, Avoid, or Watch for candidates.

The assistant must not:

- Perform full portfolio optimization.
- Give tax-aware advice.
- Execute trades.
- Produce overly precise allocation models.
- Claim to predict short-term price movement.

Example:

```text
I would not deploy the full ₹2 lakh at once if valuation risk is high. I can compare 3-5 equity candidates and suggest which ones are Buy, Hold, Avoid, or Watch for your horizon.
```

## 7. Investment Brief Requirements

### 7.1 Brief Format

Completed research should return a compact, evidence-backed investment brief.

The brief should be readable in approximately 30-45 seconds.

It should include:

- Investment target
- Suggested action
- Confidence
- Relevant horizon
- Verdict summary
- Signal summary with data points
- Explanation of why the signals lead to the suggested action
- Key risks
- Conditions that would change the view
- Portfolio relevance, when portfolio context is used
- Concise source summary

### 7.2 Evidence Requirement

The brief must not be a black-box recommendation.

Each major positive or negative claim should include:

- A concrete metric
- A source-backed observation
- Or a clearly stated assumption

Avoid unsupported statements like:

```text
The company has strong fundamentals.
```

Prefer:

```text
Growth: Positive — revenue +13.7% YoY, net profit +20.9% YoY.
```

Avoid long textbook explanations of financial ratios unless the user asks for educational detail.

### 7.3 Example Brief

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

## 8. Recommendations and Confidence

### 8.1 Suggested Actions

Allowed actions:

- Buy
- Hold
- Avoid
- Watch

Action definitions:

| Action | Meaning |
|---|---|
| Buy | Evidence supports accumulation for the stated horizon, with risks acceptable for the user profile. |
| Hold | Existing holders may continue holding, but new buying is not strongly supported. |
| Avoid | Risk/reward appears unattractive or evidence quality is poor enough to stay away. |
| Watch | Interesting, but not enough conviction. Wait for better price, stronger data, or clearer conditions. |

The assistant should avoid "Buy now" language.

Use:

```text
Suggested action: Buy
```

Avoid:

```text
Buy now
```

### 8.2 Confidence Levels

Allowed confidence values:

- Low
- Medium
- High

Confidence definitions:

| Confidence | Meaning |
|---|---|
| High | Multiple reliable current sources support the view, and key uncertainties are limited. |
| Medium | Evidence is reasonable, but there are meaningful risks, valuation concerns, or incomplete data. |
| Low | Evidence is mixed, data is incomplete, or the answer depends heavily on uncertain assumptions. |

### 8.3 Minimum Quality Bar

The assistant should provide Buy, Hold, or Avoid only when there is enough evidence.

When evidence is mixed, context is incomplete, source freshness is weak, or conviction is low, the assistant should use:

```text
Suggested action: Watch
Confidence: Low
```

If the request is ambiguous or out of scope, the assistant should ask a clarifying question instead of forcing a recommendation.

## 9. Source Requirements

### 9.1 Source Hierarchy

The assistant should prefer high-quality sources in this order:

1. Company filings, annual reports, investor presentations, earnings releases
2. Exchange or regulatory sources such as NSE, BSE, and SEC
3. Earnings transcripts or management commentary
4. Reputable financial data providers
5. Reputable business and market news
6. Analyst or media commentary as supporting evidence only

### 9.2 Freshness Rules

Fresh or current sources are required for:

- Market price
- Valuation
- Recent performance
- Earnings
- Guidance
- News-sensitive claims

Older sources may be acceptable for:

- Business model
- Long-term strategy
- Historical context

Where practical, metrics should include the relevant period or date.

Example:

```text
Revenue: +13.7% YoY in the latest reported quarter.
```

### 9.3 Missing Data

The assistant must not fabricate metrics.

If a data point is unavailable, the assistant should say so clearly.

Example:

```text
Valuation: Incomplete — P/E is available, but reliable free cash flow data was not found.
```

If fresh data cannot be retrieved, the assistant may provide a limited view, but should not give a high-confidence action.

## 10. Research Artifacts

### 10.1 Artifact Purpose

The system should save completed research artifacts so research is not lost.

Artifacts should support future:

- Historical lookup
- Research refreshes
- Follow-up capability
- Comparison against new research

User-facing artifact retrieval is out of scope for the first MVP.

The system must not use saved artifacts as hidden conversational context.

### 10.2 Artifact Save Rules

Save only completed investment research outputs.

Save when the response includes:

- Clear user question
- Identifiable investment target or entities
- Structured analysis
- Sources
- Suggested action
- Confidence
- Final answer

Do not save:

- Clarifying questions
- Confirmation prompts
- Profile messages
- Portfolio messages
- Prior-artifact retrieval responses
- Incomplete drafts
- Casual investment explanations

### 10.3 Artifact Contents

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

Each source should store:

- URL
- Title
- Publisher
- Published date, when available
- Retrieved timestamp
- Claim summary

The MVP does not need to store:

- Full source snapshots
- Raw scraped pages
- Full document text
- Embeddings
- Source version history

## 11. Architecture Requirements

### 11.1 High-Level Flow

```text
User message
→ Telegram app
→ Identify user
→ Load profile, portfolio, session
→ Select Investment Research Skill
→ Confirm portfolio if portfolio will be used
→ Agent executes research
→ Agent returns investment brief + artifact data
→ App sends Telegram response
→ App saves artifact when eligible
```

### 11.2 Agent Runtime Options

The implementation may use one of several agentic research approaches.

#### Option A: Hermes Agent Runtime

Hermes acts as the research agent runtime.

```text
Telegram app → Hermes agent → Investment Research Skill → structured output
```

Best fit when Hermes is already part of the project and can provide planning, tool use, tracing, retries, and structured outputs.

Hermes should own:

- Research planning
- Tool use
- Skill execution
- Brief generation
- Artifact payload generation

Hermes should not own:

- Telegram identity
- Profile persistence
- Portfolio persistence
- Artifact persistence
- Session lifecycle

#### Option B: OpenAI Agent Runtime

Use an OpenAI agent framework to execute the Investment Research Skill with tools and structured outputs.

Best fit when speed of implementation and managed agent capabilities matter more than custom runtime control.

#### Option C: LangGraph-Style Workflow

Use an explicit graph for the research workflow.

Example:

```text
Parse request → gather sources → analyze metrics → synthesize brief → validate output
```

Best fit when the team wants maximum control, observability, and durable workflow execution.

#### Option D: Deterministic Pipeline + LLM Synthesis

Use a mostly deterministic research pipeline, then ask an LLM to synthesize the brief.

Example:

```text
Classify request → fetch data → validate sources → compute metrics → LLM writes brief → schema validator checks output
```

Best fit when reliability, cost control, and predictable outputs matter most.

### 11.3 Recommended MVP Architecture

For MVP, prefer either:

- Hermes, if it already fits the project runtime, or
- A deterministic research pipeline with LLM synthesis, if predictability is more important.

Avoid a complex multi-agent architecture for the first MVP.

One strong analyst-style agent is enough.

## 12. Safety Requirements

The assistant may provide educational investment research and suggested actions.

The assistant must not:

- Guarantee returns
- Claim certainty
- Tell the user to execute a trade immediately
- Present itself as a licensed financial advisor
- Hide uncertainty
- Recommend unsupported out-of-scope instruments
- Execute trades

The assistant should clearly state uncertainty when evidence is incomplete or mixed.

## 13. Deferred Implementation Details

The following should be defined in the implementation spec:

- Database schema
- Telegram handlers
- Session state machine
- Skill input contract
- Skill output contract
- Artifact schema
- Source schema
- Tool access policy
- Error handling
- Validation rules
- Test scenarios

## 14. Acceptance Criteria

The MVP is acceptable when:

- A Telegram user can ask for investment research.
- The app can load the user’s explicit profile.
- The app can load the user’s saved portfolio.
- Portfolio context is confirmed before use.
- The Investment Research Skill can produce a compact, evidence-backed brief.
- The brief includes data points, suggested action, confidence, risks, and sources.
- Completed research is saved as an artifact.
- Incomplete or ambiguous requests trigger clarifying questions.
- The system does not store inferred preferences.
- The system does not use saved artifacts as hidden memory.
- Out-of-scope instruments are politely rejected or narrowed.

