from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter()

@router.get("/privacy", response_class=HTMLResponse)
def privacy_policy():
    return """
    <html>
      <head><title>Privacy Policy</title></head>
      <body>
        <h1>Privacy Policy</h1>
        <p>This API provides NBA statistics using publicly available data.</p>
        <p>No personal data is collected, stored, or shared.</p>
        <p>Requests may be cached temporarily for performance.</p>
        <p>No user-identifying information is retained.</p>
      </body>
    </html>
    """
