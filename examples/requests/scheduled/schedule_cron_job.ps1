$body = @{
    task_name = "sample_recurring"
    service_name = "sample_python_job"
    image = "sample_python_job:latest"
    cron = "*/1 * * * *"
} | ConvertTo-Json

Invoke-RestMethod -Method Post `
                  -Uri "http://localhost:5000/scheduler/recurring" `
                  -ContentType "application/json" `
                  -Body $body
