$body = @{
    job_text = "hi there"
} | ConvertTo-Json

Invoke-RestMethod -Method Post `
                  -Uri "http://localhost:5000/jobs/schedule" `
                  -ContentType "application/json" `
                  -Body $body
