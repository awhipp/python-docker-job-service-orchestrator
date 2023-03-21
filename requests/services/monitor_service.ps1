# Monitor a job through a PS1 GET call

Invoke-RestMethod -Method Get `
                  -Uri "http://localhost:5000/monitor_service?service_name=sample_python_service" `
                  -ContentType "application/json" `
                  -Body $body
