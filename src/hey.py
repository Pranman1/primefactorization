from qiskit import QuantumCircuit
from qiskit import Aer
# Create a Quantum Circuit with 2 qubits and 2 classical bits
qc = QuantumCircuit(2, 2)

# Add a Hadamard gate on qubit 0
qc.h(0)

# Add a CNOT gate on control qubit 0 and target qubit 1
qc.cx(0, 1)

# Measure qubits
qc.measure([0, 1], [0, 1])

# Execute the circuit on the qasm simulator
backend = Aer.get_backend('qasm_simulator')
job = execute(qc, backend, shots=1024)

# Grab results from the job
result = job.result()

# Returns counts
counts = result.get_counts(qc)
print("\nTotal count for 00 and 11 are:", counts)
