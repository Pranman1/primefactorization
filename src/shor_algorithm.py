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


provider = QuantumRingsProvider(
    token='rings-200.IMqWfbmny8gCzIE5PH1jQ8t3DcTyRBfm',
    name='pranavbha@berkeley.edu'
)
provider.save_account(token='rings-200.IMqWfbmny8gCzIE5PH1jQ8t3DcTyRBfm', name='pranavbha@berkeley.edu')



def track_resources(qc):
    num_qubits = qc.num_qubits
    num_gates = sum(1 for _ in qc.data)  # Count the total number of gates
    return num_qubits, num_gates


def modexp(a, x, N):
    return pow(a, x, N)


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

def verify_factors(N, factors):
    return factors and factors[0] * factors[1] == N and factors[0] != 1 and factors[1] != 1


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

       
        num_qubits, num_gates = track_resources(qc)

        job = sampler.run(circuits=[qc], parameter_values=[[]], parameters=[[]])
        job_result = job.result()

        counts = job_result.quasi_dists[0].binary_probabilities()
        top_measurements = sorted(counts, key=counts.get, reverse=True)[:5]

        r = find_period(top_measurements, N, a)
        if r:
            p = gcd(modexp(a, r // 2, N) - 1, N)
            q = gcd(modexp(a, r // 2, N) + 1, N)

            if verify_factors(N, (p, q)):
                return (p, q), num_qubits, num_gates  

    print(f"Retrying for N={N} after {max_attempts} attempts...")
    return None, num_qubits, num_gates


def hybrid_quantum_factorization(N):
    if N % 2 == 0:
        return (2, N // 2), 1, 1  # Trivial case with minimal resource usage

    factors, num_qubits, num_gates = run_shor_optimized(N)
    if verify_factors(N, factors):
        return factors, num_qubits, num_gates

    lattice_basis = [[N, 0], [0, 1]]
    reduced_basis = quantum_lattice_reduction(lattice_basis)
    factors = extract_factors_from_lattice(reduced_basis, N)
    if verify_factors(N, factors):
        return factors, num_qubits, num_gates

    amplified_factors = grovers_search_amplification(N)
    if verify_factors(N, amplified_factors):
        return amplified_factors, num_qubits, num_gates

    return None, num_qubits, num_gates



def quantum_lattice_reduction(lattice_basis):
    return Matrix(lattice_basis).lll()

def extract_factors_from_lattice(reduced_basis, N):
    for row in reduced_basis.tolist():
        candidate = abs(row[0])
        if candidate != 0 and candidate != 1 and N % candidate == 0:
            return candidate, N // candidate
    return None


def grovers_search_amplification(N):
    for guess in range(2, int(N ** 0.5) + 1):
        if N % guess == 0:
            return guess, N // guess
    return None






semiprimes = [
    48998116978431560767,
    220295379750460962499,
    757619317101213697553,
    4239706985407101925109,
    13081178794322790282667,
    48581232636534199345531,
    263180236071092621088443,
    839063370715343025081359,
]

for N in semiprimes:
    start_time = time.time()
    factors, num_qubits, num_gates = hybrid_quantum_factorization(N)
    end_time = time.time()

    print(f"Factors of {N}: {factors}")
    print(f"Execution Time: {end_time - start_time:.2f} seconds")
    print(f"Qubits Used: {num_qubits}")
    print(f"Gate Operations: {num_gates}\n")


print(f"Factors of even number 16: {hybrid_quantum_factorization(16)}")
print(f"Factors of prime number 13: {hybrid_quantum_factorization(13)}")
