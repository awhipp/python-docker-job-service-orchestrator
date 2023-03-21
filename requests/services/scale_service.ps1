$body = @{
    service_name = "sample_python_service"
    replicas = 3
} | ConvertTo-Json

Invoke-RestMethod -Method Post `
                  -Uri "http://localhost:5000/scale_service" `
                  -ContentType "application/json" `
                  -Body $body
