# Investment Memo Generator - Technical Assessment Project

## Project Overview

You are tasked with building an Investment Memo Generator, a sophisticated platform that helps venture capital analysts create comprehensive investment memos by processing and analyzing multiple startup documents. The system should take in various types of documents (pitch decks, financial models, market research reports, competitive analyses) and produce a structured, well-researched investment memo with proper citations and evidence-based insights.

## Core Functionality

### 1. Document Ingestion & Processing

The system must handle multiple document types:

- **Pitch Decks** (PDF, PPTX): Extract company overview, problem/solution, market size, business model, team info, traction metrics, and funding ask
- **Financial Models** (XLSX, CSV): Parse revenue projections, burn rate, unit economics, CAC/LTV ratios, and growth assumptions
- **Market Research Reports** (PDF): Extract TAM/SAM/SOM data, growth rates, competitive landscape, and industry trends
- **Press Releases & News Articles** (PDF, URLs): Gather external validation, partnership announcements, and market positioning
- **Previous Investor Updates** (PDF, Email): Track historical performance vs. projections

### 2. Multi-Step LLM Analysis Pipeline

The system should perform the following analysis steps, each building on the previous:

#### Step 1: Information Extraction

- Extract all quantitative claims (market size, growth rates, revenue figures)
- Identify all qualitative claims (competitive advantages, team expertise, technology differentiation)
- Map each claim to its source document and specific location (page/slide number)

#### Step 2: Claim Verification & Cross-Reference

- Cross-reference market size claims against uploaded market research
- Verify team backgrounds against LinkedIn data or provided bios
- Check financial projections for internal consistency
- Flag any contradictions between documents

#### Step 3: Competitive Analysis

- Extract competitive positioning from pitch deck
- Compare against market research data
- Identify true differentiators vs. table stakes
- Assess defensibility of competitive moats

#### Step 4: Risk Assessment

- Identify key business risks (market, execution, technology, regulatory)
- Analyze burn rate vs. runway
- Evaluate customer concentration
- Assess scalability challenges

#### Step 5: Investment Thesis Generation

- Synthesize findings into coherent investment thesis
- Generate bull case and bear case scenarios
- Create financial projections sensitivity analysis
- Recommend investment decision with confidence level

### 3. Citation & Evidence Management

Every claim or insight in the generated memo must include:

- Direct link to source document
- Specific page/slide reference
- Confidence score based on evidence strength
- Visual indicator for claims without supporting evidence

### 4. Frontend Requirements

#### Document Management Interface

- Drag-and-drop upload with automatic document type detection
- Document preview with zoom and navigation
- Status indicators for processing progress
- Ability to add manual annotations

#### Analysis Dashboard

- Real-time processing status for each analysis step
- Intermediate results preview
- Ability to adjust analysis parameters
- Option to exclude specific documents from analysis

#### Memo Builder Interface

- Side-by-side view: source documents | generated memo
- Click any statement to see supporting evidence
- Inline editing with AI assistance
- Section templates (Executive Summary, Market Analysis, Team Assessment, etc.)

#### Citation Viewer

- Hover over any claim to see source preview
- Click to navigate to exact location in source document
- Filter view by confidence level
- Export citations in standard formats

#### Collaboration Features

- Comment threads on specific sections
- Version history with diff view
- Share draft memos with team members
- Export to various formats (PDF, Word, Notion)

## Technical Requirements

### Backend Architecture

- **Document Processing Service**: OCR, text extraction, format conversion
- **Vector Database**: Store document chunks with embeddings for semantic search
- **LLM Orchestration Service**: Manage multi-step analysis pipeline
- **Citation Service**: Track claim-to-source mappings
- **Export Service**: Generate formatted outputs

### Data Models

- Document: type, upload_date, processing_status, extracted_content
- Claim: text, source_doc_id, location, confidence_score, verification_status
- Analysis: step_name, input_claims, output_insights, llm_config
- Memo: sections, claims_used, version, export_history

### API Endpoints

- POST /documents/upload
- GET /documents/{id}/status
- POST /analysis/start
- GET /analysis/{id}/progress
- GET /memo/{id}/draft
- PUT /memo/{id}/section
- POST /memo/{id}/export

## Evaluation Criteria

The technical assessment will evaluate:

1. **Document Processing Quality**

   - Accuracy of information extraction
   - Handling of various file formats
   - Performance with large documents

2. **LLM Integration Sophistication**

   - Quality of multi-step reasoning
   - Proper prompt engineering
   - Effective use of context windows
   - Citation accuracy

3. **Frontend User Experience**

   - Intuitive document management
   - Smooth navigation between sources and output
   - Responsive design
   - Real-time updates

4. **System Architecture**

   - Scalability considerations
   - Error handling
   - Security (document privacy)
   - Performance optimization

5. **Code Quality**
   - Clean, maintainable code
   - Proper testing
   - Documentation
   - Following provided tech stack conventions

## Example Use Case

A VC analyst uploads:

1. 30-slide pitch deck for a B2B SaaS startup
2. 3-year financial model spreadsheet
3. Gartner report on the target market
4. TechCrunch articles about competitors

The system should produce a 5-page investment memo containing:

- Executive summary with investment recommendation
- Market analysis with TAM/SAM/SOM breakdown
- Competitive positioning matrix
- Financial analysis with key metrics
- Risk assessment with mitigation strategies
- Each section backed by numbered citations linking to source documents

## Constraints & Considerations

- Assume documents may contain sensitive information - implement appropriate security
- Handle inconsistent or contradictory information gracefully
- Optimize for accuracy over speed (but show progress)
- Design for future extensibility (new document types, analysis modules)
- Consider token limits and implement smart chunking strategies
- Implement caching to avoid redundant LLM calls
