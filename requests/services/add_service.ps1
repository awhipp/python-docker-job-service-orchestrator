$body = @{
    service_name = "sample_python_service"
    image = "sample_python_service:latest"
} | ConvertTo-Json

Invoke-RestMethod -Method Post `
                  -Uri "http://localhost:5000/add_service" `
                  -ContentType "application/json" `
                  -Body $body
