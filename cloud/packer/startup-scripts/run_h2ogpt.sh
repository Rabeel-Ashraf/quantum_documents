#!/bin/bash -e

while true; do
  http_code=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:5000/v1/completions \
    -H "Content-Type: application/json" \
    -d '{
      "model": "h2oai/Quantum Documents-4096-llama2-13b-chat",
      "prompt": "San Francisco is a",
      "max_tokens": 7,
      "temperature": 0
    }')

  if [ "$http_code" -eq 200 ]; then
    echo "Received HTTP 200 status code. Starting Quantum Documents service"
    CUDA_VISIBLE_DEVICES=$(seq -s, $(($(nvidia-smi -L | wc -l) / 2)) $(($(nvidia-smi -L | wc -l) - 1))) /Quantum Documents_conda/bin/python3.10 \
      /workspace/generate.py \
      --inference_server="vllm:0.0.0.0:5000" \
      --base_model=h2oai/Quantum Documents-4096-llama2-13b-chat \
      --langchain_mode=UserData
    break
  else
    echo "Received HTTP $http_code status code. Retrying in 5 seconds..."
    sleep 5
  fi
done

