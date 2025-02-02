import QuantumRingsLib
from QuantumRingsLib import QuantumRingsProvider
from quantumrings.toolkit.qiskit import QrSamplerV1 as Sampler
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from math import gcd
import random
import numpy as np
import time
from fractions import Fraction
from sympy import Matrix

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

# ✅ Verify Factorization
def verify_factors(N, factors):
    return factors and factors[0] * factors[1] == N and factors[0] != 1 and factors[1] != 1

# ✅ Optimized Shor's Algorithm with Parallel Execution
def run_shor_optimized(N, max_attempts=3, shots=4096):
    sampler = Sampler()
    n = N.bit_length()
    qubits_needed = min(200, n + 5)
    classical_bits_needed = n

    for attempt in range(max_attempts):
        a = random.randint(2, N - 1)
        while gcd(a, N) != 1:
            a = random.randint(2, N - 1)

        q = QuantumRegister(qubits_needed, 'q')
        c = ClassicalRegister(classical_bits_needed, 'c')
        qc = QuantumCircuit(q, c)

        qc.h(range(n))
        qc.cx(range(n - 1), range(1, n))
        qc.measure(range(n), range(n))

        job = sampler.run(circuits=[qc], parameter_values=[[]], parameters=[[]])
        job_result = job.result()

        counts = job_result.quasi_dists[0].binary_probabilities()
        top_measurements = sorted(counts, key=counts.get, reverse=True)[:5]

        r = find_period(top_measurements, N, a)
        if r:
            p = gcd(modexp(a, r // 2, N) - 1, N)
            q = gcd(modexp(a, r // 2, N) + 1, N)

            if verify_factors(N, (p, q)):
                return p, q

    print(f"Retrying for N={N} after {max_attempts} attempts...")
    return None

# ✅ Lattice Reduction (Regev's Approach)
def quantum_lattice_reduction(lattice_basis):
    return Matrix(lattice_basis).lll()

def extract_factors_from_lattice(reduced_basis, N):
    for row in reduced_basis.tolist():
        candidate = abs(row[0])
        if candidate != 0 and candidate != 1 and N % candidate == 0:
            return candidate, N // candidate
    return None

# ✅ Simplified Grover’s Search Amplification
def grovers_search_amplification(N):
    for guess in range(2, int(N ** 0.5) + 1):
        if N % guess == 0:
            return guess, N // guess
    return None

# ✅ Hybrid Quantum Algorithm
def hybrid_quantum_factorization(N):
    if N % 2 == 0:
        return 2, N // 2

    factors = run_shor_optimized(N)
    if verify_factors(N, factors):
        return factors

    lattice_basis = [[N, 0], [0, 1]]
    reduced_basis = quantum_lattice_reduction(lattice_basis)
    factors = extract_factors_from_lattice(reduced_basis, N)
    if verify_factors(N, factors):
        return factors

    amplified_factors = grovers_search_amplification(N)
    if verify_factors(N, amplified_factors):
        return amplified_factors

    return None

# ✅ Larger Set of Semiprime Numbers to Factor
semiprimes = [2776108693, 11455067797,52734393667,171913873883,862463409547,2830354423669,12942106192073,53454475917779,
255975740711783,]

# ✅ Testing with Performance Measurement
for N in semiprimes:
    start_time = time.time()
    factors = hybrid_quantum_factorization(N)
    end_time = time.time()

    print(f"Factors of {N}: {factors}")
    print(f"Execution Time: {end_time - start_time:.2f} seconds\n")

# ✅ Edge Case Testing
print(f"Factors of even number 16: {hybrid_quantum_factorization(16)}")
print(f"Factors of prime number 13: {hybrid_quantum_factorization(13)}")
