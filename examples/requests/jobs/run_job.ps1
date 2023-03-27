$body = @{
    image = "sample_python_job:latest"
    job_name = "sample_python_job"
} | ConvertTo-Json

Invoke-RestMethod -Method Post `
                  -Uri "http://localhost:5000/jobs/run" `
                  -ContentType "application/json" `
                  -Body $body
