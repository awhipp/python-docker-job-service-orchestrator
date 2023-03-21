# Monitor a job through a PS1 GET call

Invoke-RestMethod -Method Get `
                  -Uri "http://localhost:5000/monitor_job?job_name=sample_python_job" `
                  -ContentType "application/json" `
                  -Body $body
