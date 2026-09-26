from flask import Flask, jsonify
import os, socket
import boto3
from botocore.config import Config
from botocore.exceptions import BotoCoreError, ClientError

app = Flask(__name__)
# Fail fast instead of letting a slow/flaky connection to AWS block the
# whole (single) gunicorn worker for up to its 30s timeout.
boto_config = Config(connect_timeout=3, read_timeout=3, retries={"max_attempts": 2})
dynamodb = boto3.resource("dynamodb", config=boto_config)
table = dynamodb.Table(os.getenv("COUNTER_TABLE", "thumbs-up-counter"))

def get_count():
    try:
        response = table.get_item(Key={"id": "counter"})
        return response.get("Item", {}).get("count", 0)
    except (ClientError, BotoCoreError) as e:
        print(f"Failed to read counter: {e}")
        return 0

@app.route("/")
def home():
    env = os.getenv("APP_ENV", "development")
    version = os.getenv("APP_VERSION", "local")
    hostname = socket.gethostname()
    count = get_count()
    color = {"staging": "#f59e0b", "production": "#16a34a"}.get(env, "#6b7280")
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Liliya Petillo</title>
  <style>
    body {{
      font-family: system-ui, sans-serif;
      background: #f3f4f6;
      display: flex;
      align-items: center;
      justify-content: center;
      min-height: 100vh;
      margin: 0;
      padding: 2rem 1rem;
    }}
    .card {{
      background: white;
      padding: 3.5rem;
      border-radius: 16px;
      box-shadow: 0 4px 12px rgba(0,0,0,0.1);
      text-align: center;
      max-width: 680px;
    }}
    .avatar {{
      width: 180px;
      height: 180px;
      border-radius: 50%;
      object-fit: cover;
      margin-bottom: 1.5rem;
    }}
    h1 {{
      margin: 0 0 0.4rem;
      font-size: 2rem;
    }}
    .subtitle {{
      color: #6b7280;
      font-size: 1.1rem;
      margin-bottom: 0.35rem;
    }}
    .location {{
      color: #9ca3af;
      font-size: 0.95rem;
      margin-bottom: 1.25rem;
    }}
    .about-heading {{
      text-align: left;
      font-size: 0.8rem;
      font-weight: 700;
      letter-spacing: 0.05em;
      text-transform: uppercase;
      color: #9ca3af;
      margin: 0 0 0.5rem;
    }}
    .summary {{
      color: #374151;
      font-size: 0.95rem;
      line-height: 1.6;
      text-align: left;
      margin-bottom: 1.5rem;
    }}
    .summary p {{
      margin: 0 0 0.9rem;
    }}
    .summary p:last-child {{
      margin-bottom: 0;
    }}
    .certs {{
      list-style: none;
      padding: 0;
      margin: 0 0 1.5rem;
      font-size: 0.95rem;
      color: #374151;
      text-align: left;
      background: #f9fafb;
      border-radius: 8px;
      padding: 1rem 1.25rem;
    }}
    .certs li {{
      padding: 0.25rem 0;
    }}
    .links a {{
      color: #2563eb;
      text-decoration: none;
      margin: 0 0.5rem;
      font-size: 1.05rem;
    }}
    .links a:hover {{
      text-decoration: underline;
    }}
    .thumbs-form {{
      margin: 2rem 0;
    }}
    button.thumbs {{
      font-size: 1.3rem;
      padding: 0.75rem 1.5rem;
      border: none;
      border-radius: 8px;
      background: #2563eb;
      color: white;
      cursor: pointer;
    }}
    button.thumbs:hover {{
      background: #1d4ed8;
    }}
    .meta {{
      margin-top: 1.25rem;
      font-size: 0.75rem;
      color: {color};
    }}
  </style>
</head>
<body>
  <div class="card">
    <picture>
      <source srcset="/static/headshot.avif" type="image/avif">
      <img class="avatar" src="/static/headshot.jpg" alt="Liliya Petillo">
    </picture>
    <h1>Liliya Petillo</h1>
    <div class="subtitle">Senior QA engineer moving into cloud and DevOps</div>
    <div class="location">Staten Island, NY</div>

    <div class="about-heading">About me</div>
    <div class="summary">
      <p>
        I'm Liliya, a QA engineer with 10+ years of experience testing web, iOS, and Android products, and I'm now moving into cloud and DevOps. Over the years I've built automation frameworks, wired tests into CI/CD pipelines, and owned quality on platforms where mistakes are costly, including a state government licensing platform and a healthcare-adjacent ordering portal.
      </p>
      <p>
        The move to cloud felt natural. After enough time working inside pipelines, I wanted to understand what runs underneath them. So I earned my AWS Cloud Practitioner and HashiCorp Terraform Associate certifications, and I've been building ever since: containerized projects with Docker deployed through GitHub Actions, small AWS environment entirely in Terraform, and a serverless CRUD app.
      </p>
      <p>
        What I bring is a tester's habit of asking "what could break here?", comfort working in regulated, security-conscious environments, and a knack for picking up new tools quickly. This site is where I share the projects I build along the way.
      </p>
    </div>

    <ul class="certs">
      <li>AWS Certified Cloud Practitioner (CLF-C02)</li>
      <li>HashiCorp Certified: Terraform Associate (TA-004)</li>
      <li>ISTQB CTFL - Certified Tester Foundation Level</li>
    </ul>

    <div class="links">
      <a href="mailto:liliya.petillo@gmail.com">Email</a>&middot;
      <a href="https://linkedin.com/in/liliya-petillo" target="_blank">LinkedIn</a>&middot;
      <a href="https://github.com/liliyapetillo/portfolio" target="_blank">GitHub</a>
    </div>

    <div class="thumbs-form">
      <button type="button" class="thumbs" id="thumbs-btn" onclick="likeIt()">👍 <span id="count">{count}</span></button>
    </div>

    <div class="meta">Environment: {env.upper()} · Commit: {version[:7]} · Container: {hostname}</div>
  </div>
  <script>
    async function likeIt() {{
      const btn = document.getElementById('thumbs-btn');
      const countEl = document.getElementById('count');
      btn.disabled = true;
      try {{
        const res = await fetch('/like', {{ method: 'POST' }});
        if (res.ok) {{
          const data = await res.json();
          countEl.textContent = data.count;
        }}
      }} catch (err) {{
        console.error('Failed to update counter', err);
      }} finally {{
        btn.disabled = false;
      }}
    }}
  </script>
</body>
</html>
"""

@app.route("/like", methods=["POST"])
def like():
    try:
        response = table.update_item(
            Key={"id": "counter"},
            UpdateExpression="ADD #c :incr",
            ExpressionAttributeNames={"#c": "count"},
            ExpressionAttributeValues={":incr": 1},
            ReturnValues="UPDATED_NEW",
        )
        return jsonify({"count": int(response["Attributes"]["count"])})
    except (ClientError, BotoCoreError) as e:
        print(f"Failed to update counter: {e}")
        return jsonify({"error": "Failed to update counter"}), 502

@app.route("/health")
def health():
    return jsonify({"status": "ok"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
