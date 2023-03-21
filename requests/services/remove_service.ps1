$body = @{
    service_name = "sample_python_service"
} | ConvertTo-Json

Invoke-RestMethod -Method Post `
                  -Uri "http://localhost:5000/remove_service" `
                  -ContentType "application/json" `
                  -Body $body
