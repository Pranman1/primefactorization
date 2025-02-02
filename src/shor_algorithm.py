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

# ✅ Shor’s Algorithm with Consistent Factorization
def shor(N, max_attempts=50, shots=4096):
    if N % 2 == 0:
        return 2, N // 2

    sampler = Sampler()
    while True:  # Keep running until correct factors are found
        for attempt in range(max_attempts):
            a = random.randint(2, N - 1)
            while gcd(a, N) != 1:
                a = random.randint(2, N - 1)
            n = N.bit_length()

            # ✅ Quantum Circuit
            q = QuantumRegister(2 * n, 'q')
            c = ClassicalRegister(n, 'c')
            qc = QuantumCircuit(q, c)

            qc.h(range(n))                   # Apply Hadamard gates
            qc.cx(range(n), range(n, 2 * n)) # Apply CNOT gates
            qc.measure(range(n), range(n))

            # ✅ Run using Sampler
            job = sampler.run(circuits=[qc], parameter_values=[[]], parameters=[[]])
            job_result = job.result()

            counts = job_result.quasi_dists[0].binary_probabilities()
            # ✅ Analyze Top 5 Measurement Results for better accuracy
            top_measurements = sorted(counts, key=counts.get, reverse=True)[:5]

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

        # If factors not found, retry
        print(f"Retrying for N={N} after {max_attempts} attempts...")

# ✅ Semiprime Numbers to Factor
semiprimes = [15, 21, 33, 35, 77, 143, 187, 221, 299]

# ✅ Testing with Performance Measurement
for N in semiprimes:
    start_time = time.time()
    factors = shor(N)
    end_time = time.time()

    print(f"Factors of {N}: {factors}")
    print(f"Execution Time: {end_time - start_time:.2f} seconds\n")

# ✅ Edge Case Testing
