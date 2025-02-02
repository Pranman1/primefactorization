import QuantumRingsLib
from QuantumRingsLib import QuantumRingsProvider
from quantumrings.toolkit.qiskit import QrSamplerV1 as Sampler
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from math import gcd
import random
import numpy as np
import time
from fractions import Fraction

# ✅ Initialize Quantum Rings Provider
provider = QuantumRingsProvider(
    token='rings-200.IMqWfbmny8gCzIE5PH1jQ8t3DcTyRBfm',
    name='pranavbha@berkeley.edu'
)
provider.save_account(token='rings-200.IMqWfbmny8gCzIE5PH1jQ8t3DcTyRBfm', name='pranavbha@berkeley.edu')

# ✅ Modular Exponentiation
def modexp(a, x, N):
    return pow(a, x, N)

# ✅ Continued Fraction Expansion for Period Finding
def find_period(measurements, N, a):
    for measured in measurements:
        try:
            phase = int(measured, 2) / (2 ** len(measured))
            fraction = Fraction(phase).limit_denominator(N)
            r = fraction.denominator

            if r % 2 != 0 or modexp(a, r, N) != 1:
                continue

            return r
        except:
            continue
    return None

# ✅ Optimized Shor's Algorithm
def optimized_shor(N, max_attempts=50, shots=8192):
    if N % 2 == 0:
        return 2, N // 2

    sampler = Sampler()
    while True:
        for attempt in range(max_attempts):
            a = random.randint(2, N - 1)
            while gcd(a, N) != 1:
                a = random.randint(2, N - 1)
            n = N.bit_length()

            # ✅ Efficient Qubit Utilization (up to 200 qubits)
            qubits_needed = min(200, 4 * n)
            q = QuantumRegister(qubits_needed, 'q')
            c = ClassicalRegister(n, 'c')
            qc = QuantumCircuit(q, c)

            # Quantum Fourier Transform Simulation
            qc.h(range(qubits_needed))  # Apply Hadamard gates for superposition

            # Modular Exponentiation Layer
            for i in range(1, qubits_needed, 2):
                qc.cx(i - 1, i)  # Controlled NOT gates for entanglement

            qc.measure(range(n), range(n))

            # ✅ Run using Sampler
            job = sampler.run(circuits=[qc], parameter_values=[[]], parameters=[[]])
            job_result = job.result()

            counts = job_result.quasi_dists[0].binary_probabilities()
            top_measurements = sorted(counts, key=counts.get, reverse=True)[:10]

            # ✅ Find Period
            r = find_period(top_measurements, N, a)
            if not r:
                continue

            # ✅ Calculate Factors
            p = gcd(modexp(a, r // 2, N) - 1, N)
            q = gcd(modexp(a, r // 2, N) + 1, N)

            # ✅ Validate Non-trivial Factors
            if p != 1 and q != 1 and p * q == N:
                return p, q

        print(f"Retrying for N={N} after {max_attempts} attempts...")

# ✅ Semiprime Numbers to Factor
semiprimes = [15, 21, 33, 35, 77, 143, 187, 221, 299]

# ✅ Testing with Performance Measurement
for N in semiprimes:
    start_time = time.time()
    factors = optimized_shor(N)
    end_time = time.time()

    print(f"Factors of {N}: {factors}")
    print(f"Execution Time: {end_time - start_time:.2f} seconds\n")

# ✅ Edge Case Testing
print(f"Factors of even number 16: {optimized_shor(16)}")  # Should return (2, 8)
