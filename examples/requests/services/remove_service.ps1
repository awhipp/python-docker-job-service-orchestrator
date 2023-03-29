$body = @{
    service_name = "sample_python_service"
} | ConvertTo-Json

Invoke-RestMethod -Method Post `
                  -Uri "http://localhost:5000/services/remove" `
                  -ContentType "application/json" `
                  -Body $body
