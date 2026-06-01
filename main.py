from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
import uvicorn
import os
from dotenv import load_dotenv
from models import GovernanceRequest, GovernanceResponse
from utils.batch_processor import BatchProcessor
from utils.response_formatter import ResponseFormatter
import logging

# Load environment variables
load_dotenv()

# Configure logging
log_level = os.getenv('LOG_LEVEL', 'INFO')
logging.basicConfig(level=getattr(logging, log_level.upper()))
logger = logging.getLogger(__name__)

app = FastAPI(
    title="AI Governance Middleware",
    description="Multi-Agent AI Governance System for LLM Output Compliance",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize processors
batch_processor = BatchProcessor()
response_formatter = ResponseFormatter()

@app.get("/")
async def root():
    return {"message": "AI Governance Middleware API", "version": "1.0.0"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "ai-governance-middleware"}

@app.post("/govern", response_model=GovernanceResponse)
async def govern_llm_output(request: GovernanceRequest):
    """
    Main governance endpoint that processes LLM output through 5 compliance agents
    """
    try:
        logger.info(f"Processing governance request for client: {request.client_id}")
        
        # Process through all 5 agents in batch
        agent_results = await batch_processor.process_all_agents(request.llm_output)
        
        # Format comprehensive response
        response = response_formatter.format_response(
            original_output=request.llm_output,
            agent_results=agent_results
        )
        
        logger.info(f"Governance analysis complete with {len(response.governance_results)} agents")
        return response
        
    except Exception as e:
        logger.error(f"Error processing governance request: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.get("/demo", response_class=HTMLResponse)
async def demo_page():
    """
    Simple demo page for testing the governance API
    """
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>AI Governance Demo</title>
        <style>
            body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }
            textarea { width: 100%; height: 200px; margin: 10px 0; }
            button { background: #007bff; color: white; padding: 10px 20px; border: none; cursor: pointer; border-radius: 4px; }
            button:disabled { background: #6c757d; cursor: not-allowed; }
            .result { background: #f8f9fa; padding: 15px; margin: 10px 0; border-radius: 5px; }
            .risk-high { border-left: 5px solid #dc3545; }
            .risk-medium { border-left: 5px solid #ffc107; }
            .risk-low { border-left: 5px solid #28a745; }
            .risk-flagged { border-left: 5px solid #17a2b8; }
            
            #loading { 
                text-align: center; 
                padding: 20px; 
                background: #e3f2fd; 
                border-radius: 5px; 
                margin: 10px 0; 
            }
            
            .loading-spinner {
                border: 4px solid #f3f3f3;
                border-top: 4px solid #007bff;
                border-radius: 50%;
                width: 40px;
                height: 40px;
                animation: spin 1s linear infinite;
                margin: 0 auto 10px;
            }
            
            @keyframes spin {
                0% { transform: rotate(0deg); }
                100% { transform: rotate(360deg); }
            }
        </style>
    </head>
    <body>
        <h1>AI Governance Middleware Demo</h1>
        <p>Test the governance system by entering LLM output below:</p>
        
        <textarea id="llmOutput" placeholder="Enter LLM output to analyze..."></textarea>
        <br>
        <button id="analyzeBtn" onclick="analyzeContent()">Analyze Content</button>
        
        <div id="loading" style="display: none;">
            <div class="loading-spinner"></div>
            <p>Analyzing content through 5 compliance agents...</p>
        </div>
        
        <div id="results"></div>
        
        <script>
            async function analyzeContent() {
                const output = document.getElementById('llmOutput').value;
                const analyzeBtn = document.getElementById('analyzeBtn');
                const loadingDiv = document.getElementById('loading');
                const resultsDiv = document.getElementById('results');
                
                if (!output.trim()) {
                    alert('Please enter some content to analyze');
                    return;
                }
                
                // Show loading state
                analyzeBtn.disabled = true;
                analyzeBtn.textContent = 'Analyzing...';
                loadingDiv.style.display = 'block';
                resultsDiv.innerHTML = '';
                
                try {
                    const response = await fetch('/govern', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({
                            llm_output: output,
                            client_id: 'demo-client'
                        })
                    });
                    
                    if (!response.ok) {
                        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
                    }
                    
                    const result = await response.json();
                    displayResults(result);
                    
                } catch (error) {
                    console.error('Analysis error:', error);
                    resultsDiv.innerHTML = 
                        '<div class="result" style="border-left: 5px solid #dc3545;">' +
                        '<h3>Analysis Error</h3>' +
                        '<p><strong>Error:</strong> ' + error.message + '</p>' +
                        '<p>Please try again or check the server logs.</p>' +
                        '</div>';
                } finally {
                    // Hide loading state
                    analyzeBtn.disabled = false;
                    analyzeBtn.textContent = 'Analyze Content';
                    loadingDiv.style.display = 'none';
                }
            }
            
            function displayResults(result) {
                document.getElementById('results').innerHTML = `
                    <div class="result">
                        <h3>🔍 AI Governance Analysis</h3>
                        
                        <div style="display: grid; gap: 12px; margin-top: 15px;">
                            ${Object.entries(result.governance_results).map(([agent, data]) => {
                                const riskColor = data.flag_type === 'high-risk' ? '#dc3545' : 
                                                data.flag_type === 'medium-risk' ? '#ffc107' : '#28a745';
                                const riskIcon = data.flag_type === 'high-risk' ? '🚨' : 
                                               data.flag_type === 'medium-risk' ? '⚠️' : '✅';
                                
                                return `
                                    <div style="border: 1px solid #e9ecef; border-left: 3px solid ${riskColor}; border-radius: 6px; padding: 12px; background: white; box-shadow: 0 1px 3px rgba(0,0,0,0.1);">
                                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                                            <h4 style="margin: 0; color: #495057; font-size: 14px;">${riskIcon} ${data.agent_name}</h4>
                                            <span style="background: ${riskColor}; color: white; padding: 2px 6px; border-radius: 10px; font-size: 11px; font-weight: bold;">
                                                ${data.score}
                                            </span>
                                        </div>
                                        
                                        ${data.violations && data.violations.length > 0 ? `
                                            <div style="margin: 6px 0; padding: 4px 0;">
                                                <span style="font-size: 12px; color: #dc3545; font-weight: 600;">⚠ ${data.violations.join(', ')}</span>
                                            </div>
                                        ` : ''}
                                        
                                        ${data.specific_findings && data.specific_findings.length > 0 ? `
                                            <div style="margin: 6px 0; padding: 4px 0;">
                                                <div style="font-size: 12px; color: #6c757d; font-weight: 600;">Findings:</div>
                                                <div style="font-size: 12px; color: #6c757d; margin-top: 2px;">${data.specific_findings.join(' • ')}</div>
                                            </div>
                                        ` : ''}
                                        
                                        ${data.reasoning ? `
                                            <div style="margin: 6px 0; padding: 4px 0;">
                                                <div style="font-size: 12px; color: #495057; font-weight: 600;">Reasoning:</div>
                                                <div style="font-size: 12px; color: #495057; margin-top: 2px;">${data.reasoning}</div>
                                            </div>
                                        ` : ''}
                                        
                                        ${data.recommendations && data.recommendations.length > 0 ? `
                                            <div style="margin: 6px 0; padding: 4px 0;">
                                                <div style="font-size: 12px; color: #007bff; font-weight: 600;">Recommendations:</div>
                                                <div style="font-size: 12px; color: #007bff; margin-top: 2px;">${data.recommendations.join(' • ')}</div>
                                            </div>
                                        ` : ''}
                                    </div>
                                `;
                            }).join('')}
                        </div>
                    </div>
                `;
            }
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
