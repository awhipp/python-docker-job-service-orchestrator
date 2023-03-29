$body = @{
    service_name = "sample_python_service"
    replicas = 3
} | ConvertTo-Json

Invoke-RestMethod -Method Put `
                  -Uri "http://localhost:5000/services/scale" `
                  -ContentType "application/json" `
                  -Body $body
