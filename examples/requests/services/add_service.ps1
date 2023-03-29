$body = @{
    service_name = "sample_python_service"
    image = "sample_python_service:latest"
} | ConvertTo-Json

Invoke-RestMethod -Method Post `
                  -Uri "http://localhost:5000/services/add" `
                  -ContentType "application/json" `
                  -Body $body
