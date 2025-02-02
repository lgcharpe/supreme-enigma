# Parliament Summary API Documentation

## Path Parameters

- `{country}`: ISO 3166-1 alpha-2 country code (e.g. 'us', 'uk', 'fr')
- `{date}`: ISO 8601 date format (YYYY-MM-DD)
- `{startDate}`: ISO 8601 date format (YYYY-MM-DD)
- `{endDate}`: ISO 8601 date format (YYYY-MM-DD)
- `{topic}`: Integer ID representing a specific topic

## Query Parameters

- `lang`: ISO 639-1 language code (e.g. 'en', 'fr', 'es')

## Endpoints

```
GET summary/{country}/latest
GET summary/{country}/latest/{topic}
GET summary/{country}/date/{date}
GET summary/{country}/date/{date}/{topic}
GET summary/{country}/period/{startDate}/{endDate}
GET summary/{country}/period/{startDate}/{endDate}/{topic}
GET topics/{country}
```

## Response Objects

### Period Summary response

```json
{
  "summary": "string",          // 100-word overview of the period
  "keyPoliticians": [{
    "name": "string",           // Politician's full name
    "party": "string",          // Political party
    "mainArguments": ["string"] // List of their main points/arguments
  }],
  "disputes": [{
    "topic": "string",          // Subject of disagreement
    "parties": ["string"],      // Parties involved
    "summary": "string"         // Brief description of the dispute
  }],
  "agreements": [{
    "topic": "string",          // Subject of agreement
    "parties": ["string"],      // Parties involved
    "summary": "string"         // Brief description of what was agreed
  }],
  "votingResults": [{
    "motion": "string",         // What was voted on
    "result": "string",         // Outcome of the vote
    "forCount": "integer",      // Number of votes in favor
    "againstCount": "integer"   // Number of votes against
  }],
  "funnyMoments": [{
    "description": "string",    // Description of the humorous event
    "politicians": ["string"]   // Politicians involved
  }],
  "specialEvents": [{
    "type": "string",           // Type of special event
    "description": "string",    // What happened
    "impact": "string"          // Why it matters
  }]
}

### Topic Summary Response

```json
{
  "summary": "string",          // Overview of topic developments
  "keyDecisions": [{
    "date": "string",           // Date of decision
    "description": "string",    // What was decided
    "impact": "string"          // How it affects citizens
  }],
  "currentStatus": {
    "state": "string",           // Current state of the topic
    "lastUpdated": "string"      // When this was last reviewed
  },
  "nextSteps": [{
    "description": "string",     // What's coming next
    "expectedDate": "string"     // When it's expected
  }],
  "publicFeedback": {
    "summary": "string",         // Overview of public response
    "mainConcerns": ["string"]   // List of main public concerns
  }
}
```

### Topics List Response

```json
{
  "topics": [{
    "id": "integer",             // Topic ID
    "name": "string",            // Topic name
    "description": "string",     // Brief description?
  }]
}
```
