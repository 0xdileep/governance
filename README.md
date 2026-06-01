# AI Governance Middleware - Multi-Agent Compliance System

**🚨 HACKATHON DEMO PROJECT - NOT FOR PRODUCTION USE 🚨**

A demonstration governance middleware API that processes LLM outputs through 5 specialized compliance agents running concurrently. Built in 2 days for AWS & Impetus GenAI Hackathon 2025.

## 🌐 **Live Demo Access**

### **🎮 Interactive Demo**
**Access the project demo here:** https://gtjwwsonixepfg6ttgnjnxgbda0ooaxa.lambda-url.us-east-1.on.aws/demo

### **🔗 API Endpoint** 
**Access the project endpoint here:** https://gtjwwsonixepfg6ttgnjnxgbda0ooaxa.lambda-url.us-east-1.on.aws/govern

### **🎥 Demo Video**
**Watch the demo video here:** https://www.youtube.com/watch?v=yY4EAecQ2Po

## 🎯 Overview

This demo system processes LLM outputs through 5 independent compliance agents in **concurrent execution**:

1. **Data Privacy & Security Agent** - GDPR, CCPA, PII detection
2. **AI Risk & Ethics Agent** - EU AI Act, bias detection, ethical concerns  
3. **Content & Platform Compliance Agent** - DSA, NIS2, harmful content
4. **Standards & Quality Agent** - ISO/IEC 42001, quality assessment
5. **Legal & Regulatory Agent** - Cross-jurisdictional compliance, legal risks

## 🏗️ Architecture

- **FastAPI REST API** with `/govern` endpoint
- **Concurrent Processing** - 5 simultaneous AWS Bedrock calls using **Llama 3.3 70B Instruct**
- **Multi-Agent Analysis** - Each agent makes independent API calls for specialized compliance checking
- **Simplified Output** - Clean JSON response with individual agent results
- **Stateless Design** - No database required, perfect for demo

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- AWS Account with Bedrock access
- AWS credentials configured
- **Llama 3.3 70B Instruct** model access in Bedrock (us-east-1 region)

### Installation

1. **Clone and setup:**
```bash
git clone <repository>
cd governance
pip install -r requirements-ultra-minimal.txt
```

2. **Configure AWS credentials:**
```bash
# Option 1: AWS CLI
aws configure

# Option 2: Environment variables
export AWS_ACCESS_KEY_ID=your_access_key
export AWS_SECRET_ACCESS_KEY=your_secret_key
export AWS_REGION=us-east-1
```

3. **Run the demo:**
```bash
python main.py
```

The demo API will be available at `http://localhost:8000`

## 📡 API Usage

### Main Endpoint: `/govern`

**POST** `/govern`

**Headers:**
- `Content-Type: application/json`
- `Accept: application/json`
- **No authentication required** (demo only)

**Request Body:**
```json
{
  "llm_output": "Content to analyze for compliance",
  "client_id": "demo-client"
}
```

**Response:**
```json
{
  "original_output": "Content that was analyzed",
  "governance_results": {
    "data_privacy_security": {
      "agent_name": "Data Privacy & Security",
      "score": 0.8,
      "flag_type": "none",
      "violations": [],
      "reasoning": "No privacy concerns detected in the content",
      "specific_findings": [],
      "recommendations": []
    },
    "ai_risk_ethics": {
      "agent_name": "AI Risk & Ethics", 
      "score": 0.9,
      "flag_type": "none",
      "violations": [],
      "reasoning": "Content shows no ethical concerns or bias",
      "specific_findings": [],
      "recommendations": []
    },
    "content_platform": {
      "agent_name": "Content & Platform Compliance",
      "score": 0.9,
      "flag_type": "none", 
      "violations": [],
      "reasoning": "Content is safe and compliant with platform policies",
      "specific_findings": [],
      "recommendations": []
    },
    "standards_quality": {
      "agent_name": "Standards & Quality",
      "score": 0.8,
      "flag_type": "none",
      "violations": [],
      "reasoning": "Content meets quality standards",
      "specific_findings": [],
      "recommendations": []
    },
    "legal_regulatory": {
      "agent_name": "Legal & Regulatory",
      "score": 0.9,
      "flag_type": "none",
      "violations": [],
      "reasoning": "No legal risks identified in the content",
      "specific_findings": [],
      "recommendations": []
    }
  }
}
```

### Demo Endpoints

- **GET** `/` - API information
- **GET** `/health` - Health check
- **GET** `/demo` - **Interactive demo page** (recommended for testing)
- **GET** `/docs` - Swagger API documentation

## 🧪 Testing the Demo

### Option 1: Web Interface (Recommended)
1. Go to `http://localhost:8000/demo`
2. Enter test content in the text area
3. Click "Analyze Content"
4. View real-time compliance analysis

### Option 2: API Call
```bash
curl -X POST "http://localhost:8000/govern" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -d '{
    "llm_output": "Hello, my email is john@example.com",
    "client_id": "demo-test"
  }'
```

### Sample Test Cases

1. **Clean Content:** `"Hello, how are you today?"`
   - Expected: All agents score 0.8+ with no violations

2. **PII Content:** `"My email is john@example.com and phone is 555-1234"`
   - Expected: Data Privacy agent flags PII exposure

3. **Biased Content:** `"Women are bad at technical jobs"`
   - Expected: AI Ethics agent flags discrimination risk

## 🔧 Configuration

### Environment Variables

- `AWS_REGION` - AWS region for Bedrock (default: us-east-1)
- `BEDROCK_MODEL_ID` - Model ID (default: us.meta.llama3-3-70b-instruct-v1:0)
- `LOG_LEVEL` - Logging level (default: INFO)

### Model Configuration

The demo uses **Llama 3.3 70B Instruct** via AWS Bedrock:
- **Model ID:** `us.meta.llama3-3-70b-instruct-v1:0`
- **Region:** us-east-1 (required for this model)
- **Concurrent Calls:** 5 simultaneous API requests (one per agent)
- **JSON Optimized:** Strict prompts for reliable JSON output

## 📊 Agent Scoring

Each agent returns:
- **Score:** 0.0-1.0 (1.0 = fully compliant)
- **Flag Type:** none, low-risk, medium-risk, high-risk
- **Violations:** List of specific issues found
- **Reasoning:** One-sentence explanation
- **Findings:** Specific problems identified
- **Recommendations:** Actionable suggestions

## 🚀 AWS Lambda Deployment

**For Hackathon Demo Only - Not Production Ready**

1. **Use the deployment script:**
```bash
python deploy_ultra_minimal.py
```

2. **Upload via AWS Console:**
   - Go to AWS Lambda Console
   - Create/update function: `ai-governance-api`
   - Upload: `ai-governance-lambda-ultra.zip`
   - Set Memory: 1024 MB (required)
   - Set Timeout: 900 seconds (15 minutes)

3. **Test the deployed function:**
   - Use API Gateway URL + `/demo` for web interface
   - Use API Gateway URL + `/govern` for API calls

## ⚠️ Demo Limitations

**This is a hackathon demonstration project with the following limitations:**

- **No Authentication** - Open API for demo purposes
- **No Rate Limiting** - Unlimited requests (demo only)
- **No Data Persistence** - No database or storage
- **Single Model** - Only Llama 3.3 70B Instruct
- **English Only** - Primarily designed for English content
- **Basic Error Handling** - Minimal production safeguards
- **No Monitoring** - Basic logging only
- **No Caching** - Every request hits Bedrock
- **No Load Balancing** - Single instance deployment

## 🔒 Security Notice

**⚠️ DEMO SECURITY - NOT FOR PRODUCTION ⚠️**

- No API authentication required
- No input validation beyond basic JSON parsing
- No output sanitization
- AWS credentials required for Bedrock access
- All requests logged for demo purposes

## 📈 Performance

- **Concurrent Processing** - 5 agents run simultaneously
- **Response Time** - 15-30 seconds (5 Bedrock API calls)
- **Cold Start** - First Lambda request may take 30+ seconds
- **Warm Requests** - Subsequent requests faster
- **Memory Usage** - 1024 MB Lambda memory required

## 🛠️ Project Structure

```
governance/
├── main.py                 # FastAPI application
├── lambda_handler.py       # AWS Lambda entry point
├── models.py              # Simplified Pydantic models
├── bedrock_client.py      # AWS Bedrock integration
├── agents/                # 5 independent agents
│   ├── data_privacy_agent.py
│   ├── ai_ethics_agent.py
│   ├── content_compliance_agent.py
│   ├── standards_quality_agent.py
│   └── legal_regulatory_agent.py
├── utils/                 # Processing utilities
│   ├── batch_processor.py
│   └── response_formatter.py
├── requirements-ultra-minimal.txt  # Pure Python dependencies
├── deploy_ultra_minimal.py         # Lambda deployment script
└── README.md
```

## 🎯 Hackathon Demo Features

✅ **Multi-Agent Architecture** - 5 specialized compliance agents  
✅ **Concurrent Processing** - Parallel Bedrock API calls  
✅ **Real-time Analysis** - Sub-30 second response times  
✅ **Interactive Demo** - Web UI for easy testing  
✅ **AWS Integration** - Serverless Lambda deployment  
✅ **JSON API** - Clean, structured responses  
✅ **Zero Dependencies** - Pure Python, no binaries  

## 🚧 Future Enhancements

This demo could be expanded with:
- Multi-LLM model support (GPT-4, Claude, Gemini)
- RAG integration with compliance documentation
- Custom rule engines for organization-specific policies
- Persistent analytics and reporting
- Authentication and rate limiting
- Multi-language support
- Real-time streaming analysis

## 📞 Demo Support

For demo issues:
1. Check AWS Bedrock access and credentials
2. Verify Llama 3.3 70B model availability in us-east-1
3. Check Lambda memory is set to 1024 MB
4. Use `/health` endpoint to verify API status
5. Check CloudWatch logs for detailed error messages

---

**🏆 Built for AWS & Impetus GenAI Hackathon 2025**  
**⚡ 2-Day Development Sprint**  
**🎯 Proof of Concept - Multi-Agent AI Governance**
