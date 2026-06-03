FROM rocm/pytorch:rocm6.2_ubuntu22.04_py3.10_pytorch_release_2.3.0

LABEL maintainer="DevSelf12"
LABEL description="hip-benchmark-suite -- HIP kernel benchmarks"

WORKDIR /workspace/hip-benchmark-suite

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "run_all.py", "--cpu"]
